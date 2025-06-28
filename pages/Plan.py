import streamlit as st
import pandas as pd
import base64
import os

# Configuración de página
st.set_page_config(page_title="Plan de Desarrollo - Resultados Principales", layout="wide")

# Ocultar sidebar completamente desde el inicio
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Fondo personalizado
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

        h1, h2, h3, h5 {{
            color: white !important;
        }}

        .custom-kpi {{
            background-color: rgba(255, 255, 255, 0.4);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.5);
            backdrop-filter: blur(6px);
            margin-bottom: 30px;
            transition: 0.3s;
        }}

        .custom-kpi:hover {{
            transform: scale(1.02);
            cursor: pointer;
        }}

        .custom-kpi h5, .custom-kpi h1 {{
            color: #0A2540 !important;
        }}

        .custom-table {{
            border-collapse: collapse;
            width: 100%;
            background-color: rgba(255, 255, 255, 0.85);
            color: #0A2540;
            font-family: sans-serif;
        }}

        .custom-table th, .custom-table td {{
            border: 1px solid #ddd;
            padding: 10px;
        }}

        .custom-table th {{
            background-color: #0A2540;
            color: white;
            text-align: left;
        }}

        section[data-testid="stSidebar"] > div:first-child {{
            background-color: #f27821;
            color: white;
            padding: 20px;
            border-radius: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("imagen principal.jpeg")
# Ocultar sidebar
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


# Función para convertir imagen a base64
def img_to_base64(image_name):
    if os.path.exists(image_name):
        with open(image_name, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        return f"data:image/png;base64,{img_base64}"
    return ""

# KPIs con íconos
datos = [
    {"titulo": "TOTAL POBLACIÓN", "valor": 26919, "icono": "personas.png", "ancho": "60"},
    {"titulo": "TOTAL VIVIENDAS", "valor": 9891, "icono": "viviendas.png", "ancho": "60"},
    {"titulo": "TOTAL HOGARES", "valor": 7738, "icono": "hogares.png", "ancho": "60"},
    {"titulo": "TOTAL EMIGRANTES", "valor": 711, "icono": "emigrantes.png", "ancho": "60"},
    {"titulo": "TOTAL FALLECIDOS", "valor": 344, "icono": "fallecidos.png", "ancho": "45"},
]

# Título
st.markdown("<h2 style='text-align:center;'>📊 Resultados Principales del Plan de Desarrollo</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)

# Rutas para las tarjetas principales
rutas = ["plan_poblacion", "plan_vivienda", "plan_hogar"]

# Fila 1 - KPIs clicables
cols = st.columns(3)
for i, dato in enumerate(datos[:3]):
    icon_url = img_to_base64(dato["icono"])
    ruta = rutas[i]
    with cols[i]:
        st.markdown(f"""
            <a href="/{ruta}" target="_self" style="text-decoration: none;">
                <div class="custom-kpi">
                    <img src="{icon_url}" alt="icon" width="{dato['ancho']}">
                    <h5>{dato['titulo']}</h5>
                    <h1 style="font-size: 40px;">{dato['valor']:,}</h1>
                </div>
            </a>
        """, unsafe_allow_html=True)

# Fila 2 - Centradas (emigrantes y fallecidos)
cols2 = st.columns([1, 3, 3, 1])
with cols2[1]:
    icon_url = img_to_base64(datos[3]["icono"])
    st.markdown(f"""
        <div class="custom-kpi">
            <img src="{icon_url}" alt="icon" width="{datos[3]['ancho']}">
            <h5>{datos[3]['titulo']}</h5>
            <h1 style="font-size: 40px;">{datos[3]['valor']:,}</h1>
        </div>
    """, unsafe_allow_html=True)

with cols2[2]:
    icon_url = img_to_base64(datos[4]["icono"])
    st.markdown(f"""
        <div class="custom-kpi">
            <img src="{icon_url}" alt="icon" width="{datos[4]['ancho']}">
            <h5>{datos[4]['titulo']}</h5>
            <h1 style="font-size: 40px;">{datos[4]['valor']:,}</h1>
        </div>
    """, unsafe_allow_html=True)

# -------------------------------------------
# TABLA DE ACTIVIDADES ECONÓMICAS POR SEXO
# -------------------------------------------
df = pd.read_csv("ACTIVIDAD ECONÓMICA.csv", sep=",", encoding="utf-8")

tabla = df.pivot_table(index="DESCRIPCIÓN", columns="Sexo_al_nacer", values="Total Poblacion", aggfunc="sum", fill_value=0)
tabla.columns.name = None
tabla = tabla.reset_index()

tabla["Hombre"] = tabla.get("Hombre", 0)
tabla["Mujer"] = tabla.get("Mujer", 0)
tabla["Total"] = tabla["Hombre"] + tabla["Mujer"]
tabla = tabla.sort_values(by="Total", ascending=False)

st.markdown("<h3 style='color: white;'>📋 Tabla de Actividades Económicas por Sexo</h3>", unsafe_allow_html=True)
html_table = tabla[["DESCRIPCIÓN", "Hombre", "Mujer", "Total"]].to_html(index=False, classes='custom-table')
st.markdown(html_table, unsafe_allow_html=True)
