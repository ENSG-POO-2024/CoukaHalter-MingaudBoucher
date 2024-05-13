from pokemon import pokemon, pokemonSauvage
from joueur import joueur
from combat import combat
import pandas as pd
import numpy as np

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


    stats = pd.read_csv('data/pokemon_first_gen.csv')
    position = pd.read_csv('data/pokemon_coordinates.csv')
    recap = pd.merge(position,stats, left_on='pokemon', right_on='Name') #tableau des pokemons sauvages
    TablePokemon = recap.values #tableau des pokemons sauvages en numpy
    
    
    pokemon1 = recap.head(1)
    an = combat.attaqueneutre(j1.pokemons_captures[0], pokemon1)
    at = combat.attaquetype(j1.pokemons_captures[0], pokemon1)
    combat1 = combat.combat(j1, TablePokemon[0])
