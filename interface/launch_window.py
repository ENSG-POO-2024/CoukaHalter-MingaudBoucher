from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QHBoxLayout,
)
from PyQt6.QtGui import QIcon, QPixmap
import sys
from game_window import GameWindow


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Pokemon Python Launcher")
        self.setWindowIcon(QIcon("./assets/pokeball.png"))
        self.setFixedHeight(500)
        self.setFixedWidth(500)

        label = QLabel(self)
        pixmap = QPixmap("./assets/launch.png")
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())

        play_button = QPushButton(self)
        play_button.setGeometry(200, 225, 100, 30)

        quit_button = QPushButton("Quit", self)
        quit_button.setStyleSheet("background-color: red;")
        quit_button.setGeometry(200, 275, 100, 30)
        quit_button.clicked.connect(self.close)

        play_button.raise_()
        quit_button.raise_()

    def openNewWindow(self):
        self.window = QWidget()
        self.ui = GameWindow()
        self.ui.setupUi(self.window)
        self.window.show()


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
