# TODO(To optimize and clean code)
import json

import cv2
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QWidget
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from model.Triangle import *
from window.ParametersTriangulationWindow import ParametersTriangulationWindow


class Triangulation:
    step = 0
    points = np.array([])
    triangles = np.array([])

    def __init__(self, **kwargs):
        if 'parameters_triangulation_window' in kwargs and \
                isinstance(kwargs['parameters_triangulation_window'], ParametersTriangulationWindow):
            self.parameters_triangulation_window = kwargs['parameters_triangulation_window']
            self.map_filename = self.parameters_triangulation_window.map_filename
            self.map_height_image = self.parameters_triangulation_window.map_height_image
            self.min_height = self.parameters_triangulation_window.min_height_spinbox.value()
            self.max_height = self.parameters_triangulation_window.max_height_spinbox.value()
            self.step_x = self.parameters_triangulation_window.step_x_spinbox.value()
            self.step_y = self.parameters_triangulation_window.step_y_spinbox.value()
            self.max_discrepancy = self.parameters_triangulation_window.max_discrepancy_spinbox.value()
        elif 'filename' in kwargs and \
                isinstance(kwargs['filename'], str):
            self.parameters_triangulation_window = QWidget()
            filename = kwargs['filename']
            with open(filename, "r") as reader:
                data = list(json.load(reader).values())
                try:
                    parameters_triangulation_json = data[0]
                    if len(parameters_triangulation_json) != 5:
                        raise Exception
                    if isinstance(parameters_triangulation_json["path to map of height"], str):
                        self.map_filename = parameters_triangulation_json["path to map of height"]
                    else:
                        raise Exception
                    try:
                        self.map_height_image = cv2.imdecode(np.fromfile(self.map_filename, dtype=np.uint8),
                                                             cv2.IMREAD_UNCHANGED)
                        if len(np.array(self.map_height_image).shape) == 3:
                            self.map_height_image = np.array(
                                cv2.cvtColor(src=self.map_height_image,
                                             code=cv2.COLOR_BGR2GRAY))
                    except FileNotFoundError:
                        self.map_height_image = None
                    if isinstance(parameters_triangulation_json["range of height"], str):
                        self.min_height, self.max_height = \
                            list(
                                map(int, parameters_triangulation_json["range of height"].split(' '))
                            )
                    else:
                        raise Exception
                    if isinstance(parameters_triangulation_json["step on the OX axis"], str):
                        self.step_x = int(parameters_triangulation_json["step on the OX axis"])
                    else:
                        raise Exception
                    if isinstance(parameters_triangulation_json["step on the OY axis"], str):
                        self.step_y = int(parameters_triangulation_json["step on the OY axis"])
                    else:
                        raise Exception
                    if isinstance(parameters_triangulation_json["maximum residual value"], str):
                        self.max_discrepancy = int(parameters_triangulation_json["maximum residual value"])
                    else:
                        raise Exception

                    for triangle in data[1:]:
                        try:
                            self.triangles = np.append(self.triangles, Triangle.get_object_from_str(triangle))
                            for node in self.triangles[-1].nodes:
                                if node not in self.points:
                                    self.points = np.append(self.points, node)
                        except:
                            raise Exception
                    QMessageBox.about(self.parameters_triangulation_window,
                                      "Сообщение", "Триангуляция успешно загружена")
                except:
                    raise Exception

    def is_immutable_triangle(self, index_triangle):
        if isinstance(index_triangle, float):
            index_triangle = int(index_triangle)
        return not list(
            filter(
                lambda index: self.triangles[int(index)].contamination_level != self.triangles[index_triangle].contamination_level,
                self.triangles[index_triangle].indices_neighbours
            ))

    def build(self, func_update_statusbar):
        func_update_statusbar(text="Извлечение точек...")

        # region Extract points
        def split_axis(right_border, step, max_discrepancy):
            taken_points = [i * step for i in range(int(right_border / step) + 1)]
            if abs(right_border - taken_points[-1]) < max_discrepancy:
                taken_points[-1] = right_border
            else:
                taken_points.append(right_border)
            return taken_points

        split_axes_x = split_axis(self.map_height_image.shape[1] - 1, self.step_x, self.max_discrepancy)
        split_axes_y = split_axis(self.map_height_image.shape[0] - 1, self.step_y, self.max_discrepancy)
        self.points = np.array(
            [[Point(x=x, y=y, z=self.map_height_image[y][x]) for x in split_axes_x] for y in split_axes_y])
        # endregion
        func_update_statusbar(text="Создание триангуляции на плоскости...")

        # region Create Triangles
        def add_neighbour(triangle1, triangle1_index, triangle2, triangle2_index):
            triangle1.indices_neighbours = np.append(triangle1.indices_neighbours, [triangle2_index])
            triangle2.indices_neighbours = np.append(triangle2.indices_neighbours, [triangle1_index])

        for i in range(self.points.shape[0] - 1):
            for j in range(self.points.shape[1] - 1):
                self.triangles = \
                    np.append(self.triangles,
                              [Triangle(np.array([self.points[i][j], self.points[i + 1][j], self.points[i][j + 1]])),
                               Triangle(
                                   np.array([self.points[i + 1][j + 1], self.points[i][j + 1], self.points[i + 1][j]]))]
                              )
                index_triangle1 = len(self.triangles) - 2
                index_triangle2 = len(self.triangles) - 1
                add_neighbour(triangle1=self.triangles[index_triangle1],
                              triangle1_index=index_triangle1,
                              triangle2=self.triangles[index_triangle2],
                              triangle2_index=index_triangle2)
                if j > 0:
                    index_triangle2 = index_triangle1 - 1
                    add_neighbour(triangle1=self.triangles[index_triangle1],
                                  triangle1_index=index_triangle1,
                                  triangle2=self.triangles[index_triangle2],
                                  triangle2_index=index_triangle2)
                if i > 0:
                    index_triangle2 = index_triangle1 - (2 * self.points.shape[1] - 3)
                    add_neighbour(triangle1=self.triangles[index_triangle1],
                                  triangle1_index=index_triangle1,
                                  triangle2=self.triangles[index_triangle2],
                                  triangle2_index=index_triangle2)
        # endregion
        func_update_statusbar(text="Переход в пространственную триангуляцию...")

        # region Transform to 3D triangulation
        heights = [int(round(self.min_height + x * (self.max_height - self.min_height) / 255)) for x in range(256)]
        for point in self.points.ravel():
            point.z = heights[point.z]
        # endregion

    def show_points(self, color):
        fig, ax = plt.subplots()
        plt.get_current_fig_manager().window.setWindowIcon(QIcon("ui/triangle.png"))
        plt.get_current_fig_manager().canvas.set_window_title("Выделенные точки")
        ax.set_title("Выделенные точки")
        for point in self.points.ravel():
            ax.scatter(point.x, point.y, c=color, s=4)
        plt.show()

    def show_2d(self, color):
        fig, ax = plt.subplots()
        plt.get_current_fig_manager().window.setWindowIcon(QIcon("ui/triangle.png"))
        plt.get_current_fig_manager().canvas.set_window_title("Триангуляция на плоскости")
        ax.set_title("Триангуляция на плоскости")
        max_x = max([node.x for node in np.ravel(self.points)])
        max_y = max([node.y for node in np.ravel(self.points)])
        for i, triangle in enumerate(self.triangles):
            if i % 2 == 0:
                plt.hlines(
                    y=triangle.nodes[0].y,
                    xmin=min(triangle.nodes[0].x, triangle.nodes[2].x),
                    xmax=max(triangle.nodes[0].x, triangle.nodes[2].x),
                    color=color)
                plt.vlines(
                    x=triangle.nodes[0].x,
                    ymin=min(triangle.nodes[0].y, triangle.nodes[1].y),
                    ymax=max(triangle.nodes[0].y, triangle.nodes[1].y),
                    color=color)
                min_x, max_x = min(triangle.nodes[1].x, triangle.nodes[2].x), max(triangle.nodes[1].x,
                                                                                  triangle.nodes[2].x)
                min_y, max_y = min(triangle.nodes[1].y, triangle.nodes[2].y), max(triangle.nodes[1].y,
                                                                                  triangle.nodes[2].y)
                plt.plot([min_x, max_x], [max_y, min_y], color=color)
            else:
                if triangle.nodes[0].y == max_y:
                    plt.hlines(
                        y=triangle.nodes[0].y,
                        xmin=min(triangle.nodes[0].x, triangle.nodes[2].x),
                        xmax=max(triangle.nodes[0].x, triangle.nodes[2].x),
                        color=color)
                if triangle.nodes[0].x == max_x:
                    plt.vlines(
                        x=triangle.nodes[0].x,
                        ymin=min(triangle.nodes[0].y, triangle.nodes[1].y),
                        ymax=max(triangle.nodes[0].y, triangle.nodes[1].y),
                        color=color)
        plt.show()

    def show_3d(self,
                mode,
                color_triangles,
                color_edges):
        color_all_triangles = np.empty(np.array(self.triangles).shape, dtype='U50')
        for i in range(len(self.triangles)):
            averageZ = 150 * max(abs(self.triangles[i].nodes[0].z), abs(self.triangles[i].nodes[1].z),
                                 abs(self.triangles[i].nodes[2].z)) / (self.max_height - self.min_height)
            color_all_triangles[i] = '#%02x%02x%02x' % (
                min(int(averageZ * 1.5), color_triangles.red()),
                min(int(averageZ * 1.5), color_triangles.green()),
                min(int(averageZ * 1.5), color_triangles.blue()))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.get_current_fig_manager().window.setWindowIcon(QIcon("ui/triangle.png"))
        plt.get_current_fig_manager().canvas.set_window_title(f"3D Триангуляция (режим: {mode})")
        ax.set_title(f"3D Триангуляция (режим: {mode})")
        Z = [point.z for point in np.ravel(self.points)]
        ax.set_xlim([0, max([point.x for point in np.ravel(self.points)])])
        ax.set_ylim([0, max([point.y for point in np.ravel(self.points)])])
        ax.set_zlim([min(Z), max(Z) * 2])
        triangles = []
        for triangle in self.triangles:
            triangles.append(
                ((triangle.nodes[0].x, triangle.nodes[0].y, triangle.nodes[0].z),
                 (triangle.nodes[1].x, triangle.nodes[1].y, triangle.nodes[1].z),
                 (triangle.nodes[2].x, triangle.nodes[2].y, triangle.nodes[2].z))
            )
        ax.add_collection3d(Poly3DCollection(verts=triangles,
                                             alpha=0.0 if mode == "only edges" else 1.0,
                                             edgecolors=color_edges if mode != "only triangles" else None,
                                             facecolors=color_all_triangles if mode != "only edges" else None))
        plt.show()

    def show_parameters(self):
        QMessageBox.about(self.parameters_triangulation_window, "Параметры триангуляции",
                          f"Абсолютный путь к файлу: <i><b>{self.map_filename}</b></i><br>\n"
                          f"Диапазон высот (в метрах): <i><b>{self.min_height} (м) - {self.max_height} (м)</b></i><br>\n"
                          f"Шаг по оси OX: <i><b>{self.step_x} пикселей</b></i><br>\n"
                          f"Шаг по оси OY: <i><b>{self.step_y} пикселей</b></i><br>\n")

    def show_map_image_height(self):
        if self.map_height_image is not None:
            cv2.namedWindow("The map of height", cv2.WINDOW_NORMAL)
            cv2.imshow("The map of height", self.map_height_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            QMessageBox.critical(self.parameters_triangulation_window,
                                 "Ошибка",
                                 f"Файла\n'{self.map_filename}'\nне существует!")

    def save(self):
        # region Serialize triangulation
        serialize_triangulation = {
            "parameters": {
                "path to map of height": self.parameters_triangulation_window.map_filename,
                "range of height": str(self.min_height) + " " + str(self.max_height),
                "step on the OX axis": str(self.step_x),
                "step on the OY axis": str(self.step_y),
                "maximum residual value": str(self.max_discrepancy),
            }
        }
        serialize_triangulation.update({"Triangle {0}".format(i): triangle.__dict__()
                                        for i, triangle in enumerate(self.triangles)})
        # endregion
        try:
            json_filename = QFileDialog.getSaveFileName(parent=self.parameters_triangulation_window,
                                                        caption="Сохранить триангуляцию как...",
                                                        filter="JSON Files (*.json)")[0]
            if json_filename is not None:
                with open(json_filename, "w") as file:
                    json.dump(obj=serialize_triangulation,
                              fp=file,
                              indent=4)
                QMessageBox.about(self.parameters_triangulation_window,
                                  "Сообщение",
                                  f"Триангуляция сохранена успешно в {json_filename}")
        except:
            QMessageBox.critical(self.parameters_triangulation_window,
                                 "Ошибка",
                                 "Ошибка при сохранениии триангуляции!")
