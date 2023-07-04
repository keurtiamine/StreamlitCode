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
            st.write("Les valeurs choisies ne doivent pas être des chaînes de caractères.")
            kpi_result.append(None)
    return kpi_result

# Interface utilisateur
st.title('Calcul du KPI')

# Chargement des tableaux à partir des fichiers Excel
tableau1 = pd.read_excel('tableau1.xlsx', skiprows=1, nrows=12)
tableau2 = pd.read_excel('tableau2.xlsx', skiprows=1, nrows=12)

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
    kpi_df = kpi_df.dropna()  # Supprimer les lignes avec des valeurs nulles (division par 0)
    st.write(kpi_df)

    # Affichage du graphe
    st.write('Graphe du KPI :')
    plt.plot(kpi_df['KPI'])
    plt.xlabel('Index')
    plt.ylabel('KPI')
    st.pyplot(plt)
