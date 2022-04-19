import os.path
from ui.ui_ParametersTriangulationWindow import Ui_parameters_triangulation_mainwindow
import cv2
import numpy as np
# from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QMainWindow, QAction, QActionGroup
from History import History


def create_question(title, question, text_btn1, text_btn2):
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Question)
    message_box.setWindowTitle(title)
    message_box.setText(question)
    message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    message_box.setDefaultButton(QMessageBox.Yes)

    button_yes = message_box.button(QMessageBox.Yes)
    button_yes.setText(text_btn1)

    button_no = message_box.button(QMessageBox.No)
    button_no.setText(text_btn2)
    message_box.exec_()
    return message_box, button_yes, button_no


class ParametersTriangulationWindow(QMainWindow, Ui_parameters_triangulation_mainwindow):
    history = History(path_to_db_file="history.db")
    map_filename = ""
    map_height_image = None
    map_height_image_shape = None

    def __init__(self, func_load_triangulation, func_start_triangulation):
        # super(ParametersTriangulationWindow, self).__init__()
        # uic.loadUi('ui/ParametersTriangulationWindow.ui', self)
        super(ParametersTriangulationWindow, self).__init__(parameters_triangulation_mainwindow=self)
        self.setFixedSize(self.width(), self.height())
        self.choose_file_button.clicked.connect(self.choose_map_file)
        self.start_triangulation_button.clicked.connect(lambda: self.start_triangulation(func_start_triangulation))
        self.load_triangulation_action.triggered.connect(func_load_triangulation)
        self.load_history()

    def load_history(self):
        file_info_all = self.history.load()
        action_group = QActionGroup(self)
        if len(file_info_all) > 0:
            for file_info in file_info_all:
                action = QAction(f"{6 - file_info[0]}. {os.path.basename(file_info[1])}", self)
                action.setStatusTip(f"{file_info[1]} ({file_info[2]})")
                action_group.addAction(action)
                self.triangulation_menu.addAction(action)
            action_group.triggered.connect(self.load_parameters)

    def load_parameters(self, action):
        info = self.history.select_row_file_info(id_row=6 - int(action.text()[0]))
        load_parameters_question, button_yes, _ = create_question(
            title="Подтверждение",
            question=f"Вы желаете загрузить триангуляцию от {info[2]}\nдля файла {info[1]}?",
            text_btn1="Да",
            text_btn2="Нет")
        if load_parameters_question.clickedButton() == button_yes:
            parameters = self.history.select_row_triangle_parameters(id_row=info[0])
            self.min_height_spinbox.setValue(parameters[1])
            self.max_height_spinbox.setValue(parameters[2])
            self.step_x_spinbox.setValue(parameters[3])
            self.step_y_spinbox.setValue(parameters[4])
            self.max_discrepancy_spinbox.setValue(parameters[5])
            try:
                self.map_filename = info[1]
                self.load_map_height()
                self.update_statusbar("Параметры и изображение загружены")
            except FileNotFoundError:
                self.map_filename = ""
                QMessageBox.critical(self, "Ошибка", f"Файла\n\n{info[1]}\n\nне существует!")
                self.update_statusbar("Параметры загружены")

    def choose_map_file(self):
        self.map_filename = QFileDialog.getOpenFileName(parent=self,
                                                        caption='Выберите карту высот',
                                                        filter="Image (*.png *.jpg *.jpeg)")[0]
        if len(self.map_filename) > 0 and QMessageBox.question(self, "Подтверждение",
                                                               f"Загрузить файл\n{self.map_filename}?",
                                                               QMessageBox.Yes | QMessageBox.No,
                                                               QMessageBox.Yes) == QMessageBox.Yes:
            self.update_statusbar(text="Загрузка карты высот...")
            self.load_map_height()
            self.update_statusbar(text="Загрузка карты высот завершена")

    def load_map_height(self):
        self.map_height_image = cv2.imdecode(np.fromfile(self.map_filename, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        if len(np.array(self.map_height_image).shape) == 3:
            self.map_height_image = np.array(
                cv2.cvtColor(src=self.map_height_image,
                             code=cv2.COLOR_BGR2GRAY))
        self.map_height_image_shape = np.array(self.map_height_image).shape
        self.chosen_map_image.setPixmap(QtGui.QPixmap(self.map_filename))
        self.chosen_map_image.setToolTip(self.map_filename)
        self.chosen_map_image.setStatusTip(self.map_filename)

        if self.choose_file_button.text() == "Выбрать карту высот":
            self.choose_file_button.setText("Изменить карту высот")

    def update_statusbar(self, text):
        self.parameters_triangulation_statusbar.showMessage(text)
        self.parameters_triangulation_statusbar.repaint()

    def start_triangulation(self, func_start_triangulation):
        if len(self.map_filename) == 0:
            QMessageBox.critical(self, "Ошибка", "Загрузите файл!")
        elif self.min_height_spinbox.value() >= self.max_height_spinbox.value():
            QMessageBox.critical(self, "Ошибка", "Минимальная высота должна быть больше меньше максимальной высоты")
        else:
            self.history.update(map_filename=self.map_filename,
                                min_height=self.min_height_spinbox.value(), max_height=self.max_height_spinbox.value(),
                                step_x=self.step_x_spinbox.value(), step_y=self.step_y_spinbox.value(),
                                max_discrepancy=self.max_discrepancy_spinbox.value())
            func_start_triangulation(func_update_statusbar=self.update_statusbar)
