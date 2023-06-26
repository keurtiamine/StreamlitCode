import pandas as pd
import streamlit as st

# Titre de l'interface graphique
st.title("Affichage intégral de la boucle eau-vapeur")

# Chemin vers l'image
image_path = "SCHEMA BOUCLE EAU VAPEUR.jpg"

# Affichage de l'image
st.image(image_path, caption='Image', use_column_width=True)

# Chemin vers le classeur Excel
excel_path = "bilan thermique(Réel) 1.xlsx"

# Lecture du classeur Excel
excel_data = pd.read_excel(excel_path)

# Affichage des données dans Streamlit
st.title("Affichage de la base de données des composantes du cycle eau-vapeur")
st.dataframe(excel_data)

