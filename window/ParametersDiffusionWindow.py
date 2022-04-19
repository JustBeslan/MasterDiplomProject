from ui.ui_ParametersDiffusionWindow import Ui_parameters_diffusion_mainwindow
from PyQt5.QtGui import QPixmap, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QColorDialog, QMessageBox


def choose_color(button):
    color = QColorDialog.getColor()
    if color.isValid():
        button.setStyleSheet('background: %s;' % (color.name()))


def set_color_icon_action(action, color, changing):
    if changing:
        color_dialog = QColorDialog()
        new_color = color_dialog.getColor()
        if new_color.isValid():
            color.setNamedColor(new_color.name())
    pixmap = QPixmap(20, 20)
    pixmap.fill(color)
    action.setIcon(QIcon(pixmap))


class ParametersDiffusionWindow(QMainWindow, Ui_parameters_diffusion_mainwindow):

    def __init__(self,
                 triangulation,
                 func_start_simulation_diffusion):
        # super(ParametersDiffusionWindow, self).__init__()
        # uic.loadUi('ui/ParametersDiffusionWindow.ui', self)
        super(ParametersDiffusionWindow, self).__init__(parameters_diffusion_mainwindow=self)
        self.setFixedSize(self.width(), self.height())

        # region Init properties
        self.triangulation = triangulation
        self.show_parameters_triangulation_action.triggered.connect(triangulation.show_parameters)
        # endregion

        # region Preparing menu

        # region Preparing change color actions
        self.color_demonstration_points = QColor(170, 80, 255)
        set_color_icon_action(action=self.change_color_points_action,
                              color=self.color_demonstration_points,
                              changing=False)
        self.change_color_points_action.triggered.connect(
            lambda: set_color_icon_action(action=self.change_color_points_action,
                                          color=self.color_demonstration_points,
                                          changing=True))

        self.color_demonstration_edges = QColor(255, 0, 0)
        set_color_icon_action(action=self.change_color_edges_action,
                              color=self.color_demonstration_edges,
                              changing=False)
        self.change_color_edges_action.triggered.connect(
            lambda: set_color_icon_action(action=self.change_color_edges_action,
                                          color=self.color_demonstration_edges,
                                          changing=True))

        self.color_demonstration_triangles = QColor(0, 255, 0)
        set_color_icon_action(action=self.change_color_triangles_action,
                              color=self.color_demonstration_triangles,
                              changing=False)
        self.change_color_triangles_action.triggered.connect(
            lambda: set_color_icon_action(action=self.change_color_triangles_action,
                                          color=self.color_demonstration_triangles,
                                          changing=True))
        # endregion

        # region Preparing show triangulation actions
        self.show_extract_points_action.triggered.connect(
            lambda: triangulation.show_points(color=self.color_demonstration_points.name())
        )
        self.show_2d_triangulation_action.triggered.connect(
            lambda: triangulation.show_2d(color=self.color_demonstration_edges.name())
        )

        def show_3d(mode):
            triangulation.show_3d(mode=mode,
                                  color_triangles=self.color_demonstration_triangles,
                                  color_edges=self.color_demonstration_edges.name())
        self.show_only_triangles_action.triggered.connect(
            lambda: show_3d(mode="only triangles")
        )
        self.show_only_edges_action.triggered.connect(
            lambda: show_3d(mode="only edges")
        )
        self.show_triangles_and_edges_action.triggered.connect(
            lambda: show_3d(mode="triangles and edges")
        )
        # endregion

        self.show_map_action.triggered.connect(triangulation.show_map_image_height)
        self.save_triangulation_action.triggered.connect(triangulation.save)
        self.start_simulation_diffusion_button.clicked.connect(func_start_simulation_diffusion)
        self.calculating_float_values_checkbox.stateChanged.connect(
            lambda: self.analyzing_radius_calculating_float_values_spinbox.setEnabled(
                self.calculating_float_values_checkbox.isChecked())
        )
        # endregion

    def show_parameters_diffusion(self):
        text = f"Начальный радиус загрязнения : <i><b>{self.initial_radius_of_contamination_spinbox.value()}</b></i><br>\n" \
               f"Метод выбора соседнего треугольника: <i><b>{'По наименьшей стороне' if self.choise_adjacent_triangle_smallest_side_radiobutton.isChecked() else 'Равновероятно'}</b></i><br>\n" \
               f"Переходить в вещественные значения: <i><b>{'Переходить' if self.calculating_float_values_checkbox.isChecked() else 'Не переходить'}</b></i><br>\n"
        if self.calculating_float_values_checkbox.isChecked():
            text += f"Анализируемый радиус для перехода в вещественные значения: <i><b>{self.analyzing_radius_calculating_float_values_spinbox.value()}</b></i><br>\n"
        QMessageBox.about(self, "Параметры диффузии", text)
