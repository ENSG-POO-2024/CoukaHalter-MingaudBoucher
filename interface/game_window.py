# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 600)  # Set fixed size for the window
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.map_label = QtWidgets.QLabel(self.centralwidget)
        self.map_label.setGeometry(QtCore.QRect(0, 0, 800, 600))  # Set map size
        self.character_label = QtWidgets.QLabel(self.centralwidget)
        self.character_label.setGeometry(
            QtCore.QRect(400, 300, 20, 20)
        )  # Center of the screen
        self.character_label.setStyleSheet(
            "background-color: red; border-radius: 10px"
        )  # Character appearance
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pokemon Python"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.map_label.setPixmap(QtGui.QPixmap("./assets/map.jpg"))  # Set map image
        self.map_label.setScaledContents(True)  # Scale the image to fit the label

        self.map_width = 600  # Map width
        self.map_height = 400  # Map height
        self.character_width = 20  # Character width
        self.character_height = 20  # Character height

        self.window_width = self.map_width
        self.window_height = self.map_height

        self.center_character()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self.moveMap(10, 0)  # Move map left
        elif event.key() == QtCore.Qt.Key_Right:
            self.moveMap(-10, 0)  # Move map right
        elif event.key() == QtCore.Qt.Key_Up:
            self.moveMap(0, 10)  # Move map up
        elif event.key() == QtCore.Qt.Key_Down:
            self.moveMap(0, -10)  # Move map down

    def moveMap(self, dx, dy):
        new_map_x = self.map_label.x() + dx
        new_map_y = self.map_label.y() + dy
        new_character_x = self.character_label.x() - dx
        new_character_y = self.character_label.y() - dy

        # Adjust map position based on character movement
        if new_map_x < 0:
            new_map_x = 0
        elif new_map_x > self.map_width - self.window_width:
            new_map_x = self.map_width - self.window_width

        if new_map_y < 0:
            new_map_y = 0
        elif new_map_y > self.map_height - self.window_height:
            new_map_y = self.map_height - self.window_height

        self.map_label.move(new_map_x, new_map_y)
        self.character_label.move(new_character_x, new_character_y)

    def center_character(self):
        self.character_label.move(
            self.window_width // 2 - self.character_label.width() // 2,
            self.window_height // 2 - self.character_label.height() // 2,
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
