import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("customer_shopping_data.csv")
    
    df["invoice_date"] = pd.to_datetime(
        df["invoice_date"],
        dayfirst=True,
        errors="coerce"
    )
    
    return df

df = load_data()

st.title("Análisis de desempeño comercial y hábitos de compra - Centros comerciales")

# SIDEBAR - FILTROS
st.sidebar.header("Filtros")

genero = st.sidebar.multiselect(
    "Género",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

edad = st.sidebar.slider(
    "Rango de edad",
    int(df["age"].min()),
    int(df["age"].max()),
    (int(df["age"].min()), int(df["age"].max()))
)

metodo_pago = st.sidebar.multiselect(
    "Método de pago",
    options=df["payment_method"].unique(),
    default=df["payment_method"].unique()
)

categoria = st.sidebar.multiselect(
    "Categorías",
    options=df["category"].unique(),
    default=df["category"].unique()
)

# Aplicar filtros
df_filtrado = df[
    (df["gender"].isin(genero)) &
    (df["age"].between(edad[0], edad[1])) &
    (df["payment_method"].isin(metodo_pago)) &
    (df["category"].isin(categoria))
]

if df_filtrado.empty:
    st.warning("No hay datos con los filtros seleccionados.")
    st.stop()


# KPIs
col1, col2, col3, col4 = st.columns(4)

ticket_promedio = df_filtrado["price"].mean()

meses_unicos = df_filtrado["invoice_date"].dt.to_period("M").nunique()
frecuencia_compra = df_filtrado.shape[0] / meses_unicos if meses_unicos > 0 else 0

categoria_mayor = df_filtrado["category"].value_counts().idxmax()
metodo_pref = df_filtrado["payment_method"].value_counts().idxmax()

col1.metric("Ticket Promedio", f"${ticket_promedio:,.2f}")
col2.metric("Frecuencia compra (Prom/Mes)", round(frecuencia_compra, 2))
col3.metric("Categoría más demandada", categoria_mayor)
col4.metric("Método de pago preferido", metodo_pref)

st.markdown("---")

col_g1, col_g2 = st.columns(2)

# Centro comercial más visitado
with col_g1:
    st.subheader("Centro Comercial más visitado")
    mall_visitas = df_filtrado["shopping_mall"].value_counts()
    st.bar_chart(mall_visitas)

# Categorías por Mall (simplificado)
with col_g2:
    st.subheader("Categorías por Mall")
    categorias_mall = pd.crosstab(
        df_filtrado["shopping_mall"],
        df_filtrado["category"]
    )
    st.bar_chart(categorias_mall)

st.markdown("---")

col_g3, col_g4 = st.columns(2)

# Perfil del comprador por Mall
with col_g3:
    st.subheader("Perfil del comprador por Mall")
    perfil = pd.crosstab(
        df_filtrado["shopping_mall"],
        df_filtrado["gender"]
    )
    st.bar_chart(perfil)

# Top 5 categorías con mayor venta
with col_g4:
    st.subheader("Top 5 categorías con mayor venta")
    
    top_categorias = (
        df_filtrado
        .groupby("category")["price"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    st.bar_chart(top_categorias)