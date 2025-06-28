import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(page_title="Uso del Territorio", layout="wide")

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

# === Encabezado ===
st.markdown("<h2 style='text-align:center; color:white;'>🌍📐 USO DEL TERRITORIO</h2>", unsafe_allow_html=True)
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

# === Colores del GAD ===
colores_gad = [
    "#2E3192", "#EC008C", "#00A79D", "#8DC63F", "#F7941E",
    "#662D91", "#C1272D", "#39B54A", "#00AEEF", "#F15A24"
]

# === Cargar y limpiar datos ===
df = pd.read_csv("data_vinculacion/Uso de territorio.csv", sep=";", encoding="utf-8")
df.columns = df.columns.str.strip()

df["AREA"] = df["AREA"].str.replace(",", ".", regex=False).astype(float)
df["% Territorio"] = df["% Territorio"].str.replace(",", ".", regex=False).astype(float)

# === Filtro de categoría ===
categoria = st.selectbox("CATEGORÍA", ["Todas"] + df["Uso de suelo principal"].unique().tolist())
df_filtrado = df if categoria == "Todas" else df[df["Uso de suelo principal"] == categoria]

# === Tarjetas ===
total_area = df_filtrado["AREA"].sum()
total_porcentaje = df_filtrado["% Territorio"].sum()

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
        <div style="padding: 25px; background-color: rgba(255,255,255,0.4); border-radius: 12px; text-align: center;">
            <h4 style="color:#0A2540;">ÁREA</h4>
            <h1 style="color:#0A2540;">{total_area:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style="padding: 25px; background-color: rgba(255,255,255,0.4); border-radius: 12px; text-align: center;">
            <h4 style="color:#0A2540;">TERRITORIO</h4>
            <h1 style="color:#0A2540;">{total_porcentaje:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

# === Transformación para gráfico combinado ===
df_melted = df_filtrado.melt(
    id_vars=["Uso de suelo principal"],
    value_vars=["AREA", "% Territorio"],
    var_name="Variable",
    value_name="Valor"
)

# === Gráfico de barras agrupadas ===
fig = px.bar(
    df_melted,
    x="Uso de suelo principal",
    y="Valor",
    color="Variable",
    barmode="group",
    text="Valor",
    color_discrete_sequence=["#2E3192", "#EC008C"]
)

fig.update_traces(textposition="outside")

fig.update_layout(
    title="Distribución del Uso del Territorio",
    title_font_color="white",
    plot_bgcolor="rgba(255,255,255,0.1)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    xaxis_title="USO DEL TERRITORIO",
    yaxis_title="VALOR",
    legend_title_text="Tipo de Dato"
)

st.plotly_chart(fig, use_container_width=True)
