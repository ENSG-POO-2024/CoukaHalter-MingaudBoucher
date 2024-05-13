from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtMultimedia import QSoundEffect, QMediaPlayer, QMediaContent
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pokemon Python"))


class MainWindow(QMainWindow, Ui_MainWindow):
    MAP_FILE = "./assets/map.jpg"
    MOVE_AMOUNT = 4
    WALK_FRAMES = {
        "down": [f"./sprites/front/trainer/tile00{i}.png" for i in range(4)],
        "up": [f"./sprites/back/trainer/tile0{i}.png" for i in range(34, 38)],
        "left": [f"./sprites/front/trainer/tile0{i}.png" for i in range(68, 71)],
        "right": [f"./sprites/front/trainer/tile{i}.png" for i in range(102, 105)],
    }

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loadMap()
        self.loadCharacter()
        self.initSounds()
        self.initBackgroundMusic()
        self.window_x, self.window_y = 0, 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateWalk)
        self.current_frame = 0
        self.direction = ""
        self.is_walking = False

    def loadMap(self):
        self.map_pixmap = QtGui.QPixmap(self.MAP_FILE)
        self.map_label.setPixmap(self.map_pixmap)
        self.map_label.setScaledContents(True)
        self.map_width, self.map_height = (
            self.map_pixmap.width(),
            self.map_pixmap.height(),
        )

    def loadCharacter(self):
        character_image = QtGui.QPixmap("./sprites/front/trainer/tile102.png")
        self.character_label.setPixmap(character_image)
        self.character_label.setGeometry(self.centerCharacter(character_image))

    def centerCharacter(self, character_image):
        center_x = (self.window_size_x - character_image.width()) // 2
        center_y = (self.window_size_y - character_image.height()) // 2
        return QtCore.QRect(
            center_x, center_y, character_image.width(), character_image.height()
        )

    def initSounds(self):
        self.walk_sound = QSoundEffect()
        self.walk_sound.setSource(
            QtCore.QUrl.fromLocalFile("./assets/sounds/footsteps.wav")
        )
        self.walk_sound.setVolume(0.5)

    def initBackgroundMusic(self):
        self.background_music = QSoundEffect()
        self.background_music.setSource(
            QtCore.QUrl.fromLocalFile("./assets/sounds/background.wav")
        )
        self.background_music.setVolume(0.5)
        self.background_music.play()

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        if event.key() == QtCore.Qt.Key_Left:
            self.walkLeft()
        elif event.key() == QtCore.Qt.Key_Right:
            self.walkRight()
        elif event.key() == QtCore.Qt.Key_Up:
            self.walkUp()
        elif event.key() == QtCore.Qt.Key_Down:
            self.walkDown()

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        if event.key() in {
            QtCore.Qt.Key_Left,
            QtCore.Qt.Key_Right,
            QtCore.Qt.Key_Up,
            QtCore.Qt.Key_Down,
        }:
            self.stopWalking()

    def moveMap(self, dx, dy):
        self.window_x += dx
        self.window_y += dy
        self.window_x = max(0, min(self.window_x, self.map_width - self.window_size_x))
        self.window_y = max(0, min(self.window_y, self.map_height - self.window_size_y))
        self.updateMap()

    def moveCharacter(self, dx, dy):
        current_pos = self.character_label.pos()
        new_pos = QtCore.QPoint(current_pos.x() + dx, current_pos.y() + dy)
        if (0 <= new_pos.x() <= self.map_width - self.character_label.width()) and (
            0 <= new_pos.y() <= self.map_height - self.character_label.height()
        ):
            self.character_label.move(new_pos)

    def updateMap(self):
        cropped_pixmap = self.map_pixmap.copy(
            self.window_x, self.window_y, self.window_size_x, self.window_size_y
        )
        self.map_label.setPixmap(cropped_pixmap)

    def walk(self, direction):
        self.is_walking = True
        if (
            not self.walk_sound.isPlaying()
        ):  # Only play the sound if it's not already playing
            self.walk_sound.play()
        self.direction = direction
        self.walk_frames = self.WALK_FRAMES[direction]
        self.current_frame = 0
        self.timer.start(80)

    def stopWalking(self):
        self.is_walking = False
        self.timer.stop()
        self.walk_sound.stop()

    def updateWalk(self):
        if self.current_frame < len(self.walk_frames):
            frame_file = self.walk_frames[self.current_frame]
            frame = QtGui.QPixmap(frame_file)
            self.character_label.setPixmap(frame)
            dx, dy = {
                "down": (0, -self.MOVE_AMOUNT),
                "up": (0, self.MOVE_AMOUNT),
                "left": (self.MOVE_AMOUNT, 0),
                "right": (-self.MOVE_AMOUNT, 0),
            }[self.direction]
            self.moveCharacter(-dx, -dy)
            self.moveMap(-5 * dx, -5 * dy)
            self.current_frame += 1
        else:
            self.current_frame = 0

    def walkDown(self):
        self.walk("down")

    def walkUp(self):
        self.walk("up")

    def walkLeft(self):
        self.walk("left")

    def walkRight(self):
        self.walk("right")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
