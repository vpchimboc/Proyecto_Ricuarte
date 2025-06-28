import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# === Configuración de página ===
st.set_page_config(page_title="ESTABLECIMIENTOS EDUCATIVOS", layout="wide")

# === Ocultar el sidebar completamente ===
st.markdown("""
    <style>
    [data-testid="stSidebar"], header[data-testid="stHeader"] > div:first-child {
        display: none !important;
    }
    button[kind="header"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# === Fondo personalizado ===
def set_background(img_file):
    with open(img_file, "rb") as img:
        b64 = base64.b64encode(img.read()).decode()
    style = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)),
                    url('data:image/jpeg;base64,{b64}') no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

set_background("imagen principal.jpeg")

# === Ocultar el sidebar completamente ===
st.markdown("""
    <style>
    [data-testid="stSidebar"], header[data-testid="stHeader"] > div:first-child {
        display: none !important;
    }
    button[kind="header"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# === Título y botón ===
st.markdown("<h2 style='text-align:center; color:white; font-weight:bold; font-size:32px;'>🏫 ESTABLECIMIENTOS EDUCATIVOS</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)

st.markdown("""
    <form action='/tematicas' method='get'>
        <button style='
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #0A2540;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
        '>🔙 Volver a Temáticas</button>
    </form>
""", unsafe_allow_html=True)

# === Cargar datos ===
df = pd.read_csv("data_vinculacion/Establecimientos educativos.csv", sep=";", encoding="utf-8-sig")
df.columns = df.columns.str.strip()

# === Selectores ===
col1, col2, col3 = st.columns(3)

with col1:
    admin = st.selectbox("TIPO DE ADMINISTRACIÓN", ["Todas"] + sorted(df["ADMINISTRACIÓN"].dropna().unique().tolist()))

with col2:
    tipo_estable = st.selectbox("TIPO DE ESTABLECIMIENTO", ["Todas"] + sorted(df["TIPO DE ESTABLECIMIENTO"].dropna().unique().tolist()))

with col3:
    barrio = st.selectbox("BARRIO", ["Todas"] + sorted(df["BARRIO"].dropna().unique().tolist()))

# === Filtro de datos ===
df_filtrado = df.copy()
if admin != "Todas":
    df_filtrado = df_filtrado[df_filtrado["ADMINISTRACIÓN"] == admin]
if tipo_estable != "Todas":
    df_filtrado = df_filtrado[df_filtrado["TIPO DE ESTABLECIMIENTO"] == tipo_estable]
if barrio != "Todas":
    df_filtrado = df_filtrado[df_filtrado["BARRIO"] == barrio]

# === Gráficos ===
col4, col5 = st.columns(2)

with col4:
    fig_nivel = px.histogram(df_filtrado, x="BARRIO", color="NIVEL",
                              title="NIVEL SEGÚN BARRIOS", barmode="group")
    fig_nivel.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(255,255,255,0.4)',
        title_font_color='white',
        title_font_size=20,
        title_font_family="Arial Black"
    )
    st.plotly_chart(fig_nivel, use_container_width=True)

with col5:
    fig_jornada = px.histogram(df_filtrado, x="BARRIO", color="JORNADA",
                                title="JORNADA SEGÚN BARRIOS", barmode="group")
    fig_jornada.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(255,255,255,0.4)',
        title_font_color='white',
        title_font_size=20,
        title_font_family="Arial Black"
    )
    st.plotly_chart(fig_jornada, use_container_width=True)

# === Estilo personalizado para DataFrame ===
st.markdown("""
    <style>
    /* Fondo blanco translúcido para la tabla */
    div[data-testid="stDataFrame"] div[role="grid"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px;
        color: #0A2540 !important;
        font-weight: 600;
    }

    /* Encabezado de columnas */
    div[data-testid="stDataFrame"] thead tr th {
        background-color: rgba(255, 255, 255, 0.4) !important;
        color: #0A2540 !important;
        font-size: 14px;
        font-weight: bold;
        border-bottom: 1px solid #ccc;
    }

    /* Celdas */
    div[data-testid="stDataFrame"] td {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #0A2540 !important;
    }

    /* Scroll personalizado */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(10, 37, 64, 0.5);
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# === Mostrar tabla ===
st.markdown("<h4 style='text-align:center; color:white;'>📊 ESTABLECIMIENTOS EDUCATIVOS</h4>", unsafe_allow_html=True)
st.dataframe(df_filtrado, use_container_width=True)
