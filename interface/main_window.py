from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QSoundEffect, QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
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

        self.video_widget = QVideoWidget(Dialog)
        self.video_widget.setGeometry(QtCore.QRect(-20, -20, 571, 411))
        self.video_widget.setObjectName("video_widget")

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(0, 270, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Close | QtWidgets.QDialogButtonBox.Yes
        )
        self.buttonBox.setObjectName("buttonBox")

        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(150, 80, 201, 41))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(
            self.openGameWindow
        )

    def retranslateUi(self, Dialog: QDialog) -> None:
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Pokemon Python Launcher"))
        self.textEdit.setHtml(
            _translate(
                "Dialog",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:16pt; font-weight:600; color:#26a269;">Pokemon Python </span></p></body></html>',
            )
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
        self.initVideoBackground()
        self.initBackgroundMusic()

    def initVideoBackground(self) -> None:
        self.media_player = QMediaPlayer(self)
        video_path = QtCore.QUrl.fromLocalFile(
            "./assets/background_video.mp4"
        )  # Use an absolute path
        media_content = QMediaContent(video_path)
        self.media_player.setMedia(media_content)
        self.media_player.setVideoOutput(self.ui.video_widget)
        self.media_player.setVolume(0)  # Mute the video sound if needed
        self.media_player.play()

        # Error handling
        self.media_player.error.connect(self.handleMediaError)

    def handleMediaError(self, error: QMediaPlayer.Error) -> None:
        print(f"Media error occurred: {self.media_player.errorString()}")

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
