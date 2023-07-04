import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Stockage des tableaux Excel chargés par l'utilisateur
tableau_previsionel = None
energie_electrique = None
production_vapeur = None

# Style utilisant toute la largeur de l'écran
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: coral; /* Remplacez #f0f0f0 par la couleur d'arrière-plan souhaitée */
    }

    /* Modifier la police et la taille du titre */
    .title {
        font-family: 'Arial', sans-serif;
        font-size: 32px;
        color: #333333;
    }

    /* Modifier la taille des en-têtes de tableau */
    .dataframe th {
        font-size: 16px;
        background-color: #f5f5f5;
    }

    /* Modifier l'arrière-plan du tableau */
    .dataframe {
        background-color: #ffffff;
    }

    /* Ajouter de la marge autour du tableau */
    .dataframe {
        margin: 20px auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre de l'interface graphique
st.markdown("<h1 style='text-align: center;'>Interface graphique PMP</h1>", unsafe_allow_html=True)

st.title("Affichage intégral de la boucle eau-vapeur")

# Chemin vers l'image
image_path = "SCHEMA BOUCLE EAU VAPEUR.jpg"

# Affichage de l'image
st.image(image_path, caption='Image', use_column_width=True)

# Chemin vers la base de données des composants
excel_path = "bilan thermique(Réel) 1.xlsx"

# Lecture du classeur Excel
bilan_thermique = pd.read_excel(excel_path)

# Affichage des données dans Streamlit
st.title("Base de données des composantes du cycle eau-vapeur")
st.dataframe(bilan_thermique)

#############################################################################################

## Tableau prévisionnel
st.title("Tableau prévisionnel")
tableau_previsionel_file = st.file_uploader("Upload Excel file", type=["xlsx"], key=1)
if tableau_previsionel_file is not None:
    tableau_previsionel = pd.read_excel(tableau_previsionel_file)
    st.write("File uploaded successfully.")
    st.write("File Name:", tableau_previsionel_file.name)
    st.dataframe(tableau_previsionel)

## Tableau énergie électrique
st.title("Production de l'énergie électrique")
energie_electrique_file = st.file_uploader("Upload Excel file", type=["xlsx"], key=2)
if energie_electrique_file is not None:
    energie_electrique = pd.read_excel(energie_electrique_file)
    st.write("File uploaded successfully.")
    st.write("File Name:", energie_electrique_file.name)
    st.dataframe(energie_electrique)

## Tableau production de vapeur
st.title("Production de la vapeur")
production_vapeur_file = st.file_uploader("Upload Excel file", type=["xlsx"], key=3)
if production_vapeur_file is not None:
    production_vapeur = pd.read_excel(production_vapeur_file)
    st.write("File uploaded successfully.")
    st.write("File Name:", production_vapeur_file.name)
    st.dataframe(production_vapeur)

# Fonction pour le calcul des KPI
def kpi():
    if tableau_previsionel is not None and energie_electrique is not None and production_vapeur is not None:
        # Effectuer le calcul des KPI ici en utilisant les tableaux
        # tableau_previsionel, energie_electrique, production_vapeur
        # ...

        # Exemple : Calcul du coefficient de corrélation entre la production de vapeur et l'énergie électrique
        df = pd.merge(production_vapeur, energie_electrique, on='Date')
        x = df['Production Vapeur']
        y = df['Energie Electrique']
        model = LinearRegression()
        model.fit(x.values.reshape(-1, 1), y.values.reshape(-1, 1))
        correlation = model.coef_[0][0]

        # Affichage du résultat
        st.title("Résultats des KPI")
        st.write("Coefficient de corrélation entre la production de vapeur et l'énergie électrique:", correlation)

# Bouton pour le calcul des KPI
if st.button("Calculer les KPI"):
    kpi()
