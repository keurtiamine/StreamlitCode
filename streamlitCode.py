import streamlit as st
from pdf2image import convert_from_path

# Titre de l'interface graphique
st.title("Affichage d'un PDF")

# Chemin vers le fichier PDF
pdf_path = "SCHEMA BOUCLE EAU VAPEUR.pdf"

# Conversion du PDF en images
images = convert_from_path(pdf_path)

# Affichage des images
for i, image in enumerate(images):
    st.image(image, caption=f"Page {i+1}", use_column_width=True)
