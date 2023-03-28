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
