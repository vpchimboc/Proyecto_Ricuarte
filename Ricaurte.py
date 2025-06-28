import streamlit as st
from PIL import Image
import base64
import os

st.set_page_config(page_title="Ricaurte", layout="wide")
# Ocultar sidebar completamente desde el inicio
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

def load_image_as_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Cargar imágenes
background_image = "imagen principal.jpeg"
logo_gad = "logo_gad.png"
logo_tec = "logo.png"
logo_fb = "logo_fb.png"
logo_ig = "logo_ig.png"
logo_tw = "logo_tw.png"

# Fondo y estilos
if os.path.exists(background_image):
    b64_bg = load_image_as_base64(background_image)
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)),
                        url('data:image/jpeg;base64,{b64_bg}') no-repeat center center fixed;
            background-size: cover;
        }}
        .menu-container {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 30px;
            flex-wrap: wrap;
        }}
        .menu-button {{
            width: 280px;
            height: 150px;
            background-color: #e3f2fd;
            border: 2px solid #1a237e;
            border-radius: 20px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: black;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 4px 4px 8px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }}
        .menu-button:hover {{
            transform: scale(1.05);
            background-color: #bbdefb;
        }}
        .logo-centered {{
            text-align: center;
            margin-top: 20px;
        }}
        .social-footer {{
            text-align: center;
            margin-top: 40px;
        }}
        .social-footer a img {{
            height: 40px;
            margin: 0px 10px;
        }}
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2 {{
            color: white !important;
            font-weight: bold;
        }}
        section[data-testid="stSidebar"] > div:first-child {{
            background-color: #f27821 !important;
            padding: 12px 20px;
            border-radius: 5px;
        }}
        </style>
    """, unsafe_allow_html=True)
# Ocultar sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)
# Logo GAD centrado
st.markdown(f"""
    <div class='logo-centered'>
        <img src='data:image/png;base64,{load_image_as_base64(logo_gad)}' height='300'>
    </div>
""", unsafe_allow_html=True)

# Botones principales en la fila superior
st.markdown("""
    <div class='menu-container'>
        <form action='/' method='get'>
            <button class='menu-button' name='page' value='mapeo'>📍<br>Mapeo de Ricaurte</button>
        </form>
        <form action='/' method='get'>
            <button class='menu-button' name='page' value='plan'>🧭<br>Plan de Desarrollo</button>
        </form>
        <form action='/' method='get'>
            <button class='menu-button' name='page' value='tematicas'>📚<br>Temáticas</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# # Fila inferior con botones centrados
st.markdown("""
     <div class='menu-container' style='justify-content: center; margin-top: 10px;'>
        <form action='/' method='get'>
            <button class='menu-button' name='page' value='predicciones'>📈<br>Predicciones</button>
        </form>
        <form action='/' method='get'>
            <button class='menu-button' name='page' value='proyecciones'>📊<br>Proyecciones</button>
        </form>
    </div>
 """, unsafe_allow_html=True)


# Navegación
if "page" not in st.session_state:
    st.session_state.page = "home"

params = st.query_params
if "page" in params:
    st.session_state.page = params["page"]

if st.session_state.page == "mapeo":
    st.switch_page("pages/Mapeo.py")
elif st.session_state.page == "plan":
    st.switch_page("pages/Plan.py")
elif st.session_state.page == "tematicas":
    st.switch_page("pages/tematicas.py")
elif st.session_state.page == "predicciones":
    st.switch_page("pages/predicciones.py")
elif st.session_state.page == "proyecciones":
    st.switch_page("pages/proyecciones.py")

# Footer con redes sociales
st.markdown(f"""
    <div class='social-footer'>
        <a href='https://www.facebook.com/RicaurteGAD/?locale=es_LA' target='_blank'>
            <img src='data:image/png;base64,{load_image_as_base64(logo_fb)}'>
        </a>
        <a href='https://www.instagram.com/gadricaurtecuenca/' target='_blank'>
            <img src='data:image/png;base64,{load_image_as_base64(logo_ig)}'>
        </a>
        <a href='https://x.com/ricaurtegad' target='_blank'>
            <img src='data:image/png;base64,{load_image_as_base64(logo_tw)}'>
        </a>
        <a href='https://www.tecazuay.edu.ec/' target='_blank'>
            <img src='data:image/png;base64,{load_image_as_base64(logo_tec)}' height='40'>
        </a>
    </div>
""", unsafe_allow_html=True)
