from abc import ABCMeta, abstractmethod, ABC


class pokemon(metaclass=ABCMeta):
    def __init__(
        self,
        nom,
        type1,
        type2,
        hp,
        atk,
        defense,
        atk_spe,
        defense_spe,
        vitesse,
        legendaire,
    ) -> None:

        self.nom = nom
        self.type1 = type1
        self.type2 = type2
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
        type2,
        hp,
        atk,
        defense,
        atk_spe,
        defense_spe,
        vitesse,
        legendaire,
        position,
        chemin_sprite,
        pokemon_label,
    ) -> None:

        super().__init__(
            nom,
            type1,
            type2,
            hp,
            atk,
            defense,
            atk_spe,
            defense_spe,
            vitesse,
            legendaire,
        )
        self.position = position
        self.chemin_sprite = chemin_sprite
        self.pokemon_label = pokemon_label

    def attributs(self):

        super().attributs()
        print(f"Position : {self.position}")


class pokemonCapture(pokemon):

    def __init__(
        self,
        ID,
        nom,
        type1,
        type2,
        hp,
        atk,
        defense,
        atk_spe,
        defense_spe,
        vitesse,
        legendaire,
    ) -> None:
        super().__init__(
            nom,
            type1,
            type2,
            hp,
            atk,
            defense,
            atk_spe,
            defense_spe,
            vitesse,
            legendaire,
        )
        self.ID = ID

    def attributs(self):

        return super().attributs()
