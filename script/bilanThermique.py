import pandas as pd

# Lire le fichier Excel avec des colonnes imbriquées
df = pd.read_excel('../files/bilan thermique(Réel).xlsx', header=[7, 8])
df = df[:39]
print(df['Valeur Nominale'])