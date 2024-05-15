from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtMultimedia import QSoundEffect
import sys
import random
import math


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QMainWindow) -> None:
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

    def retranslateUi(self, MainWindow: QMainWindow) -> None:
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pokemon Python"))


class PointWindow(QMainWindow):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__()
        self.main_window = main_window
        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle("Combat")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(50, 50, 200, 200)
        self.label.setText("You are near a point!")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.main_window.resumeBackgroundMusic()
        super().closeEvent(event)


class MainWindow(QMainWindow, Ui_MainWindow):
    MAP_FILE = "./assets/map.jpg"
    MOVE_AMOUNT = 10
    WALK_FRAMES = {
        "down": [f"./sprites/front/trainer/tile00{i}.png" for i in range(4)],
        "up": [f"./sprites/back/trainer/tile0{i}.png" for i in range(34, 38)],
        "left": [f"./sprites/front/trainer/tile0{i}.png" for i in range(68, 71)],
        "right": [f"./sprites/front/trainer/tile{i}.png" for i in range(102, 105)],
    }

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.loadMap()
        self.loadCharacter()
        self.initSounds()
        self.initBackgroundMusic()
        self.window_x, self.window_y = 0, 0
        self.character_x, self.character_y = (
            self.window_size_x - self.character_label.width()
        ) // 2, (self.window_size_y - self.character_label.height()) // 2
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateWalk)
        self.current_frame = 0
        self.direction = ""
        self.is_walking = False
        self.points = []
        self.point_windows = []
        self.generateRandomPoints()

    def loadMap(self) -> None:
        self.map_pixmap = QtGui.QPixmap(self.MAP_FILE)
        self.map_label.setPixmap(self.map_pixmap)
        self.map_label.setScaledContents(True)
        self.map_width, self.map_height = (
            self.map_pixmap.width(),
            self.map_pixmap.height(),
        )

    def loadCharacter(self) -> None:
        character_image = QtGui.QPixmap("./sprites/front/trainer/tile102.png")
        self.character_label.setPixmap(character_image)
        self.character_label.setGeometry(self.centerCharacter(character_image))

    def centerCharacter(self, character_image: QtGui.QPixmap) -> QtCore.QRect:
        center_x = (self.window_size_x - character_image.width()) // 2
        center_y = (self.window_size_y - character_image.height()) // 2
        return QtCore.QRect(
            center_x, center_y, character_image.width(), character_image.height()
        )

    def initSounds(self) -> None:
        self.walk_sound = QSoundEffect()
        self.walk_sound.setSource(
            QtCore.QUrl.fromLocalFile("./assets/sounds/footsteps.wav")
        )
        self.walk_sound.setVolume(0.5)

    def initBackgroundMusic(self) -> None:
        self.background_music = QSoundEffect()
        self.background_music.setSource(
            QtCore.QUrl.fromLocalFile("./assets/sounds/background.wav")
        )
        self.background_music.setLoopCount(QSoundEffect.Infinite)
        self.background_music.setVolume(0.5)
        self.background_music.play()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
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

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.isAutoRepeat():
            return
        if event.key() in {
            QtCore.Qt.Key_Left,
            QtCore.Qt.Key_Right,
            QtCore.Qt.Key_Up,
            QtCore.Qt.Key_Down,
        }:
            self.stopWalking()

    def moveMap(self, dx: int, dy: int) -> None:
        self.window_x += dx
        self.window_y += dy
        self.window_x = max(0, min(self.window_x, self.map_width - self.window_size_x))
        self.window_y = max(0, min(self.window_y, self.map_height - self.window_size_y))
        self.updateMap()
        self.updatePoints()

    def moveCharacter(self, dx: int, dy: int) -> None:
        new_x = self.character_x + dx
        new_y = self.character_y + dy
        new_x = max(0, min(new_x, self.map_width - self.character_label.width()))
        new_y = max(0, min(new_y, self.map_height - self.character_label.height()))
        self.character_x = new_x
        self.character_y = new_y
        self.character_label.move(
            self.character_x - self.window_x, self.character_y - self.window_y
        )

    def updateMap(self) -> None:
        cropped_pixmap = self.map_pixmap.copy(
            self.window_x, self.window_y, self.window_size_x, self.window_size_y
        )
        self.map_label.setPixmap(cropped_pixmap)

    def walk(self, direction: str) -> None:
        self.is_walking = True
        if not self.walk_sound.isPlaying():
            self.walk_sound.play()
        self.direction = direction
        self.walk_frames = self.WALK_FRAMES[direction]
        self.current_frame = 0
        self.timer.start(80)
        print(self.character_x, self.character_y)

    def stopWalking(self) -> None:
        self.is_walking = False
        self.timer.stop()
        self.walk_sound.stop()

    def updateWalk(self) -> None:
        if self.current_frame < len(self.walk_frames):
            frame_file = self.walk_frames[self.current_frame]
            frame = QtGui.QPixmap(frame_file)
            self.character_label.setPixmap(frame)
            dx, dy = {
                "down": (0, self.MOVE_AMOUNT),
                "up": (0, -self.MOVE_AMOUNT),
                "left": (-self.MOVE_AMOUNT, 0),
                "right": (self.MOVE_AMOUNT, 0),
            }[self.direction]
            self.moveCharacter(dx, dy)
            self.moveMap(dx, dy)
            self.current_frame += 1
        else:
            self.current_frame = 0

    def walkDown(self) -> None:
        self.walk("down")

    def walkUp(self) -> None:
        self.walk("up")

    def walkLeft(self) -> None:
        self.walk("left")

    def walkRight(self) -> None:
        self.walk("right")

    def generateRandomPoints(self) -> None:
        for _ in range(10):
            map_x = random.randint(0, self.map_width - 20)
            map_y = random.randint(0, self.map_height - 20)
            window_x = map_x - self.window_x
            window_y = map_y - self.window_y
            point_label = QtWidgets.QLabel(self.centralwidget)
            point_label.setGeometry(window_x, window_y, 20, 20)
            point_label.setStyleSheet("background-color: red; border-radius: 10px;")
            point_label.show()
            self.points.append((map_x, map_y, point_label))
            print(self.map_width, self.map_height)

    def distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def updatePoints(self) -> None:
        character_center_x = self.character_x + self.character_label.width() / 2
        character_center_y = self.character_y + self.character_label.height() / 2

        for idx, (map_x, map_y, point_label) in enumerate(self.points):
            point_label.move(map_x - self.window_x, map_y - self.window_y)
            distance_to_point = self.distance(
                character_center_x, character_center_y, map_x, map_y
            )

            if distance_to_point < 100:
                print(f"Character is near point {idx + 1}")
                if idx not in self.point_windows:
                    self.point_windows.append(idx)
                    point_label.hide()
                    self.openPointWindow()

    def openPointWindow(self) -> None:
        self.background_music.stop()
        self.combat_music = QSoundEffect()
        self.combat_music.setSource(
            QtCore.QUrl.fromLocalFile("./assets/sounds/combat_music.wav")
        )
        self.combat_music.setVolume(0.5)
        self.combat_music.play()
        self.point_window = PointWindow(self)
        self.stopWalking()
        self.point_window.show()

    def resumeBackgroundMusic(self) -> None:
        self.combat_music.stop()
        self.background_music.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
