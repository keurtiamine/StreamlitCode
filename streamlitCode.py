import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

st.markdown("<h1 style='text-align: center;'>Interface graphique PMP</h1>", unsafe_allow_html=True)


st.title("Affichage intégral de la boucle eau-vapeur")

# Chemin vers l'image
image_path = "SCHEMA BOUCLE EAU VAPEUR.jpg"

# Affichage de l'image
st.image(image_path, caption='Image', use_column_width=True)
# Fonction pour calculer le KPI en fonction des paramètres sélectionnés
def calculate_kpi(param1, param2, norm):
    # Test pour l'opération de division
    if isinstance(param1, str) or isinstance(param2, str):
        st.write("Les paramètres ne doivent pas être des chaînes de caractères")
        return None
    
    # Logique de calcul du KPI en utilisant les paramètres sélectionnés
    kpi_result = param1 / param2
    
    # Calcul de la différence avec la norme
    diff = np.abs(kpi_result - norm)
    
    return kpi_result, diff

# Interface utilisateur
st.title('Calcul du KPI')

# Chargement des tableaux à partir des fichiers Excel
tableau1_file = st.file_uploader('Charger le tableau 1 (Excel)', type='xlsx')
tableau2_file = st.file_uploader('Charger le tableau 2 (Excel)', type='xlsx')

# Vérification si les fichiers ont été chargés
if tableau1_file is not None and tableau2_file is not None:
    # Lecture des fichiers Excel pour créer les tableaux de données
    tableau1 = pd.read_excel(tableau1_file)
    tableau2 = pd.read_excel(tableau2_file)
    
    # Liste des tableaux disponibles avec leurs noms
    tableaux = {'Tableau 1': tableau1, 'Tableau 2': tableau2}
    
    # Sélection du tableau pour le premier paramètre
    tableau1_choice = st.selectbox('Choisir un tableau pour le premier paramètre', list(tableaux.keys()))
    
    # Récupération du tableau sélectionné pour le premier paramètre
    selected_tableau1 = tableaux[tableau1_choice]
    
    # Affichage du tableau pour le premier paramètre
    st.write('Tableau sélectionné pour le premier paramètre :')
    st.write(selected_tableau1)
    
    # Sélection du tableau pour le deuxième paramètre
    tableau2_choice = st.selectbox('Choisir un tableau pour le deuxième paramètre', list(tableaux.keys()))
    
    # Récupération du tableau sélectionné pour le deuxième paramètre
    selected_tableau2 = tableaux[tableau2_choice]
    
    # Affichage du tableau pour le deuxième paramètre
    st.write('Tableau sélectionné pour le deuxième paramètre :')
    st.write(selected_tableau2)
    
    # Récupération des lignes 1 à 12 des deux tableaux pour les paramètres
    param1_values = selected_tableau1.iloc[1:13, :]
    param2_values = selected_tableau2.iloc[1:13, :]
    
    # Sélection des colonnes (paramètres) pour chaque tableau
    param1_columns = param1_values.columns.tolist()
    param2_columns = param2_values.columns.tolist()
    
    # Sélection des paramètres pour le premier paramètre
    selected_param1 = st.selectbox('Choisir un paramètre pour le premier paramètre', param1_columns)
    
    # Sélection des paramètres pour le deuxième paramètre
    selected_param2 = st.selectbox('Choisir un paramètre pour le deuxième paramètre', param2_columns)
    
    # Demande de la norme du KPI
    norm = st.number_input("Norme du KPI", value=1.0)
    
    # Bouton de calcul
    calculate_button = st.button('Calculer')
    
    # Vérification si le bouton de calcul a été cliqué
    if calculate_button:
        # Récupération des valeurs des paramètres sélectionnés
        param1_values = param1_values[selected_param1].tolist()
        param2_values = param2_values[selected_param2].tolist()
        
        # Calcul du KPI et différence avec la norme
        results = [calculate_kpi(param1, param2, norm) for param1, param2 in zip(param1_values, param2_values)]
        
        # Filtrage des résultats valides
        valid_results = [(kpi, diff) for kpi, diff in results if kpi is not None]
        kpi_values, diff_values = zip(*valid_results)
        
        # Affichage du tableau de résultats
        st.write('Résultats du KPI :')
        kpi_df = pd.DataFrame({selected_param1: param1_values, selected_param2: param2_values, 'KPI': kpi_values, 'Différence': diff_values})
        st.write(kpi_df)
        
        # Affichage du graphe
        st.write('Graphe du KPI :')
        plt.figure(figsize=(10, 6))
        plt.plot(np.arange(1, 13), kpi_values, marker='o', linestyle='-', linewidth=2, color='blue', label='KPI')
        plt.axhline(norm, color='red', linestyle='--', linewidth=2, label='Norme')
        plt.xlabel('Index')
        plt.ylabel('KPI')
        plt.title('Évolution du KPI avec la Norme')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)
