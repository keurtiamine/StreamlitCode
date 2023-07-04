import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fonction pour calculer le KPI en fonction des paramètres sélectionnés
def calculate_kpi(param1, param2):
    # Logique de calcul du KPI en utilisant les paramètres sélectionnés
    kpi_result = param1 * param2  # Exemple de calcul simple
    
    return kpi_result

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
    
    # Sélection du tableau
    tableau_choice = st.selectbox('Choisir un tableau', list(tableaux.keys()))
    
    # Récupération du tableau sélectionné
    selected_tableau = tableaux[tableau_choice]
    
    # Affichage du tableau
    st.write('Tableau sélectionné :')
    st.write(selected_tableau)
    
    # Récupération des noms des colonnes (paramètres) du tableau sélectionné
    params = selected_tableau.columns.tolist()
    
    # Sélection des paramètres
    selected_params = st.multiselect('Choisir les paramètres', params)
    
    # Bouton de calcul
    calculate_button = st.button('Calculer')
    
    # Vérification si le bouton de calcul a été cliqué
    if calculate_button:
        # Récupération des valeurs des paramètres sélectionnés
        param_values = []
        for param in selected_params:
            param_value = st.number_input(param, value=0.0)
            param_values.append(param_value)
        
        # Calcul du KPI
        kpi_value = calculate_kpi(*param_values)
        
        # Affichage du tableau de résultats
        st.write('Résultats du KPI :')
        kpi_df = pd.DataFrame({param: [value] for param, value in zip(selected_params, param_values)})
        kpi_df['KPI'] = kpi_value
        st.write(kpi_df)
        
        # Affichage du graphe
        st.write('Graphe du KPI :')
        plt.plot(kpi_df['KPI'])
        plt.xlabel('Index')
        plt.ylabel('KPI')
        st.pyplot(plt)
