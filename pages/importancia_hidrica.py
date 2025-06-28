import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(page_title="Importancia Hídrica", layout="wide")

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
# === Fondo ===
def set_background(img_file):
    with open(img_file, "rb") as img:
        b64 = base64.b64encode(img.read()).decode()
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
# === Estilo extra ===
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# === Título ===
st.markdown("<h2 style='text-align:center; color:white;'>💧 IMPORTANCIA HÍDRICA</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)

# === Botón volver ===
st.markdown("""
    <form action='/tematicas' method='get'>
        <button style='
            margin-top: 20px;
            padding: 10px 22px;
            background-color: #0A2540;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 15px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
        '>🔙 Volver a Temáticas</button>
    </form>
""", unsafe_allow_html=True)

# === Cargar y limpiar datos ===
df = pd.read_csv("data_vinculacion/Zonas importancia hidrica.csv", sep=";", encoding="utf-8")
df.columns = df.columns.str.strip()
df["Longitud"] = df["Longitud"].str.replace(",", ".").astype(float)
df["%"] = df["%"].str.replace(",", ".").astype(float)

# === Filtro ===
quebradas = ["Todas"] + sorted(df["Nombre de quebrada"].unique())
seleccion = st.selectbox("Quebradas", quebradas)

df_filtrado = df if seleccion == "Todas" else df[df["Nombre de quebrada"] == seleccion]

# === Colores del GAD ===
colores_gad = [
    "#2E3192", "#EC008C", "#00A79D", "#8DC63F", "#F7941E",
    "#662D91", "#C1272D", "#39B54A", "#00AEEF", "#F15A24"
]

# === Gráfico de barras ===
fig_bar = px.bar(
    df_filtrado,
    x="Nombre de quebrada",
    y="Longitud",
    text="Longitud",
    color="Nombre de quebrada",
    color_discrete_sequence=colores_gad
)
fig_bar.update_layout(
    title="LONGITUD POR QUEBRADAS",
    title_font_color="white",
    plot_bgcolor="rgba(255,255,255,0.1)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    showlegend=False
)
fig_bar.update_traces(textposition="outside")

# === Gráfico circular ===
fig_pie = px.pie(
    df_filtrado,
    values="%",
    names="Nombre de quebrada",
    color_discrete_sequence=colores_gad
)
fig_pie.update_layout(
    title="PORCENTAJE DEL TOTAL DE TERRITORIO OCUPADO POR QUEBRADAS",
    title_font_color="white",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)

# === Mostrar gráficos ===
st.plotly_chart(fig_bar, use_container_width=True)
st.plotly_chart(fig_pie, use_container_width=True)
