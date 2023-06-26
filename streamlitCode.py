import pandas as pd
import streamlit as st

# Titre de l'interface graphique
st.title("Affichage intégral de la boucle eau-vapeur")

# Chemin vers l'image
image_path = "SCHEMA BOUCLE EAU VAPEUR.jpg"

# Affichage de l'image
st.image(image_path, caption='Image', use_column_width=True)

# Chemin vers la base de données des composants
excel_path = "bilan thermique(Réel) 1.xlsx"

# Lecture du classeur Excel
excel_data = pd.read_excel(excel_path)

# Affichage des données dans Streamlit
st.title("Base de données des composantes du cycle eau-vapeur")
st.dataframe(excel_data)

excel_path = "Tableau prévisionnel.xlsx"
excel_data = pd.read_excel(excel_path)
st.title("Tableau prévisionnel")
st.dataframe(excel_data)

excel_path = "Energie électrique.xlsx"
excel_data = pd.read_excel(excel_path)
st.title("Production de l'énergie électrique")
st.dataframe(excel_data)

excel_path = "Production vapeur HP.xlsx"
excel_data = pd.read_excel(excel_path)
table_caption = "Ces tableaux seront utilisés afin de pouvoir calculer les différents KPI suivants"

# Affichage du tableau Excel avec légende
st.title("Production de la vapeur HP")
st.write(table_caption)
st.write(excel_data)
