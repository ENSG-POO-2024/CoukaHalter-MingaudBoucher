import os
import pandas as pd
import numpy as np

repertoire = 'assets'
nouveau_repertoire = 'sprites'
noms = pd.read_csv('data/pokemon_first_gen.csv')
nomsNumpy = noms.values

for index, nom_fichier in enumerate(os.listdir(repertoire)):
    # Générer le nouveau nom de fichier
    nouveau_nom_fichier = noms[index, 1]
    
    # Ancien chemin complet du fichier
    ancien_chemin = os.path.join(repertoire, nom_fichier)
    
    # Nouveau chemin complet du fichier
    nouveau_chemin = os.path.join(nouveau_repertoire, nouveau_nom_fichier)
    
    # Renommer le fichier
    os.rename(ancien_chemin, nouveau_chemin)