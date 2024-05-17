from PyQt5 import QtCore, QtGui, QtWidgets


from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtMultimedia import QSoundEffect
from pokemon import pokemonCapture, pokemonSauvage
from joueur import joueur
import sys
import random
import math
import os
import csv


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
    def __init__(
        self,
        main_window: "MainWindow",
        img_pokemon_sauvage: str,
        img_pokemon_capture: str,
    ) -> None:
        super().__init__()
        self.main_window = main_window
        self.setGeometry(100, 100, 465, 640)
        self.setWindowTitle("Combat")

        # Set up background label
        self.background_label = QtWidgets.QLabel(self)
        self.background_label.setGeometry(0, 0, 465, 640)
        self.setBackgroundImage(
            "combat.png"
        )  # Change this to your background image path

        self.image_label_sauvage = QtWidgets.QLabel(self)
        self.image_label_sauvage.setGeometry(300, 70, 100, 100)
        self.setFrontImage(self.image_label_sauvage, img_pokemon_sauvage)

        self.image_label_capture = QtWidgets.QLabel(self)
        self.image_label_capture.setGeometry(60, 165, 100, 100)
        self.setBackImage(self.image_label_capture, img_pokemon_capture)

    def setFrontImage(self, label: QtWidgets.QLabel, image_file: str) -> None:
        image_path = f"./sprites/front/{image_file}"
        pixmap = QtGui.QPixmap(image_path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)

    def setBackImage(self, label: QtWidgets.QLabel, image_file: str) -> None:
        image_path = f"./sprites/back/{image_file}"
        pixmap = QtGui.QPixmap(image_path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)

    def setBackgroundImage(self, image_file: str) -> None:
        image_path = f"./sprites/interfaces/{image_file}"
        pixmap = QtGui.QPixmap(image_path)
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.main_window.resumeBackgroundMusic()
        super().closeEvent(event)


class MainWindow(QMainWindow, Ui_MainWindow):
    MAP_FILE = "./sprites/interfaces/map.png"
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
        self.pokemon_sauvages = []
        self.pokemon_windows = []
        self.pokemon_data = self.load_pokemon_data("./data/pokemon_first_gen.csv")
        self.generateRandomPokemons()
        self.pokemonFought = ""
        self.joueur = joueur()
        self.joueur.capture(self.pokemon_sauvages[0])

    def load_pokemon_data(self, file_path):
        pokemon_data = []
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pokemon_data.append(
                    (
                        row["Name"],
                        row["Type 1"],
                        row["Type 2"] if row["Type 2"] else None,
                        int(row["HP"]),
                        int(row["Attack"]),
                        int(row["Defense"]),
                        int(row["Sp. Atk"]),
                        int(row["Sp. Def"]),
                        int(row["Speed"]),
                        row["Legendary"] == "True",
                    )
                )
        return pokemon_data

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
        self.updatePokemons()

    def moveCharacter(self, dx: int, dy: int) -> None:
        new_x = self.character_x + dx
        new_y = self.character_y + dy

        # Ensure new_x and new_y stay within the defined rectangle bounds
        new_x = max(82, min(new_x, 880 - self.character_label.width()))
        new_y = max(62, min(new_y, 1440 - self.character_label.height()))

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

    def generateRandomPokemons(self) -> None:
        images_folder = "./sprites/front/"
        image_files = [
            f
            for f in os.listdir(images_folder)
            if os.path.isfile(os.path.join(images_folder, f))
        ]
        for _ in range(10):
            if not image_files:
                break
            image_file = random.choice(image_files)
            image_files.remove(image_file)
            map_x = random.randint(82, 880 - 20)
            map_y = random.randint(62, 1420 - 20)
            window_x = map_x - self.window_x
            window_y = map_y - self.window_y
            pokemon_label = QtWidgets.QLabel(self.centralwidget)
            pokemon_pixmap = QtGui.QPixmap(os.path.join(images_folder, image_file))
            pokemon_label.setPixmap(pokemon_pixmap)
            pokemon_label.setGeometry(window_x, window_y, 70, 70)
            pokemon_label.setScaledContents(True)
            pokemon_label.show()
            # Create a pokemonSauvage instance
            if self.pokemon_data:
                pokemon_info = random.choice(self.pokemon_data)
                sauvage = pokemonSauvage(
                    nom=pokemon_info[0],
                    type1=pokemon_info[1],
                    type2=pokemon_info[2],
                    hp=pokemon_info[3],
                    atk=pokemon_info[4],
                    defense=pokemon_info[5],
                    atk_spe=pokemon_info[6],
                    defense_spe=pokemon_info[7],
                    vitesse=pokemon_info[8],
                    legendaire=pokemon_info[9],
                    position=(map_x, map_y),
                    chemin_sprite=image_file,
                    pokemon_label=pokemon_label,
                )
                self.pokemon_sauvages.append(sauvage)

    def distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def updatePokemons(self) -> None:
        character_center_x = self.character_x + self.character_label.width() / 2
        character_center_y = self.character_y + self.character_label.height() / 2

        for idx, sauvage in enumerate(self.pokemon_sauvages):
            img_pokemon_sauvage = sauvage.chemin_sprite
            pokemon_label = sauvage.pokemon_label
            map_x = sauvage.position[0]
            map_y = sauvage.position[1]
            pokemon_label.move(map_x - self.window_x, map_y - self.window_y)
            distance_to_pokemon = self.distance(
                character_center_x, character_center_y, map_x, map_y
            )

            if distance_to_pokemon < 100:
                print(f"Character is near pokemon {idx + 1} ({img_pokemon_sauvage})")
                if idx not in self.pokemon_windows:
                    self.pokemon_windows.append(idx)
                    pokemon_label.hide()
                    self.pokemonFought = img_pokemon_sauvage
                    self.openPointWindow(img_pokemon_sauvage)
                    self.joueur.capture(sauvage)
                    self.joueur.affiche_pokemons_captures()

    def openPointWindow(self, img_pokemon_sauvage: str) -> None:
        self.background_music.stop()
        self.combat_music = QSoundEffect()
        self.combat_music.setSource(
            QtCore.QUrl.fromLocalFile("./assets/sounds/combat_music.wav")
        )
        self.combat_music.setVolume(0.5)
        self.combat_music.play()

        img_pokemon_capture = self.joueur.pokemons_captures[0].chemin_sprite
        self.pokemon_window = PointWindow(
            self, img_pokemon_sauvage, img_pokemon_capture
        )
        self.stopWalking()
        self.pokemon_window.show()
        print(f"You encountered a Pokémon: {self.pokemonFought}")

    def resumeBackgroundMusic(self) -> None:
        self.combat_music.stop()
        self.background_music.play()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.background_music.stop()
        if hasattr(self, "combat_music") and self.combat_music.isPlaying():
            self.combat_music.stop()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
