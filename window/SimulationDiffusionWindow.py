import matplotlib.colors
import numpy as np
from ui.ui_SimulationDiffusionWindow import Ui_simulation_diffusion_mainwindow
# from PyQt5 import uic
from PyQt5.QtGui import QColor, QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QColorDialog
from matplotlib import pyplot as plt, animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def set_color_icon_action(action,
                          color,
                          changing):
    if changing:
        color_dialog = QColorDialog()
        color_dialog.setOption(QColorDialog.ShowAlphaChannel, on=True)
        new_color = color_dialog.getColor()
        if new_color.isValid():
            color.setNamedColor(new_color.name())
    pixmap = QPixmap(20, 20)
    pixmap.fill(color)
    action.setIcon(QIcon(pixmap))


class PlotCanvas(FigureCanvas):
    poly_3d_collection_discrete_values = None
    poly_3d_collection_float_values = None
    face_colors_discrete_values = None
    face_colors_float_values = None

    def __init__(self,
                 triangles,
                 lims,
                 edge_colors,
                 start_face_colors_discrete_values,
                 start_face_colors_float_values=None,
                 parent=None,
                 figure_size=(19, 8),
                 dpi=100):
        self.face_colors_discrete_values = start_face_colors_discrete_values
        # region Init Figure
        if start_face_colors_float_values is not None:
            self.fig, (self.axes_discrete_values,
                       self.axes_float_values) = plt.subplots(nrows=1, ncols=2,
                                                              subplot_kw={'projection': '3d'},
                                                              figsize=figure_size,
                                                              dpi=dpi)
            self.face_colors_float_values = start_face_colors_float_values
        else:
            self.fig = Figure(figsize=figure_size, dpi=dpi)
            self.axes_discrete_values = self.fig.add_subplot(111, projection='3d')

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # endregion

        # region Build Triangulation (Discrete Values)
        self.poly_3d_collection_discrete_values = Poly3DCollection(verts=triangles,
                                                                   linewidth=0.1,
                                                                   edgecolors=edge_colors,
                                                                   facecolors=start_face_colors_discrete_values,
                                                                   rasterized=True)
        self.axes_discrete_values.add_collection3d(self.poly_3d_collection_discrete_values)

        self.axes_discrete_values.set_xlim(lims[0])
        self.axes_discrete_values.set_ylim(lims[1])
        self.axes_discrete_values.set_zlim(lims[2])

        self.axes_discrete_values.set_title('Моделирование диффузии\nШаг 0')
        # endregion

        # region Build Triangulation (Float Values)
        if start_face_colors_float_values is not None:
            self.poly_3d_collection_float_values = Poly3DCollection(verts=triangles,
                                                                    linewidth=0.1,
                                                                    edgecolors=edge_colors,
                                                                    facecolors=start_face_colors_float_values,
                                                                    rasterized=True)
            self.axes_float_values.add_collection3d(self.poly_3d_collection_float_values)

            self.axes_float_values.set_xlim(lims[0])
            self.axes_float_values.set_ylim(lims[1])
            self.axes_float_values.set_zlim(lims[2])

            self.axes_float_values.set_title('Моделирование диффузии (в вещественных числах)\nШаг 0')
        # endregion

        plt.ion()
        self.draw()

    def update_canvas(self,
                      new_face_colors_discrete_values,
                      new_face_colors_float_values=None):
        self.face_colors_discrete_values = new_face_colors_discrete_values
        self.poly_3d_collection_discrete_values.set_facecolor(new_face_colors_discrete_values)
        if new_face_colors_float_values is not None:
            self.face_colors_float_values = new_face_colors_float_values
            self.poly_3d_collection_float_values.set_facecolor(new_face_colors_float_values)
        self.draw()


class SimulationDiffusionWindow(QMainWindow, Ui_simulation_diffusion_mainwindow):
    start_face_colors_discrete_values = None
    start_face_colors_float_values = None
    current_face_colors_discrete_values = None
    current_face_colors_float_values = None
    face_color_contamination_triangle = None
    triangulation = None
    parameters_diffusion = None

    def __init__(self,
                 parameters_diffusion,
                 func_update_discrete_values,
                 func_update_float_values,
                 triangulation):
        # super(SimulationDiffusionWindow, self).__init__()
        # uic.loadUi('ui/SimulationDiffusionWindow.ui', self)
        super(SimulationDiffusionWindow, self).__init__(simulation_diffusion_mainwindow = self)

        # region Init properties
        self.triangulation = triangulation
        self.func_update_discrete_values = func_update_discrete_values
        self.func_update_float_values = func_update_float_values
        self.parameters_diffusion = parameters_diffusion
        # endregion

        # region Preparing the menu
        self.face_color_contamination_triangle = QColor(0, 0, 255)
        set_color_icon_action(action=self.change_contamination_triangles_action,
                              color=self.face_color_contamination_triangle,
                              changing=False)
        self.change_contamination_triangles_action.triggered.connect(
            lambda: self.update_colors(action=self.change_contamination_triangles_action,
                                       color=self.face_color_contamination_triangle,
                                       changing=True))

        self.face_color_pure_triangle = QColor(255, 255, 255)
        set_color_icon_action(action=self.change_pure_triangles_action,
                              color=self.face_color_pure_triangle,
                              changing=False)
        self.change_pure_triangles_action.triggered.connect(
            lambda: self.update_colors(action=self.change_pure_triangles_action,
                                       color=self.face_color_pure_triangle,
                                       changing=True))
        self.edges_color = QColor(255, 0, 0)
        set_color_icon_action(action=self.change_edges_color_action,
                              color=self.edges_color,
                              changing=False)
        self.change_edges_color_action.triggered.connect(
            lambda: self.update_colors(action=self.change_edges_color_action,
                                       color=self.edges_color,
                                       changing=True))
        self.show_parameters_diffusion_action.triggered.connect(self.parameters_diffusion.show_parameters_diffusion)
        # endregion

        # region Init Graphic Diffusion
        self.start_characteristics = np.array(
            [(triangle.contamination_level, triangle.coefficient_diffusion)
             for triangle in self.triangulation.triangles])
        self.current_face_colors_discrete_values = np.array([
            self.face_color_contamination_triangle.name()
            if triangle.contamination_level > 0 else self.face_color_pure_triangle.name()
            for triangle in self.triangulation.triangles
        ])

        if self.parameters_diffusion.calculate_averaged_values_checkbox.isChecked():
            face_color_contamination_triangle_rgba = np.array(self.face_color_contamination_triangle.getRgb()) / 255
            self.current_face_colors_float_values = np.array([matplotlib.colors.to_hex(
                c=[face_color_contamination_triangle_rgba[0],
                   face_color_contamination_triangle_rgba[1],
                   face_color_contamination_triangle_rgba[2],
                   triangle.coefficient_diffusion],
                keep_alpha=True) for triangle in self.triangulation.triangles])

        triangles = []
        max_points_x, max_points_y, min_points_z, max_points_z = None, None, None, None
        for triangle in self.triangulation.triangles:
            max_points_x = np.max([triangle.nodes[0].x, triangle.nodes[1].x, triangle.nodes[2].x]
                                  if max_points_x is None else
                                  [triangle.nodes[0].x, triangle.nodes[1].x, triangle.nodes[2].x, max_points_x])
            max_points_y = np.max([triangle.nodes[0].y, triangle.nodes[1].y, triangle.nodes[2].y]
                                  if max_points_y is None else
                                  [triangle.nodes[0].y, triangle.nodes[1].y, triangle.nodes[2].y, max_points_y])
            max_points_z = np.max([triangle.nodes[0].z, triangle.nodes[1].z, triangle.nodes[2].z]
                                  if max_points_z is None else
                                  [triangle.nodes[0].z, triangle.nodes[1].z, triangle.nodes[2].z, max_points_z])
            min_points_z = np.min([triangle.nodes[0].z, triangle.nodes[1].z, triangle.nodes[2].z]
                                  if min_points_z is None else
                                  [triangle.nodes[0].z, triangle.nodes[1].z, triangle.nodes[2].z, min_points_z])
            triangles.append(((triangle.nodes[0].x, triangle.nodes[0].y, triangle.nodes[0].z),
                              (triangle.nodes[1].x, triangle.nodes[1].y, triangle.nodes[1].z),
                              (triangle.nodes[2].x, triangle.nodes[2].y, triangle.nodes[2].z)))
        self.plot_canvas = PlotCanvas(
            triangles=triangles,
            edge_colors=self.edges_color.name(),
            start_face_colors_discrete_values=self.current_face_colors_discrete_values,
            start_face_colors_float_values=self.current_face_colors_float_values,
            lims=[[0, max_points_x], [0, max_points_y], [min_points_z, max_points_z * 2]],
            parent=self)
        self.plot_canvas.move(10, 30)
        # endregion

        # region Preparing the elements
        self.simulation_diffusion_groupbox.move(
            (self.width() - self.simulation_diffusion_groupbox.width()) // 2,
            self.height() - self.simulation_diffusion_groupbox.height() - 50
        )
        self.next_step_button.clicked.connect(self.next_step_button_clicked)
        self.start_pause_button.clicked.connect(self.start_pause_button_clicked)
        self.stop_button.clicked.connect(self.stop_button_clicked)
        self.go_to_step_button.clicked.connect(self.go_to_step_button_clicked)
        self.go_to_step_spinbox.valueChanged.connect(
            lambda: self.go_to_step_button.setStatusTip(f"Перейти на {self.go_to_step_spinbox.value()} шаг"))

        self.animation = animation.FuncAnimation(fig=self.plot_canvas.fig,
                                                 func=self.animation_func,
                                                 interval=100)
        # endregion

    def update_colors(self,
                      action,
                      color,
                      changing):
        set_color_icon_action(action=action,
                              color=color,
                              changing=changing)
        if changing:
            if action == self.change_edges_color_action:
                self.plot_canvas.poly_3d_collection_discrete_values.set_edgecolor(self.edges_color.name())
                if self.plot_canvas.poly_3d_collection_float_values is not None:
                    self.plot_canvas.poly_3d_collection_float_values.set_edgecolor(self.edges_color.name())
                self.plot_canvas.draw()
            else:
                self.update_face_colors_discrete_values()
                if self.plot_canvas.poly_3d_collection_float_values is not None:
                    self.update_face_colors_float_values()
                self.plot_canvas.update_canvas(new_face_colors_discrete_values=self.current_face_colors_discrete_values,
                                               new_face_colors_float_values=self.current_face_colors_float_values)

    def update_face_colors_discrete_values(self):
        self.current_face_colors_discrete_values = np.array([
            self.face_color_contamination_triangle.name()
            if triangle.contamination_level > 0 else self.face_color_pure_triangle.name()
            for triangle in self.triangulation.triangles
        ])

    def update_face_colors_float_values(self):
        self.current_face_colors_float_values = np.array([
            matplotlib.colors.to_hex([self.face_color_contamination_triangle.red() / 255,
                                      self.face_color_contamination_triangle.green() / 255,
                                      self.face_color_contamination_triangle.blue() / 255,
                                      triangle.coefficient_diffusion], True)
            for triangle in self.triangulation.triangles
        ])

    def update_canvas(self, update_values=True):
        self.update_face_colors_discrete_values()
        if update_values:
            self.func_update_discrete_values()
        if self.current_face_colors_float_values is not None:
            if update_values:
                self.func_update_float_values()
            self.update_face_colors_float_values()
        self.plot_canvas.update_canvas(new_face_colors_discrete_values=self.current_face_colors_discrete_values,
                                       new_face_colors_float_values=self.current_face_colors_float_values)
        self.go_to_step_spinbox.setMinimum(self.triangulation.step)
        self.go_to_step_spinbox.setValue(self.triangulation.step)
        self.plot_canvas.axes_discrete_values.set_title(f'Моделирование диффузии\nШаг {self.triangulation.step}')
        if self.current_face_colors_float_values is not None:
            self.plot_canvas.axes_float_values.set_title(
                f'Моделирование диффузии (в вещественных числах)\nШаг {self.triangulation.step}')

    def animation_func(self, i):
        if i == 0:
            self.animation.pause()
        else:
            self.triangulation.step += 1
            self.update_canvas()
        return self.plot_canvas.poly_3d_collection_discrete_values,

    def start_pause_button_clicked(self):
        if self.start_pause_button.text() == "Старт" or self.start_pause_button.text() == "Продолжить":
            self.start_pause_button.setText("Пауза")
            self.start_pause_button.setStatusTip("Приостановить моделирование диффузии")
            self.stop_button.setEnabled(True)
            self.stop_button.setStatusTip("Сбросить дифузию к начальному состоянию")
            self.next_step_button.setEnabled(False)
            self.next_step_button.setStatusTip("")
            self.animation.resume()
        elif self.start_pause_button.text() == "Пауза":
            self.start_pause_button.setText("Продолжить")
            self.start_pause_button.setStatusTip("Запустить моделирование диффузии")
            self.next_step_button.setEnabled(True)
            self.next_step_button.setStatusTip("Перейти на следующий шаг")
            self.animation.pause()

    def stop_button_clicked(self):
        self.stop_button.setEnabled(False)
        self.stop_button.setStatusTip("")
        self.start_pause_button.setText("Старт")
        self.next_step_button.setEnabled(True)
        self.next_step_button.setStatusTip("Перейти на следующий шаг")
        self.animation.pause()
        self.triangulation.step = 0
        for i in range(len(self.triangulation.triangles)):
            self.triangulation.triangles[i].contamination_level = self.start_characteristics[i][0]
            self.triangulation.triangles[i].coefficient_diffusion = self.start_characteristics[i][1]
        self.update_canvas(update_values=False)

    def next_step_button_clicked(self):
        self.triangulation.step += 1
        self.update_canvas()
        self.stop_button.setEnabled(True)
        self.stop_button.setStatusTip("Сбросить дифузию к начальному состоянию")

    def go_to_step_button_clicked(self):
        new_step = self.go_to_step_spinbox.value()
        for i in range(1, new_step - self.triangulation.step + 1):
            self.update_statusbar(text=f"Вычисляется шаг {self.triangulation.step + i}")
            self.func_update_discrete_values()
            if self.current_face_colors_float_values is not None:
                self.func_update_float_values()
        self.update_statusbar(text=f"Отображение {new_step} шага")
        self.triangulation.step = new_step
        self.update_canvas(update_values=False)

    def update_statusbar(self, text):
        self.simulation_diffusion_statusbar.showMessage(text)
        self.simulation_diffusion_statusbar.repaint()

    def resizeEvent(self, a0):
        self.plot_canvas.resize(self.width() - 10, self.height() - self.simulation_diffusion_groupbox.height() - 100)
        self.simulation_diffusion_groupbox.move(
            (self.width() - self.simulation_diffusion_groupbox.width()) // 2,
            self.height() - self.simulation_diffusion_groupbox.height() - 50
        )
        self.simulation_diffusion_groupbox.repaint()
