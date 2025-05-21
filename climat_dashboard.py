import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tableau de bord climatique", layout="wide")
st.title("🌦️ Tableau de bord de suivi des performances climatiques")

uploaded_file = st.file_uploader("📁 Charger un fichier CSV contenant des données climatiques", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if 'Date' not in df.columns:
            st.error("Le fichier doit contenir une colonne 'Date'.")
        else:
            df['Date'] = pd.to_datetime(df['Date'])

            st.subheader("📅 Filtrage par plage de dates")
            min_date = df['Date'].min()
            max_date = df['Date'].max()
            start_date, end_date = st.date_input("Sélectionner une plage de dates", [min_date, max_date],
                                                 min_value=min_date, max_value=max_date)

            filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

            st.subheader("📊 Statistiques descriptives")
            st.write(filtered_df.describe())

            st.subheader("📈 Courbes de tendance")
            numeric_columns = filtered_df.select_dtypes(include='number').columns.tolist()

            if numeric_columns:
                selected_column = st.selectbox("Choisissez une variable à visualiser :", numeric_columns)
                fig = px.line(filtered_df, x='Date', y=selected_column, title=f"Tendance de {selected_column}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Aucune colonne numérique à afficher.")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
else:
    st.info("Veuillez charger un fichier CSV pour commencer.")
