from pokemon import pokemon, pokemonSauvage
from joueur import joueur

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from fichier_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Principal")
        self.resize(800, 600)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.quitButton.clicked.connect(self.close)


if __name__ == "__main__":
    pokemon_sauvage = pokemonSauvage(
        nom="Bulbasaur",
        type1="Grass",
        hp=45,
        atk=49,
        defense=49,
        atk_spe=65,
        defense_spe=65,
        vitesse=45,
        legendaire=False,
        position=(1, 2),
    )

    # pokemon_capture = capture(pokemon_sauvage)
    # pokemon_capture.attributs()

    j1 = joueur(
        position=[1, 2],
        pokemons_captures=[],
    )

    j1.affiche_pokemons_captures()
    j1.capture(pokemon_sauvage)
    j1.affiche_pokemons_captures()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()  # Appel de la méthode show() sur l'instance de MainWindow
    sys.exit(app.exec_())
