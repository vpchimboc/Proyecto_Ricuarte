import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# Configuración inicial
st.set_page_config(page_title="Analfabetismo por Grupo de Edad", layout="wide")

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
def set_background(image_path):
    with open(image_path, "rb") as f:
        b64_img = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)),
                        url("data:image/jpeg;base64,{b64_img}") no-repeat center center fixed;
            background-size: cover;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: white !important;
        }}
        </style>
    """, unsafe_allow_html=True)

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
st.markdown("<h2 style='text-align: center; color: white;'>📊 POBLACIÓN ANALFABETA POR GRUPO DE EDAD</h2>", unsafe_allow_html=True)
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
df = pd.read_csv("data_vinculacion/Analfabetismo.csv", sep=";", encoding="utf-8-sig")
df.columns = df.columns.str.strip()

# Ordenar por población analfabeta
df = df.sort_values(by="Población analfabeta", ascending=False)

# === Selector de grupo de edad ===
grupos = ["Todos"] + df["Grupo de edad"].unique().tolist()
opcion = st.selectbox("Selecciona un grupo de edad:", grupos)

if opcion != "Todos":
    df_filtrado = df[df["Grupo de edad"] == opcion]
else:
    df_filtrado = df

# === Colores del GAD Ricaurte ===
colores_gad = [
    "#2E3192",  # azul
    "#EC008C",  # rosado
    "#00A79D",  # verde agua
    "#8DC63F",  # verde claro
    "#F7941E",  # naranja
    "#662D91",  # morado
    "#C1272D",  # rojo
    "#39B54A",  # verde
    "#00AEEF",  # celeste
    "#F15A24"   # naranja fuerte
]

# === Gráfico ===
fig = px.bar(
    df_filtrado,
    x="Grupo de edad",
    y="Población analfabeta",
    text="Población analfabeta",
    color="Grupo de edad" if opcion == "Todos" else None,
    color_discrete_sequence=colores_gad
)

fig.update_traces(textposition='outside')

fig.update_layout(
    title="Distribución del Analfabetismo por Grupos Etarios",
    title_font_color="white",
    plot_bgcolor="rgba(255,255,255,0.4)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    xaxis_title="Grupo de edad",
    yaxis_title="Población analfabeta",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
