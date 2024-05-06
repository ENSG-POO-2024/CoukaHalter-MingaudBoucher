from pokemon import pokemon, pokemonSauvage, pokemonCapture, capture
from joueur import joueur


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
