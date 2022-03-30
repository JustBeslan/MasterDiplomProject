# TODO(To optimize and clean code)
import os.path
import cv2
import sqlite3
import numpy as np
from datetime import datetime

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QMainWindow, QAction, QActionGroup


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


class ParametersTriangulationWindow(QMainWindow):
    conn = sqlite3.connect("history.db")
    map_filename = ""
    map_height_image = None

    def __init__(self, func_load_triangulation, func_start_triangulation):
        super(ParametersTriangulationWindow, self).__init__()
        uic.loadUi('ui/ParametersTriangulationWindow.ui', self)
        self.setFixedSize(self.width(), self.height())
        self.choose_file_button.clicked.connect(self.choose_map_file)
        self.start_triangulation_button.clicked.connect(lambda: self.start_triangulation(func_start_triangulation))
        self.load_triangulation_action.triggered.connect(func_load_triangulation)
        self.db_load()

    def db_load(self):
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS file_info
                            (id INTEGER PRIMARY KEY,
                            path TEXT,
                            date_of_use TEXT)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS triangle_parameters
                            (file_id INTEGER NOT NULL REFERENCES file_info(id), 
                            min_height INTEGER, max_height INTEGER,
                            step_x INTEGER, step_y INTEGER,
                            max_discrepancy INTEGER)""")
        self.conn.commit()
        cursor.execute("SELECT * FROM file_info ORDER BY id DESC")
        file_info_all = cursor.fetchall()
        self.action_group = QActionGroup(self)
        if len(file_info_all) > 0:
            for file_info in file_info_all:
                action = QAction(f"{6 - file_info[0]}. {os.path.basename(file_info[1])}", self)
                action.setStatusTip(f"{file_info[1]} ({file_info[2]})")
                self.action_group.addAction(action)
                self.triangulation_menu.addAction(action)
            self.action_group.triggered.connect(self.load_parameters)

    def update_history(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(id) FROM file_info")
        row_count = cursor.fetchone()[0]
        cursor.execute(f"""INSERT INTO file_info VALUES (?,?,?);""",
                       (row_count + 1,
                        self.map_filename,
                        datetime.today().strftime('%d.%m.%Y %H:%M')))
        cursor.execute(f"""INSERT INTO triangle_parameters VALUES (?,?,?,?,?,?);""",
                       (row_count + 1,
                        self.min_height_spinbox.value(),
                        self.max_height_spinbox.value(),
                        self.step_x_spinbox.value(),
                        self.step_y_spinbox.value(),
                        self.max_discrepancy_spinbox.value()))
        self.conn.commit()
        if row_count == 5:
            cursor.execute(f"""DELETE FROM triangle_parameters WHERE file_id = ?""", (1,))
            cursor.execute(f"""DELETE FROM file_info WHERE id = ?""", (1,))
            cursor.execute(f"""UPDATE triangle_parameters SET file_id = file_id-1""")
            cursor.execute(f"""UPDATE file_info SET id = id-1""")
            self.conn.commit()

    def load_parameters(self, action):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM file_info WHERE id=?", (int(action.text()[0]),))
        info = cursor.fetchone()
        load_parameters_question, button_yes, _ = create_question(
            title="Подтверждение",
            question=f"Вы желаете загрузить триангуляцию от {info[2]}\nдля файла {info[1]}?",
            text_btn1="Да",
            text_btn2="Нет")
        if load_parameters_question.clickedButton() == button_yes:
            cursor.execute("SELECT * FROM triangle_parameters WHERE file_id=?", (info[0],))
            parameters = cursor.fetchone()
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
            self.update_history()
            func_start_triangulation(func_update_statusbar=self.update_statusbar)
