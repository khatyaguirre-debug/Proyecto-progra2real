import streamlit as st
import pandas as pandas
st.title ("Dashboard custumer shopping")

# Cargar datos
df = pd.read_csv("custumer_shopping_data.csv")

st.write("Vista previa del dataset:")
st.dataframe(df.head())
