from abc import ABCMeta, abstractmethod, ABC


class pokemon(metaclass=ABCMeta):
    def __init__(
        self, nom, type1, hp, atk, defense, atk_spe, defense_spe, vitesse, legendaire
    ) -> None:
        self.nom = nom
        self.type1 = type1
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.atk_spe = atk_spe
        self.defense_spe = defense_spe
        self.vitesse = vitesse
        self.legendaire = legendaire

    @abstractmethod
    def attributs(self):
        afficher_attributs = f"Nom : {self.nom}\nType1 : {self.type1}\nHP : {self.hp}\nAttaque : {self.atk}\nDefense : {self.defense}\nAttaque speciale : {self.atk_spe}\nVitesse : {self.vitesse}\nLegendaire : {self.legendaire}"
        print(afficher_attributs)


class pokemonSauvage(pokemon):
    def __init__(
        self,
        nom,
        type1,
        hp,
        atk,
        defense,
        atk_spe,
        defense_spe,
        vitesse,
        legendaire,
        position,
    ) -> None:
        super().__init__(
            nom, type1, hp, atk, defense, atk_spe, defense_spe, vitesse, legendaire
        )
        self.position = position

    def attributs(self):
        super().attributs()
        print(f"Position : {self.position}")


class pokemonCapture(pokemon):
    def __init__(
        self, nom, type1, hp, atk, defense, atk_spe, defense_spe, vitesse, legendaire
    ) -> None:
        super().__init__(
            nom, type1, hp, atk, defense, atk_spe, defense_spe, vitesse, legendaire
        )

    def attributs(self):
        return super().attributs()


def capture(pokemon_sauvage: pokemonSauvage):
    pokemon_capture = pokemonCapture(
        nom=pokemon_sauvage.nom,
        type1=pokemon_sauvage.type1,
        hp=pokemon_sauvage.hp,
        atk=pokemon_sauvage.atk,
        defense=pokemon_sauvage.defense,
        atk_spe=pokemon_sauvage.atk_spe,
        defense_spe=pokemon_sauvage.defense_spe,
        vitesse=pokemon_sauvage.vitesse,
        legendaire=pokemon_sauvage.legendaire,
    )
    return pokemon_capture
