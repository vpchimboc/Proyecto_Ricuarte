import streamlit as st
import base64
import os
import unicodedata

st.set_page_config(page_title="Temáticas - Ricaurte", layout="wide")
# Ocultar sidebar completamente desde el inicio
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Función para convertir imagen a base64
def img_to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# Función para limpiar tildes y generar rutas válidas
def limpiar_ruta(nombre):
    nfkd = unicodedata.normalize('NFKD', nombre)
    sin_tildes = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return sin_tildes.lower().replace(" ", "_")

# Fondo personalizado
background_image = "imagen principal.jpeg"
if os.path.exists(background_image):
    b64_bg = img_to_base64(background_image)
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)),
                        url('data:image/jpeg;base64,{b64_bg}') no-repeat center center fixed;
            background-size: cover;
        }}
        .tarjeta-tema {{
            background-color: rgba(255, 255, 255, 0.4);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.5);
            backdrop-filter: blur(6px);
            width: 100%;
            height: 160px;
            transition: 0.3s;
        }}
        .tarjeta-tema:hover {{
            transform: scale(1.03);
            cursor: pointer;
            background-color: rgba(255, 255, 255, 0.6);
        }}
        .tarjeta-tema h5 {{
            color: #0A2540 !important;
            font-size: 16px;
            font-weight: bold;
            margin-top: 8px;
        }}
        .tarjeta-tema img {{
            width: 40px;
            height: 40px;
        }}
        section[data-testid="stSidebar"] > div:first-child {{
            background-color: #f37020;
        }}
        </style>
    """, unsafe_allow_html=True)


st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True) 
st.markdown("""
    <form action='/' method='get'>
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
            🏠 Volver al Inicio
        </button>
    </form>
""", unsafe_allow_html=True)

# Diccionario de temáticas y archivos de imagen
tematicas = [
    ("Población Barrial", "poblacion_barrial.png"),
    ("Discapacidades Generales", "discapacidades.png"),
    ("Establecimientos Educativos", "educativos.png"),
    ("Analfabetismo", "analfabetismo.png"),
    ("Estado de Vías", "estado_vias.png"),
    ("Suceptibilidad a Amenazas", "suseptibilidad.png"),
    ("Uso del Territorio", "territorio.png"),
    ("Importancia Hídrica", "hidrica.png"),
    ("Amenazada y Dispersada", "amanzadas.png"),
]

# Cargar imágenes en base64
imagenes = {nombre: img_to_base64(f"img_tematicas/{archivo}") for nombre, archivo in tematicas}

# Título
st.markdown("<h2 style='text-align:center;'>📌 TEMÁTICAS DE RICAURTE</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)

# Primera fila (4 tarjetas)
cols1 = st.columns(4)
for i in range(4):
    nombre, _ = tematicas[i]
    ruta = limpiar_ruta(nombre)
    img_b64 = imagenes[nombre]
    with cols1[i]:
        st.markdown(f"""
            <form action='/{ruta}' method='get'>
                <button class='tarjeta-tema'>
                    <img src="data:image/png;base64,{img_b64}" alt="{nombre}">
                    <h5>{nombre.upper()}</h5>
                </button>
            </form>
        """, unsafe_allow_html=True)

# Espacio entre filas
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# Segunda fila (5 tarjetas)
cols2 = st.columns(5)
for i in range(4, 9):
    nombre, _ = tematicas[i]
    ruta = limpiar_ruta(nombre)
    img_b64 = imagenes[nombre]
    with cols2[i - 4]:
        st.markdown(f"""
            <form action='/{ruta}' method='get'>
                <button class='tarjeta-tema'>
                    <img src="data:image/png;base64,{img_b64}" alt="{nombre}">
                    <h5>{nombre.upper()}</h5>
                </button>
            </form>
        """, unsafe_allow_html=True)

# Sidebar GAD
from gad_sidebar import show_gad_sidebar
show_gad_sidebar()
