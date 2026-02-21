import streamlit as st
import pandas as pd
st.title ("Dashboard customer shopping")

# Cargar datos
df = pd.read_csv("custumer_shopping_data.csv")

st.write("Vista previa del dataset:")
st.dataframe(df.head())
