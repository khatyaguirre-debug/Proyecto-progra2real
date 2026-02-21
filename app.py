import streamlit as st
import pandas as pd
st.title ("Dashboard customer shopping")

# Cargar datos
df = pd.read_csv("customer_shopping_data.csv")

st.write("Vista previa del dataset:")
st.dataframe(df.head())

# Total ventas por shopping mall
ventas_mall = df.groupby("shopping_mall")["price"].sum()

st.subheader("Ventas por shopping mall")
st.bar_chart(ventas_mall)