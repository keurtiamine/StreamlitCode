import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fonction pour calculer le KPI en fonction des paramètres sélectionnés
def calculate_kpi(param1, param2):
    # Logique de calcul du KPI en utilisant les paramètres sélectionnés
    kpi_result = []
    for p1, p2 in zip(param1, param2):
        if isinstance(p1, (int, float)) and isinstance(p2, (int, float)) and p2 != 0:
            kpi_result.append(p1 / p2)
        else:
            kpi_result.append(None)
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
    
    # Récupération des lignes non vides des deux tableaux pour les paramètres
    param1_values = selected_tableau1.iloc[:, :].values.flatten().tolist()
    param2_values = selected_tableau2.iloc[:, :].values.flatten().tolist()
    
    # Filtrage des lignes vides
    param1_values = [param for param in param1_values if pd.notnull(param)]
    param2_values = [param for param in param2_values if pd.notnull(param)]
    
    # Sélection des 12 premières valeurs des paramètres
    param1_values = param1_values[:12]
    param2_values = param2_values[:12]
    
    # Sélection des colonnes (paramètres) pour chaque tableau
    param1_columns = selected_tableau1.columns.tolist()
    param2_columns = selected_tableau2.columns.tolist()
    
    # Sélection du paramètre pour le premier paramètre
    selected_param1 = st.selectbox('Choisir un paramètre pour le premier paramètre', param1_columns)
    
    # Sélection du paramètre pour le deuxième paramètre
    selected_param2 = st.selectbox('Choisir un paramètre pour le deuxième paramètre', param2_columns)
    
    # Bouton de calcul
    calculate_button = st.button('Calculer')
    
    # Vérification si le bouton de calcul a été cliqué
    if calculate_button:
        # Calcul du KPI
        kpi_values = calculate_kpi(param1_values, param2_values)
        
        # Affichage du tableau de résultats
        st.write('Résultats du KPI :')
        result_df = pd.DataFrame({selected_param1: param1_values, selected_param2: param2_values, 'KPI': kpi_values})
        st.write(result_df.dropna())  # Affichage des lignes non vides uniquement
        
        # Affichage du graphe
        st.write('Graphe du KPI :')
        plt.plot(result_df.dropna()['KPI'])
        plt.xlabel('Index')
        plt.ylabel('KPI')
        st.pyplot(plt)
