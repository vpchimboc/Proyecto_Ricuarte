import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(page_title="Suceptibilidad a Amenazas", layout="wide")

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

# === Fondo personalizado ===
def set_background(image_path):
    with open(image_path, "rb") as img_file:
        b64 = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)),
                        url("data:image/jpeg;base64,{b64}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("imagen principal.jpeg")

# === Título y botón de regreso ===
st.markdown("<h2 style='text-align:center; color:white;'>⚠️🌋 SUCEPTIBILIDAD A AMENAZAS</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid white;'>", unsafe_allow_html=True)

st.markdown("""
    <form action='/tematicas' method='get'>
        <button style='
            margin-top: 20px;
            margin-bottom: 30px;
            padding: 12px 25px;
            background-color: #0A2540;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
        '>🔙 Volver a Temáticas</button>
    </form>
""", unsafe_allow_html=True)

# === Cargar y limpiar datos ===
df = pd.read_csv("data_vinculacion/Suceptibilidad a amenazas.csv", sep=";", encoding="utf-8-sig")
df.columns = df.columns.str.strip()

# Convertir columnas numéricas
for col in df.columns:
    if 'Ha' in col or '%' in col:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors='coerce')

# === Selector ===
opciones = ["Todos"] + df["Susceptibilidad/Amenazas"].dropna().unique().tolist()
seleccion = st.selectbox("Selecciona un tipo de susceptibilidad:", opciones)

df_filtrado = df if seleccion == "Todos" else df[df["Susceptibilidad/Amenazas"] == seleccion]

# === Estilo de tarjetas ===
st.markdown("""
    <style>
    .card {
        background-color: rgba(255, 255, 255, 0.4);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: #001F54;
        font-weight: bold;
        font-family: 'sans-serif';
        font-size: 20px;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.3);
    }
    .card h1 {
        font-size: 48px;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# === Tarjetas ===
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="card">
            Área de Inundaciones (Ha)
            <h1>{df_filtrado['Área (Ha) inundaciones'].sum():,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="card">
            Área de Mov. de Masa (Ha)
            <h1>{df_filtrado['Área (Ha) movimientos de masa'].sum():,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="card">
            Remoción de Masas (Ha)
            <h1>{df_filtrado['SUPERFICIE (Ha) remocion de masas'].sum():,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

# === Colores del GAD Ricaurte ===
colores_gad = [
    "#2E3192", "#EC008C", "#00A79D", "#8DC63F", "#F7941E",
    "#662D91", "#C1272D", "#39B54A", "#00AEEF", "#F15A24"
]

# === Gráfico de ÁREAS (Ha) ===
df_areas = df_filtrado.melt(
    id_vars="Susceptibilidad/Amenazas",
    value_vars=["Área (Ha) inundaciones", "Área (Ha) movimientos de masa", "SUPERFICIE (Ha) remocion de masas"],
    var_name="Amenaza",
    value_name="Hectáreas"
)

st.markdown("<h4 style='color:white;'>Áreas Afectadas por Amenazas (Ha)</h4>", unsafe_allow_html=True)
fig1 = px.bar(
    df_areas,
    x="Susceptibilidad/Amenazas",
    y="Hectáreas",
    color="Amenaza",
    barmode="group",
    color_discrete_sequence=colores_gad
)
fig1.update_layout(
    plot_bgcolor="rgba(255,255,255,0.1)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)
st.plotly_chart(fig1, use_container_width=True)

# === Gráfico de PORCENTAJES (%) ===
df_porcentajes = df_filtrado.melt(
    id_vars="Susceptibilidad/Amenazas",
    value_vars=["% inundaciones", "% movimientos de masa", "% remocion de masas"],
    var_name="Amenaza",
    value_name="Porcentaje"
)

st.markdown("<h4 style='color:white;'>Porcentaje de Afectación por Amenazas</h4>", unsafe_allow_html=True)
fig2 = px.bar(
    df_porcentajes,
    x="Susceptibilidad/Amenazas",
    y="Porcentaje",
    color="Amenaza",
    barmode="group",
    color_discrete_sequence=colores_gad
)
fig2.update_layout(
    plot_bgcolor="rgba(255,255,255,0.1)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)
st.plotly_chart(fig2, use_container_width=True)
