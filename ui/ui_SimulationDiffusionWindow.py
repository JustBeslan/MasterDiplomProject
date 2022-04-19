# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SimulationDiffusionWindowQDCcMh.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_simulation_diffusion_mainwindow(object):
    def __init__(self, simulation_diffusion_mainwindow):
        if not simulation_diffusion_mainwindow.objectName():
            simulation_diffusion_mainwindow.setObjectName(u"simulation_diffusion_mainwindow")
        simulation_diffusion_mainwindow.resize(752, 824)
        icon = QIcon()
        icon.addFile(u"triangle.png", QSize(), QIcon.Normal, QIcon.Off)
        simulation_diffusion_mainwindow.setWindowIcon(icon)
        self.show_parameters_diffusion_action = QAction(simulation_diffusion_mainwindow)
        self.show_parameters_diffusion_action.setObjectName(u"show_parameters_diffusion_action")
        self.change_edges_color_action = QAction(simulation_diffusion_mainwindow)
        self.change_edges_color_action.setObjectName(u"change_edges_color_action")
        self.change_pure_triangles_action = QAction(simulation_diffusion_mainwindow)
        self.change_pure_triangles_action.setObjectName(u"change_pure_triangles_action")
        self.change_contamination_triangles_action = QAction(simulation_diffusion_mainwindow)
        self.change_contamination_triangles_action.setObjectName(u"change_contamination_triangles_action")
        self.simulation_diffusion_centralwidget = QWidget(simulation_diffusion_mainwindow)
        self.simulation_diffusion_centralwidget.setObjectName(u"simulation_diffusion_centralwidget")
        self.simulation_diffusion_groupbox = QGroupBox(self.simulation_diffusion_centralwidget)
        self.simulation_diffusion_groupbox.setObjectName(u"simulation_diffusion_groupbox")
        self.simulation_diffusion_groupbox.setGeometry(QRect(150, 610, 431, 141))
        self.next_step_button = QPushButton(self.simulation_diffusion_groupbox)
        self.next_step_button.setObjectName(u"next_step_button")
        self.next_step_button.setGeometry(QRect(270, 30, 141, 41))
        self.start_pause_button = QPushButton(self.simulation_diffusion_groupbox)
        self.start_pause_button.setObjectName(u"start_pause_button")
        self.start_pause_button.setGeometry(QRect(20, 30, 111, 41))
        self.stop_button = QPushButton(self.simulation_diffusion_groupbox)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setEnabled(False)
        self.stop_button.setGeometry(QRect(140, 30, 121, 41))
        self.go_to_step_label = QLabel(self.simulation_diffusion_groupbox)
        self.go_to_step_label.setObjectName(u"go_to_step_label")
        self.go_to_step_label.setGeometry(QRect(20, 80, 81, 41))
        self.go_to_step_spinbox = QSpinBox(self.simulation_diffusion_groupbox)
        self.go_to_step_spinbox.setObjectName(u"go_to_step_spinbox")
        self.go_to_step_spinbox.setGeometry(QRect(100, 80, 111, 41))
        self.go_to_step_spinbox.setMaximum(999999999)
        self.go_to_step_label_2 = QLabel(self.simulation_diffusion_groupbox)
        self.go_to_step_label_2.setObjectName(u"go_to_step_label_2")
        self.go_to_step_label_2.setGeometry(QRect(220, 80, 31, 41))
        self.go_to_step_button = QPushButton(self.simulation_diffusion_groupbox)
        self.go_to_step_button.setObjectName(u"go_to_step_button")
        self.go_to_step_button.setGeometry(QRect(260, 80, 141, 41))
        simulation_diffusion_mainwindow.setCentralWidget(self.simulation_diffusion_centralwidget)
        self.simulation_diffusion_menubar = QMenuBar(simulation_diffusion_mainwindow)
        self.simulation_diffusion_menubar.setObjectName(u"simulation_diffusion_menubar")
        self.simulation_diffusion_menubar.setGeometry(QRect(0, 0, 752, 26))
        self.diffusion_menu = QMenu(self.simulation_diffusion_menubar)
        self.diffusion_menu.setObjectName(u"diffusion_menu")
        simulation_diffusion_mainwindow.setMenuBar(self.simulation_diffusion_menubar)
        self.simulation_diffusion_statusbar = QStatusBar(simulation_diffusion_mainwindow)
        self.simulation_diffusion_statusbar.setObjectName(u"simulation_diffusion_statusbar")
        simulation_diffusion_mainwindow.setStatusBar(self.simulation_diffusion_statusbar)

        self.simulation_diffusion_menubar.addAction(self.diffusion_menu.menuAction())
        self.diffusion_menu.addAction(self.change_contamination_triangles_action)
        self.diffusion_menu.addAction(self.change_pure_triangles_action)
        self.diffusion_menu.addAction(self.change_edges_color_action)
        self.diffusion_menu.addSeparator()
        self.diffusion_menu.addAction(self.show_parameters_diffusion_action)

        self.retranslateUi(simulation_diffusion_mainwindow)

        QMetaObject.connectSlotsByName(simulation_diffusion_mainwindow)
    # setupUi

    def retranslateUi(self, simulation_diffusion_mainwindow):
        simulation_diffusion_mainwindow.setWindowTitle(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u041c\u043e\u0434\u0435\u043b\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u0438\u0444\u0444\u0443\u0437\u0438\u0438", None))
        self.show_parameters_diffusion_action.setText(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u0434\u0438\u0444\u0444\u0443\u0437\u0438\u0438", None))
#if QT_CONFIG(statustip)
        self.show_parameters_diffusion_action.setStatusTip(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u0434\u0438\u0444\u0444\u0443\u0437\u0438\u0438", None))
#endif // QT_CONFIG(statustip)
        self.change_edges_color_action.setText(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c \u0446\u0432\u0435\u0442 \u0440\u0435\u0431\u0435\u0440", None))
        self.change_pure_triangles_action.setText(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c \u0446\u0432\u0435\u0442 \u0447\u0438\u0441\u0442\u044b\u0445 \u0442\u0440\u0435\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432", None))
        self.change_contamination_triangles_action.setText(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c \u0446\u0432\u0435\u0442 \u0437\u0430\u0433\u0440\u044f\u0437\u043d\u0435\u043d\u043d\u044b\u0445 \u0442\u0440\u0435\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432", None))
        self.simulation_diffusion_groupbox.setTitle(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0434\u0438\u0444\u0444\u0443\u0437\u0438\u0435\u0439", None))
#if QT_CONFIG(statustip)
        self.next_step_button.setStatusTip(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u041f\u0435\u0440\u0435\u0439\u0442\u0438 \u043d\u0430 \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0438\u0439 \u0448\u0430\u0433", None))
#endif // QT_CONFIG(statustip)
        self.next_step_button.setText(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u0421\u043b\u0435\u0434\u0443\u044e\u0449\u0438\u0439 \u0448\u0430\u0433", None))
#if QT_CONFIG(shortcut)
        self.next_step_button.setShortcut(QCoreApplication.translate("simulation_diffusion_mainwindow", u"Right", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(statustip)
        self.start_pause_button.setStatusTip(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u043c\u043e\u0434\u0435\u043b\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u0438\u0444\u0444\u0443\u0437\u0438\u0438", None))
#endif // QT_CONFIG(statustip)
        self.start_pause_button.setText(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u0421\u0442\u0430\u0440\u0442", None))
#if QT_CONFIG(shortcut)
        self.start_pause_button.setShortcut(QCoreApplication.translate("simulation_diffusion_mainwindow", u"Ctrl+P", None))
#endif // QT_CONFIG(shortcut)
        self.stop_button.setText(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u0421\u0442\u043e\u043f", None))
#if QT_CONFIG(shortcut)
        self.stop_button.setShortcut(QCoreApplication.translate("simulation_diffusion_mainwindow", u"Esc", None))
#endif // QT_CONFIG(shortcut)
        self.go_to_step_label.setText(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u041f\u0435\u0440\u0435\u0439\u0442\u0438 \u043d\u0430", None))
        self.go_to_step_label_2.setText(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u0448\u0430\u0433", None))
#if QT_CONFIG(statustip)
        self.go_to_step_button.setStatusTip(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u041f\u0435\u0440\u0435\u0439\u0442\u0438 \u043d\u0430 \u0443\u043a\u0430\u0437\u0430\u043d\u043d\u044b\u0439 \u0448\u0430\u0433", None))
#endif // QT_CONFIG(statustip)
        self.go_to_step_button.setText(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u041f\u0435\u0440\u0435\u0439\u0442\u0438", None))
#if QT_CONFIG(shortcut)
        self.go_to_step_button.setShortcut(QCoreApplication.translate("simulation_diffusion_mainwindow", u"Right", None))
#endif // QT_CONFIG(shortcut)
        self.diffusion_menu.setTitle(QCoreApplication.translate("simulation_diffusion_mainwindow", u"\u0414\u0438\u0444\u0444\u0443\u0437\u0438\u044f", None))
    # retranslateUi

