from pokemon import pokemonCapture, pokemonSauvage


class joueur:
    def __init__(self) -> None:
        self.pokemons_captures = []

    def capture(self, pokemon_sauvage: pokemonSauvage):
        pokemon_capture = pokemonCapture(
            ID=1 + len(self.pokemons_captures),
            nom=pokemon_sauvage.nom,
            type1=pokemon_sauvage.type1,
            type2=pokemon_sauvage.type2,
            hp=pokemon_sauvage.hp,
            atk=pokemon_sauvage.atk,
            defense=pokemon_sauvage.defense,
            atk_spe=pokemon_sauvage.atk_spe,
            defense_spe=pokemon_sauvage.defense_spe,
            vitesse=pokemon_sauvage.vitesse,
            legendaire=pokemon_sauvage.legendaire,
        )

        return self.pokemons_captures.append(pokemon_capture)

    def affiche_pokemons_captures(self):
        pokemons_captures = self.pokemons_captures
        if pokemons_captures == []:
            print("aucun pokemon n'a ete capture")
        else:
            for pokemon in pokemons_captures:
                print(pokemon.nom)
