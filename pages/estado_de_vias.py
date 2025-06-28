import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# Configuración de página
st.set_page_config(page_title="Estado de Vías", layout="wide")

# Ocultar sidebar y header
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

# Fondo personalizado
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
        h1, h2, h3, h4, h5, h6 {{
            color: white !important;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("imagen principal.jpeg")

# Título
st.markdown("<h2 style='text-align:center;'>🛣️ ESTADO DE VÍAS</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)

# Botón volver
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
        '>
            🔙 Volver a Temáticas
        </button>
    </form>
""", unsafe_allow_html=True)



# Cargar datos
materiales = pd.read_csv("data_vinculacion/Material de las Vías.csv", sep=";", encoding="utf-8-sig")
estado = pd.read_csv("data_vinculacion/Estado de las vias.csv", sep=";", encoding="utf-8-sig")

# Limpiar materiales
materiales = materiales.dropna()
materiales = materiales[materiales["Capa de Rodadura"].str.lower() != "total"]
materiales["Longitud (km)"] = materiales["Longitud (km)"].str.replace(",", ".").astype(float)

# Limpiar estado
estado["Longitud (m)"] = estado["Longitud (m)"].str.replace(",", ".").astype(float)

# Colores del GAD Ricaurte
colores_gad = ["#2E3192", "#00AEEF", "#39B54A", "#F7941E", "#EC008C", "#662D91"]

# Gráfico circular (material de vías)
fig_material = px.pie(
    materiales,
    names="Capa de Rodadura",
    values="Longitud (km)",
    color_discrete_sequence=colores_gad,
    title="LONGITUD VIAL DEL MATERIAL POR METROS",
)
fig_material.update_traces(textinfo='percent+value', textfont_size=14)
fig_material.update_layout(
    title_font_color="white",
    paper_bgcolor="rgba(255,255,255,0.0)",
    font_color="black"
)

# Gráfico de barras (estado de vías)
fig_estado = px.bar(
    estado,
    x="Estado",
    y="Longitud (m)",
    text="Longitud (m)",
    color="Estado",
    color_discrete_sequence=colores_gad
)
fig_estado.update_traces(textposition="outside")
fig_estado.update_layout(
    title="LONGITUD VIAL POR METROS",
    title_font_color="white",
    plot_bgcolor="rgba(255,255,255,0.0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    showlegend=False
)

# Mostrar en columnas
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_material, use_container_width=True)
with col2:
    st.plotly_chart(fig_estado, use_container_width=True)
