# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.window_size_x = 800
        self.window_size_y = 600
        MainWindow.setFixedSize(self.window_size_x, self.window_size_y)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.map_label = QtWidgets.QLabel(self.centralwidget)
        self.map_label.setGeometry(
            QtCore.QRect(0, 0, self.window_size_x, self.window_size_y)
        )
        self.character_label = QtWidgets.QLabel(self.centralwidget)
        self.character_label.setGeometry(
            QtCore.QRect(390, 290, 20, 20)
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
        self.map_pixmap = QtGui.QPixmap("./assets/map.jpg")
        self.map_label.setPixmap(self.map_pixmap)
        self.map_label.setScaledContents(True)

        self.map_width = self.map_pixmap.width()
        self.map_height = self.map_pixmap.height()

        # Initial window size and position
        self.window_width = 400
        self.window_height = 300
        self.window_x = 0
        self.window_y = 0

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self.moveMap(-10, 0)
        elif event.key() == QtCore.Qt.Key_Right:
            self.moveMap(10, 0)
        elif event.key() == QtCore.Qt.Key_Up:
            self.moveMap(0, -10)
        elif event.key() == QtCore.Qt.Key_Down:
            self.moveMap(0, 10)

    def moveMap(self, dx, dy):
        self.window_x += dx
        self.window_y += dy

        if self.window_x < 0:
            self.window_x = 0
            self.moveCharacter(-10, 0)

        elif self.window_x > self.map_width - self.window_width:
            self.window_x = self.map_width - self.window_width
            self.moveCharacter(10, 0)

        if self.window_y < 0:
            self.window_y = 0
            self.moveCharacter(0, -10)

        elif self.window_y > self.map_height - self.window_height:
            self.window_y = self.map_height - self.window_height
            self.moveCharacter(0, 10)

        self.updateMap()

    def moveCharacter(self, dx, dy):
        current_pos = self.character_label.pos()

        new_pos = QtCore.QPoint(current_pos.x() + dx, current_pos.y() + dy)

        print(self.character_label.pos())
        if (
            current_pos.x() + dx <= 0
            or current_pos.y() + dy <= 0
            or current_pos.x() + dx >= self.window_size_x
            or current_pos.y() + dy >= self.window_size_y - 20
        ):
            pass
        else:
            self.character_label.move(new_pos)

    def updateMap(self):
        cropped_pixmap = self.map_pixmap.copy(
            self.window_x, self.window_y, self.window_width, self.window_height
        )
        self.map_label.setPixmap(cropped_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
