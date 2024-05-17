from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QSoundEffect
from game_window import MainWindow

import sys


class Ui_Dialog(object):
    def setupUi(self, Dialog: QDialog, main_window) -> None:
        self.main_window = main_window  # Keep a reference to the main window

        Dialog.setObjectName("Dialog")
        Dialog.resize(501, 390)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("../assets/pokeball.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        Dialog.setWindowIcon(icon)

        self.background_label = QLabel(Dialog)
        self.background_label.setGeometry(0, 0, 501, 390)
        self.background_label.setPixmap(QtGui.QPixmap("./assets/background_image.jpg"))
        self.background_label.setScaledContents(True)
        self.background_label.lower()

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(0, 270, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Close | QtWidgets.QDialogButtonBox.Yes
        )
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(
            self.openGameWindow
        )

    def openGameWindow(self) -> None:
        self.main_window.stopBackgroundMusic()  # Stop the background music
        self.game_window = MainWindow()
        self.game_window.show()


class MainLauncherWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self, self)  # Pass the reference of MainLauncherWindow
        self.initBackgroundMusic()
        self.setWindowTitle("Pokemon Python")  # Set the window title

    def initBackgroundMusic(self) -> None:
        self.background_music = QSoundEffect()
        self.background_music.setSource(
            QtCore.QUrl.fromLocalFile("./assets/sounds/launcher.wav")
        )
        self.background_music.setVolume(0.5)
        self.background_music.play()

    def stopBackgroundMusic(self) -> None:
        self.background_music.stop()  # Method to stop the background music


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainLauncherWindow()
    window.show()
    sys.exit(app.exec_())
