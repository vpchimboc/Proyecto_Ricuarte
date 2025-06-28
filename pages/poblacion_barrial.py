import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# === Configuración de la página (colapsar el sidebar de entrada) ===
st.set_page_config(page_title="Población Barrial - Ricaurte", layout="wide", initial_sidebar_state="collapsed")

# === Fondo personalizado y estilos globales ===
def set_background(image_path):
    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)),
                        url("data:image/jpg;base64,{img_base64}") no-repeat center center fixed;
            background-size: cover;
        }}
        .card {{
            background-color: rgba(255, 255, 255, 0.4);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.0);
        }}
        .card h1, .card h3 {{
            color: #002B5B;
            font-weight: bold;
        }}
        h1, h2, h3, .stTextInput > div > div {{
            color: white;
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

# === Botón de regreso ===
st.markdown("""
    <form action='/tematicas' method='get'>
        <button style='margin-bottom: 20px; padding: 10px 30px; font-size: 18px; border-radius: 10px; background-color: #002B5B; color: white; border: none;'>
            🔙 Volver a Temáticas
        </button>
    </form>
""", unsafe_allow_html=True)

# === Corrección de caracteres mal codificados en los datos ===
reemplazos = {
    "Ã“": "Ó", "Ãš": "Ú", "Ã‰": "É", "Ã": "Á", "â€“": "-",
    "Ã‘": "Ñ", "â€œ": '"', "â€": '"', "â€˜": "'", "â€™": "'",
    "â€": '"', "Â": "", "Ã­n": "ÍN", "Ã³": "ó", "Ã¡": "á",
    "Ã­": "í", "Ã©": "é", "Ã¨": "è", "Ãº": "ú", "Ã±": "ñ", "Ã¼": "ü"
}

def limpiar_texto(texto):
    if isinstance(texto, str):
        for k, v in reemplazos.items():
            texto = texto.replace(k, v)
    return texto

# === Cargar y preparar los datos ===
df = pd.read_csv("tablas_vinculacion/Datos barriales.csv", sep=";", encoding="utf-8-sig")

# Limpiar y estandarizar nombres de columnas (manteniendo snake_case)
df.columns = [col.strip().replace("Ã“", "Ó").replace("Ãš", "Ú")
              .replace("Ã", "Á").replace("Ã­n", "ÍN")
              .replace(" ", "_").lower() for col in df.columns]

# Limpiar solo los valores de la columna barrio
df["barrio"] = df["barrio"].apply(limpiar_texto)

# Convertir columnas numéricas
df["población_total_censo_2022"] = df["población_total_censo_2022"].replace(',', '.', regex=True).astype(float)
df["pea"] = pd.to_numeric(df["pea"], errors='coerce')

# === Selector de barrio ===
barrios = df["barrio"].dropna().unique()
barrio_sel = st.selectbox("Selecciona un barrio:", sorted(barrios))

# === Tarjetas ===
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div class='card'><h3>🏘️ Barrio seleccionado</h3><h1>{barrio_sel}</h1></div>", unsafe_allow_html=True)
with col2:
    poblacion_barrio = int(df[df["barrio"] == barrio_sel]["población_total_censo_2022"].sum())
    st.markdown(f"<div class='card'><h3>👥 Población presente</h3><h1>{poblacion_barrio:,}</h1></div>", unsafe_allow_html=True)

st.markdown("### ")

# === Colores institucionales GAD ===
colores_gad = ['#0F5B97', '#A3007D', '#02A9A8', '#F37020', '#6E2594', '#8CC63F', '#F15A24', '#F7E017']

# === Gráfico 1: PEA por barrio ===
df_pea = df.groupby("barrio")["pea"].sum().reset_index().sort_values("pea", ascending=False)
fig_pea = px.bar(df_pea, x="barrio", y="pea", title="Población Económicamente Activa por Barrio",
                 color="barrio", color_discrete_sequence=colores_gad)
fig_pea.update_layout(
    showlegend=True,
    legend_title_text='Barrios',
    paper_bgcolor='rgba(255,255,255,0.0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title_font_color='white',
    xaxis=dict(showticklabels=False)
)
st.plotly_chart(fig_pea, use_container_width=True)

# === Gráfico 2: Población total por barrio ===
df_total = df.groupby("barrio")["población_total_censo_2022"].sum().reset_index()
fig_total = px.pie(df_total, names="barrio", values="población_total_censo_2022",
                   title="Población Total por Barrio", hole=0.4,
                   color_discrete_sequence=colores_gad)
fig_total.update_layout(paper_bgcolor='rgba(255,255,255,0.0)', title_font_color='white')
st.plotly_chart(fig_total, use_container_width=True)

# === Gráfico 3: Jerarquización ===
df_jerarq = df.groupby("jerarquizacion_de_centros_poblados")["barrio"].count().reset_index()
df_jerarq.columns = ["jerarquizacion", "cantidad"]
fig_jer = px.bar(df_jerarq.sort_values("cantidad", ascending=False),
                 x="cantidad", y="jerarquizacion", orientation="h",
                 title="Jerarquización del Centro Poblado",
                 color="jerarquizacion", color_discrete_sequence=colores_gad)
fig_jer.update_layout(
    paper_bgcolor='rgba(255,255,255,0.0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title_font_color='white'
)
st.plotly_chart(fig_jer, use_container_width=True)
