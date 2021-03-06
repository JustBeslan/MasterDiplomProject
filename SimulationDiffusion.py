from random import shuffle

from Triangulation import Triangulation
from window.ParametersDiffusionWindow import ParametersDiffusionWindow
from window.ParametersTriangulationWindow import *
from window.SimulationDiffusionWindow import SimulationDiffusionWindow


class SimulationDiffusion:
    parameters_triangulation_window = None
    parameters_diffusion_window = None
    simulation_diffusion_window = None
    current_queue_triangles = None
    triangulation = None

    def __init__(self):
        self.show_parameters_triangulation_window()

    def show_parameters_triangulation_window(self):
        self.parameters_triangulation_window = \
            ParametersTriangulationWindow(func_load_triangulation=self.load_triangulation,
                                          func_start_triangulation=self.start_triangulation)
        self.parameters_triangulation_window.show()

    def show_parameters_diffusion_window(self):
        self.parameters_triangulation_window.close()
        self.parameters_diffusion_window = ParametersDiffusionWindow(triangulation=self.triangulation,
                                                                     func_start_simulation_diffusion=self.start)
        self.parameters_diffusion_window.show()

    def show_simulation_diffusion_window(self):
        self.parameters_diffusion_window.close()
        self.simulation_diffusion_window = \
            SimulationDiffusionWindow(parameters_diffusion=self.parameters_diffusion_window,
                                      func_update_discrete_values=self.update_discrete_values,
                                      func_update_float_values=self.update_float_values,
                                      triangulation=self.triangulation)
        self.simulation_diffusion_window.show()

    def start_triangulation(self, func_update_statusbar):
        try:
            self.triangulation = Triangulation(parameters_triangulation_window=self.parameters_triangulation_window)
            self.triangulation.build(func_update_statusbar=func_update_statusbar)
            func_update_statusbar(text="???????????????????????? ?????????????? ??????????????")
            self.show_parameters_diffusion_window()
        except Exception:
            QMessageBox.critical(self.parameters_triangulation_window,
                                 "????????????", "???????????? ???????????????? ????????????????????????")

    def load_triangulation(self):
        filename = QFileDialog.getOpenFileName(parent=self.parameters_triangulation_window,
                                               caption="???????????????? ???????? ????????????????????????",
                                               filter="JSON (*.json)")[0]
        if len(filename) > 0:
            loadTriangulationQuestion, buttonYes, _ = create_question(parent=self.parameters_triangulation_window,
                                                                      title="??????????????????????????",
                                                                      question=f'?????????????????? ????????????????????????\n"{filename}"?',
                                                                      text_btn1="????",
                                                                      text_btn2="??????")
            if loadTriangulationQuestion.clickedButton() == buttonYes:
                try:
                    self.triangulation = Triangulation(
                        filename=filename,
                        parameters_triangulation_window=self.parameters_triangulation_window)
                    self.show_parameters_diffusion_window()
                except Exception:
                    QMessageBox.critical(self.parameters_triangulation_window,
                                         "????????????", f'???????? "{filename}" ??????????????????')

    def get_indices_triangles_within_radius(self, index_triangle, radius):
        if isinstance(index_triangle, float):
            index_triangle = int(index_triangle)
        indices = {index_triangle}
        if radius > 0:
            for index_triangle_neighbour in self.triangulation.triangles[index_triangle].indices_neighbours:
                indices |= self.get_indices_triangles_within_radius(index_triangle=index_triangle_neighbour,
                                                                    radius=radius - 1)
        return indices

    def calculate_coefficient_diffusion(self, index_triangle):
        indices = self.get_indices_triangles_within_radius(
            index_triangle=index_triangle,
            radius=self.parameters_diffusion_window.averaging_radius_spinbox.value())
        count_contamination_triangle_within_radius = \
            sum([self.triangulation.triangles[index].contamination_level for index in indices])
        return count_contamination_triangle_within_radius / len(indices)

    def update_discrete_values(self):
        method = "smallest side" \
            if self.parameters_diffusion_window.choise_adjacent_triangle_smallest_side_radiobutton.isChecked() \
            else "equally probable"
        shuffle(self.current_queue_triangles)
        for index_triangle in list(filter(
                lambda index: not self.triangulation.is_immutable_triangle(index_triangle=index),
                self.current_queue_triangles)):
            current_triangle = self.triangulation.triangles[index_triangle]
            neighbours = [self.triangulation.triangles[index]
                          for index in self.triangulation.triangles[index_triangle].indices_neighbours]

            current_triangle.select_index_neighbour(method=method, neighbours=neighbours)
            if current_triangle.index_selected_neighbor == -1:
                if current_triangle.contamination_level == 1:
                    current_triangle.contamination_level = 0
            else:
                selected_neighbour_triangle = self.triangulation.triangles[current_triangle.index_selected_neighbor]
                current_triangle.contamination_level, selected_neighbour_triangle.contamination_level = \
                    selected_neighbour_triangle.contamination_level, current_triangle.contamination_level

    def update_float_values(self):
        indices_triangles = set()
        for index_triangle in list(filter(
                lambda index: self.triangulation.triangles[index].contamination_level > 0 or
                              self.triangulation.triangles[index].index_selected_neighbor is not None,
                self.current_queue_triangles
        )):
            indices_triangles |= self.get_indices_triangles_within_radius(
                index_triangle=index_triangle,
                radius=self.parameters_diffusion_window.averaging_radius_spinbox.value())
            if self.triangulation.triangles[index_triangle].index_selected_neighbor is not None:
                indices_triangles |= self.get_indices_triangles_within_radius(
                    index_triangle=self.triangulation.triangles[index_triangle].index_selected_neighbor,
                    radius=self.parameters_diffusion_window.averaging_radius_spinbox.value())
        for index_triangle in indices_triangles:
            self.triangulation.triangles[index_triangle].coefficient_diffusion = \
                self.calculate_coefficient_diffusion(index_triangle=index_triangle)

    def start(self):
        self.current_queue_triangles = np.arange(len(self.triangulation.triangles))
        # region Init diffusion discrete values
        radius = self.parameters_diffusion_window.initial_radius_of_contamination_spinbox.value()

        center_point_image = np.array(self.triangulation.map_height_image_shape) // 2

        index_center_triangle = list(
            filter(lambda pair: pair[1].check_contain_point(center_point_image[1], center_point_image[0]),
                   enumerate(self.triangulation.triangles)))[0][0]

        for index in self.get_indices_triangles_within_radius(index_triangle=index_center_triangle, radius=radius):
            if self.triangulation.triangles[index].contamination_level == 0:
                self.triangulation.triangles[index].contamination_level = 1
        # endregion

        # region Init diffusion float values
        if self.parameters_diffusion_window.calculate_averaged_values_checkbox.isChecked():
            self.update_float_values()
        # endregion
        self.show_simulation_diffusion_window()
