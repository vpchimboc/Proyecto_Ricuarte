import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(page_title="Discapacidades Generales", layout="wide")
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

# Título y botón
st.markdown("<h2 style='text-align:center; color:white;'>♿ DISCAPACIDADES GENERALES</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)

st.markdown("""
    <form action='/tematicas' method='get'>
        <button style='
            margin-bottom: 20px;
            padding: 10px 20px;
            background-color: #001f3f;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
        '>
            🔙 Volver a Temáticas
        </button>
    </form>
""", unsafe_allow_html=True)

# Cargar datos
df = pd.read_csv("data_vinculacion/Discapacidad general.csv", encoding="utf-8-sig", sep=";")
df.columns = df.columns.str.strip()
df = df.dropna(subset=["Variables"])

# Fila con selector y tarjeta
col_sel, col_card = st.columns([2, 1])

with col_sel:
    opciones = ["Todas"] + [x for x in df["Variables"] if x.startswith("TOTAL DISCAPACIDAD")]
    seleccion = st.selectbox("Discapacidad específica", opciones)

with col_card:
    if seleccion == "Todas":
        total = df[df["Variables"].str.startswith("TOTAL DISCAPACIDAD")]["Total"].sum()
    else:
        total = int(df[df["Variables"] == seleccion]["Total"].values[0])

    st.markdown(f"""
        <div style='
            background-color: rgba(255,255,255,0.4);
            padding: 30px;
            border-radius: 10px;
            color: #001f3f;
            text-align: center;
        '>
            <h4>POBLACIÓN CON DISCAPACIDAD</h4>
            <h1>{total}</h1>
        </div>
    """, unsafe_allow_html=True)

# Donuts
df_mujer = df.copy()
df_hombre = df.copy()

if seleccion != "Todas":
    df_mujer = df_mujer[df_mujer["Variables"] == seleccion]
    df_hombre = df_hombre[df_hombre["Variables"] == seleccion]

fig_mujer = px.pie(df_mujer, names="Variables", values="Mujer", hole=0.5, title="DISCAPACIDAD MUJERES")
fig_mujer.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='white')
fig_mujer.update_traces(textinfo='value+percent', marker=dict(line=dict(color='#000000', width=1)))

fig_hombre = px.pie(df_hombre, names="Variables", values="Hombre", hole=0.5, title="DISCAPACIDAD HOMBRES")
fig_hombre.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='white')
fig_hombre.update_traces(textinfo='value+percent', marker=dict(line=dict(color='#000000', width=1)))

col3, col4 = st.columns(2)
col3.plotly_chart(fig_mujer, use_container_width=True)
col4.plotly_chart(fig_hombre, use_container_width=True)

# === Gráfico de Discapacidad por Barrio ===

# Diccionario de nombres legibles
nombres_visuales = {
    "discapacidad_visual": "Discapacidad Visual",
    "discapacidad_psicosocial": "Discapacidad Psicosocial",
    "discapacidad_motriz": "Discapacidad Motriz",
    "discapacidad_auditiva": "Discapacidad Auditiva",
    "discapacidad_cognitiva": "Discapacidad Cognitiva"
}

# Cargar y limpiar datos de barrios
df_barrios = pd.read_csv("tablas_vinculacion/Datos barriales.csv", sep=";", encoding="utf-8-sig")

reemplazos = {
    "Ã“": "Ó", "Ãš": "Ú", "Ã‰": "É", "Ã": "Á", "â€“": "-", "Ã‘": "Ñ", "â€œ": '"',
    "â€": '"', "â€˜": "'", "â€™": "'", "â€": '"', "Â": "", "Ã­n": "ÍN", "Ã³": "ó",
    "Ã¡": "á", "Ã­": "í", "Ã©": "é", "Ã¨": "è", "Ãº": "ú", "Ã±": "ñ", "Ã¼": "ü"
}

def limpiar_texto(texto):
    if isinstance(texto, str):
        for k, v in reemplazos.items():
            texto = texto.replace(k, v)
    return texto

df_barrios.columns = [col.strip().lower().replace(" ", "_") for col in df_barrios.columns]
df_barrios["barrio"] = df_barrios["barrio"].apply(limpiar_texto)

# Selector para discapacidad por barrio
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3 style='color:white;'>📍 Distribución de Discapacidad por Barrio</h3>", unsafe_allow_html=True)

col_sel_barrio, col_grafico = st.columns([1, 4])

with col_sel_barrio:
    seleccion_barrio = st.selectbox("Tipo de discapacidad", options=list(nombres_visuales.keys()),
                                    format_func=lambda x: nombres_visuales[x])

# Generar gráfico
df_filtrado = df_barrios[["barrio", seleccion_barrio]].copy()
df_filtrado = df_filtrado[df_filtrado[seleccion_barrio] > 0]

fig_barrios = px.pie(df_filtrado, names="barrio", values=seleccion_barrio, hole=0.5,
                     title=nombres_visuales[seleccion_barrio])
fig_barrios.update_layout(
    height=600,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title_font_color='white',
    legend_title_text='Barrio'
)
fig_barrios.update_traces(textinfo='value+percent', marker=dict(line=dict(color='#000000', width=1)))

with col_grafico:
    st.plotly_chart(fig_barrios, use_container_width=True)
