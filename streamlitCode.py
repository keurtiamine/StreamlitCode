import streamlit as st
import pandas as pd

# Titre de la page
st.title("Visualisation de données Excel sur Streamlit")

# Sélectionner le fichier Excel à partir de l'interface graphique
file = st.file_uploader("Sélectionnez le fichier Excel", type=["xls", "xlsx"])

if file is not None:
    # Charger le fichier Excel en utilisant pandas
    df = pd.read_excel(file)

    # Afficher les données dans l'interface graphique
    st.write("## Aperçu des données : ")
    st.write(df.head())

    # Afficher les statistiques descriptives des données
    st.write("## Statistiques descriptives : ")
    st.write(df.describe())

    # Sélectionner une colonne pour l'afficher dans un graphique à barres
    column = st.selectbox("Sélectionner une colonne pour l'afficher dans un graphique à barres", df.columns)
    st.bar_chart(df[column].value_counts())

    # Afficher un histogramme pour chaque colonne numérique
    num_cols = df.select_dtypes(include=["float", "int"]).columns
    for col in num_cols:
        st.write(f"## Histogramme de {col} : ")
        st.hist_chart(df[col])


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Chargement des données depuis un fichier Excel
df = pd.read_excel('donnees_energie.xlsx')

# Affichage du titre de l'interface graphique
st.title('Pilotage de la production d\'énergie dans une usine')

# Widget de sélection de la plage de temps
start_date = st.sidebar.date_input('Date de début', value=df['Date'].min())
end_date = st.sidebar.date_input('Date de fin', value=df['Date'].max())

# Sélection des données dans la plage de temps sélectionnée
mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
df_filtered = df.loc[mask]

# Affichage d'un graphique de la consommation d'énergie en fonction du temps
fig, ax = plt.subplots()
ax.plot(df_filtered['Date'], df_filtered['Consommation'])
ax.set(xlabel='Date', ylabel='Consommation d\'énergie',
       title='Consommation d\'énergie au fil du temps')
ax.grid()
st.pyplot(fig)

# Widget de sélection du type d'énergie
energie_type = st.sidebar.selectbox('Type d\'énergie', ('Vapeur', 'Electricité'))

# Affichage d'un graphique de la production d'énergie en fonction du temps pour le type d'énergie sélectionné
fig2, ax2 = plt.subplots()
ax2.plot(df_filtered['Date'], df_filtered[energie_type])
ax2.set(xlabel='Date', ylabel='Production d\'énergie',
       title='Production d\'énergie au fil du temps - ' + energie_type)
ax2.grid()
st.pyplot(fig2)
