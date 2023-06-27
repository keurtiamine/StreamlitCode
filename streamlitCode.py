import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

#style use the entire screen width
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
   
    body {
        background-color: coral; /* Replace #f0f0f0 with your desired background color */
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

##tableau previsionel
st.title("Tableau prévisionnel")
tableau_previsionel_file = st.file_uploader("Upload Excel file", type=["xlsx"], key=1)
if tableau_previsionel_file is not None:
    tableau_previsionel = pd.read_excel(tableau_previsionel_file)
    st.write("File uploaded successfully.")
    st.write("File Name:", tableau_previsionel_file.name)
    st.dataframe(tableau_previsionel)
     # Préparation des données pour l'entraînement du modèle
    X_train = tableau_previsionel.index.values.reshape(-1, 1)
    y_train = tableau_previsionel['Production\nPrévue (MWH)\nGTA']

    # Entraînement du modèle de régression linéaire
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Prédiction de la production pour l'année suivante
    next_year = X_train[-1][0] + 1
    predicted_production = model.predict([[next_year]])

    st.write("Prédiction de la production pour l'année suivante :")
    st.write(predicted_production)	

## tableau energie electrique
st.title("Production de l'énergie électrique")
energie_electrique_file = st.file_uploader("Upload Excel file", type=["xlsx"], key=2)
if energie_electrique_file is not None:
    energie_electrique = pd.read_excel(energie_electrique_file)
    st.write("File uploaded successfully.")
    st.write("File Name:", energie_electrique_file.name)
    st.dataframe(energie_electrique)
st.title("Production de la vapeur HP")
production_vapeur_file = st.file_uploader("Upload Excel file", type=["xlsx"], key=3)
if production_vapeur_file is not None:
    production_vapeur = pd.read_excel(production_vapeur_file, header=[0, 1])
    st.write("File uploaded successfully.")
    st.write("File Name:", production_vapeur_file.name)
    st.dataframe(production_vapeur)

def kpi():
    st.write("Ces tableaux ont pour but le calcul des différents KPI suivants :")
    st.markdown("1- Capacité de production inutilisée")
    # afficher la capacité de production inutilisée pour chaque mois

    # creer une data frame vide
    capacite_production_inutilisee = pd.DataFrame()
    capacite_max = bilan_thermique[(bilan_thermique['Unité / Equipement'] == 'SAP') & (
                bilan_thermique['Type de Fuide'] == 'Vapeur HP')]['Débit (T/H)'].min() * 24 * 30

    st.write("La capacité maximale de production de vapeur HP est de : ", capacite_max, "T/Mois")
    # fill the data frame capacite_productio_inutilisee with the values month and capacitemax-capacitemonth from production_vapeur
    capacite_production_inutilisee['Mois'] = production_vapeur['Mois']
    capacite_production_inutilisee['Capacité de production inutilisée'] = capacite_max - production_vapeur['Prod\nSAP']
    st.write("capacite_production_inutilisee['Capacité de production inutilisée'] = capacite_max - production_vapeur['Prod\nSAP']")
    capacite_production_inutilisee['pourcentage inutilisé'] = (capacite_production_inutilisee[
                                                                   'Capacité de production inutilisée'] / capacite_max) * 100
    capacite_production_inutilisee["Nombre d'heure de pannes machine/ maintenance"] = capacite_production_inutilisee[
                                                                                          'Capacité de production inutilisée'] / capacite_max * 720

    capacite_production_inutilisee.loc[capacite_production_inutilisee[
                                           "Nombre d'heure de pannes machine/ maintenance"] < 0, "Nombre d'heure de pannes machine/ maintenance"] = 0

    st.dataframe(capacite_production_inutilisee.iloc[1:13, :])

    st.markdown("2- Fiabilité des planings et des prévisions")

    # creer une data frame pour comparer la df tableau_previsionel et la dfenergie_electrique
    fiabilite_prevision = pd.DataFrame()
    fiabilite_prevision['Mois'] = tableau_previsionel['Mois']
    fiabilite_prevision['Prévision (MWH)'] = tableau_previsionel['Production\nPrévue (MWH)\nGTA']
    fiabilite_prevision['Production réalisée (MWH)'] = energie_electrique['Production\nRéalisée (MWH)\nGTA']
    fiabilite_prevision['Rapport de Fiabilité Réalisée/Prévision'] = (fiabilite_prevision['Production réalisée (MWH)'] /
                                                                      fiabilite_prevision['Prévision (MWH)']) * 100
    fiabilite_prevision['Différence'] = fiabilite_prevision['Production réalisée (MWH)'] - fiabilite_prevision[
        'Prévision (MWH)']

    # afficher la df fiabilite_prevision dqns un tableau qui prend la largeur de l'ecran

    st.dataframe(fiabilite_prevision.iloc[1:13, :])
    st.write("La fiabilité des prévisions est de : ",
             fiabilite_prevision['Rapport de Fiabilité Réalisée/Prévision'].iloc[1: 13].mean(), "%")

    st.markdown("3- Rendement de la production d'énergie électrique")
    # Énergie thermique = Masse de vapeur (en kg) × Chaleur spécifique de la vapeur (en J/kg·°C) × Écart de température (en °C)
    energie1 = (141 - 53) * 1000 * 1440 * (500 - 211)
    energie2 = (141 - 11.8) * 1000 * 1440 * (500 - 118)
    energie3 = (141 - 13.2) * 1000 * 1440 * (500 - 80)
    energie4 = (141 - 70) * 1000 * 1440 * (500 - 33.5)
    energieTotal = energie1 + energie2 + energie3 + energie4
    # Rendement de la production d'électricité = (Électricité produite / Énergie thermique de la vapeur HP) * 100

    rendement_production_electrique = pd.DataFrame()
    rendement_production_electrique['Mois'] = energie_electrique['Mois']
    rendement_production_electrique['Rendement de la production d\'énergie électrique'] = ((energie_electrique[
                                                                                                'Production\nRéalisée (MWH)\nGTA'] * 3.6 * (
                                                                                                        10 ** 9)) / (
                                                                                                       720 * energieTotal)) * 100
    st.write("rendement_production_electrique['Rendement de la production d'énergie électrique'] = ((energie_electrique'Production Réalisée (MWH) GTA'] * 3.6 * (10 ** 9)) / (720 * energieTotal)) * 100")
    st.dataframe(rendement_production_electrique.iloc[1:13, :])
    st.write("Le rendement de la production d'énergie électrique est de : ",
             rendement_production_electrique['Rendement de la production d\'énergie électrique'].iloc[1: 13].mean(),
             "%")

    st.markdown("4- Taux de rejet de vapeur HP")
    # Taux de rejet de vapeur HP = (Vapeur HP rejetée / Vapeur HP produite) * 100
    taux_rejet_vapeur = pd.DataFrame()
    taux_rejet_vapeur['Mois'] = production_vapeur['Mois']
    consomationDetente = production_vapeur['Consommation']['Détente']
    productionSap = production_vapeur['Prod\nSAP']['Unnamed: 1_level_1']
    taux_rejet_vapeur['Taux de rejet de vapeur HP'] = ((consomationDetente) / productionSap) * 100
    st.write("taux_rejet_vapeur['Taux de rejet de vapeur HP'] = ((consomationDetente) / productionSap) * 100")
    st.dataframe(taux_rejet_vapeur.iloc[1:13, :])
    st.write("Le taux de rejet de vapeur HP est de : ",
             taux_rejet_vapeur['Taux de rejet de vapeur HP'].iloc[1: 13].mean(), "%")

    st.markdown("5- Taux de productivité de l'énergie électrique")
    # Taux de productivité de l'énergie électrique = (Énergie électrique produite / Énergie consommé) * 100
    taux_productivite_electrique = pd.DataFrame()
    taux_productivite_electrique['Mois'] = energie_electrique['Mois']
    taux_productivite_electrique['Taux de productivité de l\'énergie électrique'] = energie_electrique[
                                                                                        'Production\nRéalisée (MWH)\nGTA'] / \
                                                                                    energie_electrique[
                                                                                        'Conso\nUsine'] * 100
    st.write("taux_productivite_electrique['Taux de productivité de l\'énergie électrique'] = energie_electrique'Production Réalisée (MWH) GTA'] / energie_electrique'Conso Usine'] * 100")
    st.dataframe(taux_productivite_electrique.iloc[1:13, :])
    st.write("Le taux de productivité de l'énergie électrique est de : ",
             taux_productivite_electrique['Taux de productivité de l\'énergie électrique'].iloc[1: 13].mean(), "%")

if production_vapeur_file is not None and energie_electrique_file is not None and tableau_previsionel_file is not None:
    kpi()
