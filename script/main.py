import streamlit as st
import pandas as pd

def main():
    st.title("OCP - Bilan Annuel")

    # Upload the first Excel file
    st.subheader("Energie Electrique")
    energie_electrique_file = st.file_uploader("Upload Excel file", type=["xlsx"], key=1)
    if energie_electrique_file is not None:
        energie_electrique_df = pd.read_excel(energie_electrique_file)
        st.write("File uploaded successfully.")
        st.write("File Name:", energie_electrique_file.name)
        st.write("Data Frame:")
        st.write(energie_electrique_df)

    # Upload the second Excel file
    st.subheader("Vapeur HP")
    vapeur_hp_file = st.file_uploader("Upload Excel file", type=["xlsx"], key=2)
    if vapeur_hp_file is not None:
        vapeur_hp_df = pd.read_excel(vapeur_hp_file)
        st.write("File uploaded successfully.")
        st.write("File Name:", vapeur_hp_file.name)
        st.write("Data Frame:")
        st.write(vapeur_hp_df)



if __name__ == "__main__":
    main()
