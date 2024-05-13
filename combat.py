from joueur import joueur
from pokemon import pokemon, pokemonSauvage, pokemonCapture
import numpy as np
import pandas as pd
import random as rd


class combat():

    def __init__(self, joueur, pokemonSauvage) -> None:
        self.joueur = joueur
        self.pokemonSauvage = pokemonSauvage

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
        
    def ChangerDePokemon(Joueur : joueur):
        print(Joueur.pokemons_captures)
        remplacant = input('Choisissez un nouveau Pokemon') #à voir plus tard quand on commencera l'interface graphique
        index=0
        for i in range (len(Joueur.pokemons_captures)):
            if remplacant==pokemon:
                index = i
            else:
                return "Ce pokemon n'existe pas"
        permu = Joueur.pokemons_captures[0]
        Joueur.pokemons_captures[0] = Joueur.pokemons_captures[i]
        Joueur.pokemons_captures[i] = permu
        return Joueur
"""
    def combat(joueur : joueur, pokemon_sauvage : pokemonSauvage):
        if pokemon_sauvage.hp == 0:
            joueur.capture(pokemon_sauvage)
            #backtomap
            #win(le poke disparait de la map)
            return 'de retour au bercail'
        elif len(joueur.pokemons_captures) == 0:
            return'gros nul'
            #backtomap
            #game over gros nul
        elif combat.fuite(pokemon_sauvage, joueur.pokemons_captures[0]):
            #backtomap
            #lose(le poke reste sur la map)
            return 'lache'
        #else:
            #if bouton 'attaque neutre' pressé :
            #    if pokemon_sauvage.vitesse < Joueur.pokemons_captures[0].vitesse:
            #       pokemon_sauvage.hp() -= attaqueneutre(Joueur.pokemons_captures[0], pokemon_sauvage)
            #       if pokemon_sauvage.hp() == 0:
            #           joueur.capture(pokemon_sauvage)
            #       else:
            #           Joueur.pokemons_captures[0].hp -= attaqueneutre(pokemon_sauvage, Joueur.pokemons_captures[0])
            #    else:
            #       Joueur.pokemons_captures[0].hp() -= attaqueneutre(pokemon_sauvage, Joueur.pokemons_captures[0])
            #       if Joueur.pokemons_captures[0].hp() == 0:
            #          return combat(joueur, pokemon_sauvage)
            #       else:
            #           pokemon_sauvage.hp() -= attaqueneutre(Joueur.pokemons_captures[0], pokemon_sauvage)
            #   return combat(joueur, pokemon_sauvage)   
            #on fait pareil pour les 3 autres boutons
            #if bouton 'attaque type' pressé 
            #    if pokemon_sauvage.vitesse < Joueur.pokemons_captures[0].vitesse:
            #       pokemon_sauvage.hp() -= attaquetype(Joueur.pokemons_captures[0], pokemon_sauvage)
            #       if pokemon_sauvage.hp() == 0:
            #           joueur.capture(pokemon_sauvage)
            #       else:
            #           Joueur.pokemons_captures[0].hp -= attaquetype(pokemon_sauvage, Joueur.pokemons_captures[0])
            #    else:
            #       Joueur.pokemons_captures[0].hp() -= attaquetype(pokemon_sauvage, Joueur.pokemons_captures[0])
            #       if Joueur.pokemons_captures[0].hp() == 0:
            #          return combat(joueur, pokemon_sauvage)
            #       else:
            #           pokemon_sauvage.hp() -= attaquetype(Joueur.pokemons_captures[0], pokemon_sauvage)
            #   return combat(joueur, pokemon_sauvage)  ^
            #if bouton 'changer de pokemon' pressé
            #   return combat(ChangerDePokemon(joueur), pokemon_sauvage)
            #if bouton 'fuite' pressé
                fuite(pokemon_sauvage, joueur.pokemons_captures[0])
                return combat(joueur, pokemon_sauvage)
"""