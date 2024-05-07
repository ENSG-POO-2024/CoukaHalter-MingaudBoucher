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


class GameWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Pokemon Python")


app = QApplication(sys.argv)
window = GameWindow()
window.show()
sys.exit(app.exec())
