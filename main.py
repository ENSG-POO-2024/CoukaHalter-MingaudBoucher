# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:36:30 2024

@author: Formation
"""

from pokemon import pokemon, pokemonSauvage
from joueur import joueur
from combat import attaqueneutre, attaquetype, fuite, ChangerDePokemon, combat
import pandas as pd
import numpy as np

if __name__ == "__main__":
    pokemon_sauvage = pokemonSauvage(
        nom="Bulbasaur",
        type1="Grass",
        type2="Poison",
        hp=45,
        atk=49,
        defense=49,
        atk_spe=65,
        defense_spe=65,
        vitesse=45,
        legendaire=False,
        position=(1, 2),
    )
    
    pokemon_sauvage2 = pokemonSauvage(
        nom="Charmander",
        type1="Fire",
        type2= "nan",
        hp=39,
        atk=52,
        defense=43,
        atk_spe=60,
        defense_spe=50,
        vitesse=65,
        legendaire=False,
        position=(3.3, 0.3),
    )

    # pokemon_capture = capture(pokemon_sauvage)
    # pokemon_capture.attributs()

    j1 = joueur(
        position=[1, 2],
        pokemons_captures=[],
    )

    j1.affiche_pokemons_captures()
    j1.capture(pokemon_sauvage)
    j1.capture(pokemon_sauvage2)
    #j1.affiche_pokemons_captures()


    stats = pd.read_csv('data/pokemon_first_gen.csv')
    position = pd.read_csv('data/pokemon_coordinates.csv')
    recap = pd.merge(position,stats, left_on='pokemon', right_on='Name')#tableau des pokemons sauvages
    recap = recap.drop(recap.columns[2], axis=1)
    recap = recap.rename(columns={"Name": "nom", "Type 1": "type1", "Type 2": "type2", "HP":"hp", "Attack": "atk", "Defense": "defense","Sp. Atk": "atk_spe", "Sp. Def": "defense_spe", "Speed": "vitesse", "Legendary": "legendaire", "coordinates": "position"})
    TablePokemon = recap.values #tableau des pokemons sauvages en numpy
    
    T1 = pd.read_excel('Tableaudestypes.xlsx')
    TableDesTypes = T1.drop(T1.columns[0], axis=1)
    TableDesTypesNumpy = TableDesTypes.values   
    
    pokemon1 = recap.head(1)
    pokemon2 = recap.tail(1)
    an1 = attaqueneutre(j1.pokemons_captures[0], pokemon1)
    an2 = attaqueneutre(j1.pokemons_captures[0], pokemon2)
    fu = fuite(pokemon1, j1.pokemons_captures[0])
    #at1 = attaquetype(j1.pokemons_captures[0], pokemon1)
    #at2 = attaquetype(pokemon1, j1.pokemons_captures[0])
    #combat1 = combat(j1, pokemon1)
    #combat2 = combat(j1, pokemon2)
    print(j1)
    