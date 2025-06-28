import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(page_title="Amenazada y Dispersada", layout="wide")

# === Ocultar sidebar y header ===
st.markdown("""
    <style>
    [data-testid="stSidebar"], header[data-testid="stHeader"] {
        display: none !important;
    }
    .block-container {
        padding: 0rem 2rem 2rem 2rem;
    }
    </style>
""", unsafe_allow_html=True)
# === Fondo y estilo ===
def set_background(img_file):
    with open(img_file, "rb") as img:
        b64 = base64.b64encode(img.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)),
                        url('data:image/jpeg;base64,{b64}') no-repeat center center fixed;
            background-size: cover;
        }}
        [data-testid="stSidebar"] {{
            visibility: hidden;
            display: none;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("imagen principal.jpeg")

# === Ocultar sidebar y header ===
st.markdown("""
    <style>
    [data-testid="stSidebar"], header[data-testid="stHeader"] {
        display: none !important;
    }
    .block-container {
        padding: 0rem 2rem 2rem 2rem;
    }
    </style>
""", unsafe_allow_html=True)
# === Título y botón volver ===
st.markdown("<h2 style='text-align:center;'>🐾🌲 AMENAZADA Y DISPERSADA</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)

st.markdown("""
    <form action='/tematicas' method='get'>
        <button style='
            margin-top: 30px;
            padding: 12px 25px;
            background-color: #0A2540;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
        '>🔙 Volver a Temáticas</button>
    </form>
""", unsafe_allow_html=True)

# === Separación visual antes de la tarjeta ===
st.markdown("<br>", unsafe_allow_html=True)

# === Cargar y limpiar datos ===
df = pd.read_csv("data_vinculacion/Amanzada y Dispersa.csv", sep=";", encoding="utf-8")
df.columns = df.columns.str.strip()
df["DENSIDAD"] = df["DENSIDAD"].str.replace(",", ".", regex=False).astype(float)
df["AREA__Ha_"] = df["AREA__Ha_"].astype(float)
df["POBLACIÓN TOTAL"] = df["POBLACIÓN TOTAL"].astype(int)

# === Tarjeta POBLACIÓN ===
poblacion_total = df["POBLACIÓN TOTAL"].sum()
st.markdown(f"""
    <div style="padding: 25px; background-color: rgba(255,255,255,0.4); border-radius: 12px; text-align: center; margin-bottom: 20px;">
        <h4 style="color:#0A2540;">POBLACIÓN TOTAL</h4>
        <h1 style="color:#0A2540;">{poblacion_total:,}</h1>
    </div>
""", unsafe_allow_html=True)

# === Filtros debajo de la tarjeta ===
col1, col2 = st.columns(2)
with col1:
    sectores = st.selectbox("Selecciona el tipo de SECTOR", ["Todos"] + sorted(df["SECTORES"].unique()))
with col2:
    subsector = st.selectbox("Selecciona el SECTOR ANONIMIZADO", ["Todos"] + sorted(df["SECTOR ANONIMIZADOS"].astype(str).unique()))

# === Filtrar datos ===
filtro = df.copy()
if sectores != "Todos":
    filtro = filtro[filtro["SECTORES"] == sectores]
if subsector != "Todos":
    filtro = filtro[filtro["SECTOR ANONIMIZADOS"].astype(str) == subsector]

# === Agrupar por SECTORES para el gráfico de barras ===
agrupado = filtro.groupby("SECTORES", as_index=False)["AREA__Ha_"].sum()

# === Gráfico de Barras ===
st.markdown("### 📊 Área Total por Sector")
fig_bar = px.bar(
    agrupado,
    x="SECTORES",
    y="AREA__Ha_",
    color="SECTORES",
    text="AREA__Ha_",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig_bar.update_traces(textposition="outside")
fig_bar.update_layout(
    plot_bgcolor="rgba(255,255,255,0.1)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)
st.plotly_chart(fig_bar, use_container_width=True)

# === Gráfico Pie ===
st.markdown("### 🥧 Densidad por Sector")
fig_pie = px.pie(
    filtro,
    values="DENSIDAD",
    names="SECTORES",
    color_discrete_sequence=px.colors.qualitative.Set3
)
fig_pie.update_traces(textinfo='percent+label')
fig_pie.update_layout(
    plot_bgcolor="rgba(255,255,255,0.1)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)
st.plotly_chart(fig_pie, use_container_width=True)

# === Tabla Final ===
st.markdown("### 📋 Detalle de Sectores")
st.dataframe(
    filtro[["NOMBRE", "Nro.", "PARROQUIA", "POBLACIÓN TOTAL", "SECTOR ANONIMIZADOS", "SECTORES"]],
    use_container_width=True
)
