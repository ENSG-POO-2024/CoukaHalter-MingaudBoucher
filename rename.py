import os
import pandas as pd

repertoire = 'assets/frame2'
noms = pd.read_csv('data/pokemon_first_gen.csv')
nomsNumpy = noms.values

for i in range (151):
    
    nouveau_nom_fichier = f"sprites/back/frame2/{nomsNumpy[i, 1]}.png"
    
    os.rename(f"assets/frame2/{i+1}.png", nouveau_nom_fichier)