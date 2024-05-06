from abc import ABCMeta, abstractmethod, ABC
import numpy as np
import pandas as pd
import random as rd

class pokemon(metaclass=ABCMeta):
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


##### systeme combat
    

def attaqueneutre(pokemonOffensif : pokemon, pokemonDefensif : pokemon):
    
    if pokemonOffensif.atk > pokemonOffensif.atk_spe:
        degat = np.floor(22*pokemonOffensif.atk/pokemonDefensif.defense)
    else :
        degat = np.floor(22*pokemonOffensif.atk_spe/pokemonDefensif.defense_spe)  
    return(degat)


def attaquetype(pokemonOffensif : pokemon, pokemonDefensif : pokemon):
    
    T1 = pd.read_excel('Tableaudestypes.xlsx')
    TableDesTypes = T1.drop(T1.columns[0], axis=1)
    TableDesTypesNumpy = TableDesTypes.values
    multiplicateur = TableDesTypesNumpy[pokemonDefensif.type1, pokemonOffensif.type1]    
    if pokemonOffensif.atk > pokemonOffensif.atk_spe:
        degat = np.floor(np.floor(22*pokemonOffensif.atk/pokemonDefensif.defense)*multiplicateur)
    else :
        degat = np.floor(np.floor(22*pokemonOffensif.atk_spe/pokemonDefensif.defense_spe)*multiplicateur)    
    return(degat)


def fuite(pokemon_sauvage : pokemonSauvage, pokemon_capture : pokemonCapture):
    
    proba = (pokemon_capture.vitesse*32/np.floor((pokemon_sauvage/4)%255))+30
    if proba > 255:
        return True
    else:
        nb = rd.randint(0,255)
        if nb>proba:
            return False
        else:
            return True
        

def ChangerDePokemon(Joueur : Joueur):
    print(Joueur.ListePokemon)
    remplacant = input('Choisissez un nouveau Pokemon') #à voir plus tard quand on commencera l'interface graphique