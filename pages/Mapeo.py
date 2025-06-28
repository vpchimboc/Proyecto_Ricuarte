import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import base64
import unicodedata

# Configurar página
st.set_page_config(page_title="Mapeo de Ricaurte", layout="wide")

# Estilos
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
.main, .block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 5% !important;
    padding-right: 5% !important;
    max-width: 100% !important;
}
html, body, .stApp {
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    overflow-x: hidden;
}
h1, h2, h3, label, .stSelectbox label { color: white !important; }
.custom-table {
    border-collapse: collapse;
    width: 100%;
    background-color: rgba(173, 216, 230, 0.7);
    color: black;
    font-family: sans-serif;
}
.custom-table th, .custom-table td {
    border: 1px solid #ddd;
    padding: 8px;
}
.custom-table th {
    background-color: #4a90e2;
    color: white;
    text-align: left;
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
        </style>
    """, unsafe_allow_html=True)

set_background("imagen principal.jpeg")

# Botón volver al inicio
st.markdown("""
<div style="margin: 30px 0 0 15px;">
    <form action='/' method='get'>
        <button style='
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
</div>
""", unsafe_allow_html=True)

# Título
st.title("📍 Mapeo de Ricaurte")

# Función de limpieza
def normalizar_texto(texto):
    texto = str(texto).strip().upper()
    return unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("utf-8")

# Correcciones de errores
correcciones = {
    "CORAZAN DE JESASS": "CORAZON DE JESUS",
    "JESASS DEL GRAN PODER": "JESUS DEL GRAN PODER",
    "LA ASUNCIAN": "LA ASUNCION",
    "SAN JOSA DE LA PLAYA": "SAN JOSE DE LA PLAYA",
    "SEAOR DE BURGOS": "SENOR DE BURGOS",
    "SIMAN BOLIVAR": "SIMON BOLIVAR"
}

# Cargar archivos
barrios_lista = pd.read_csv("BArrios.csv")
barrios_poblacion = pd.read_csv("tablas_vinculacion/Datos barriales.csv", sep=";")
unidades = pd.read_csv("unidades_con_coordenadas.csv")
sitios = pd.read_csv("sitios_con_coordenadas.csv")

# Normalizar texto
barrios_lista["Barrio"] = barrios_lista["Barrios"].apply(normalizar_texto)
barrios_poblacion["Barrio"] = barrios_poblacion["BARRIO"].apply(normalizar_texto)
barrios_poblacion["Barrio"] = barrios_poblacion["Barrio"].replace(correcciones)
barrios_poblacion = barrios_poblacion.rename(columns={"POBLACIÃ“N TOTAL CENSO 2022": "Poblacion"})

unidades["Barrios"] = unidades["Barrios"].apply(normalizar_texto)
sitios["BARRIO"] = sitios["BARRIO"].apply(normalizar_texto)

# Asignar coordenadas
center_lat, center_lon = -2.8614725, -78.9644341
np.random.seed(42)
barrios_poblacion["Lat"] = center_lat + np.random.uniform(-0.005, 0.005, len(barrios_poblacion))
barrios_poblacion["Lon"] = center_lon + np.random.uniform(-0.005, 0.005, len(barrios_poblacion))
unidades["Lat"] = center_lat + np.random.uniform(-0.005, 0.005, len(unidades))
unidades["Lon"] = center_lon + np.random.uniform(-0.005, 0.005, len(unidades))
sitios["Lat"] = center_lat + np.random.uniform(-0.005, 0.005, len(sitios))
sitios["Lon"] = center_lon + np.random.uniform(-0.005, 0.005, len(sitios))

# Selector de barrio
barrio_options = sorted(barrios_lista["Barrio"].unique())
barrio_sel = st.selectbox("Selecciona un barrio", ["Todos"] + barrio_options)

# Filtrado con corrección para "Todos"
if barrio_sel == "Todos":
    df_mapa = barrios_poblacion.copy()
    unidad_mapa = unidades.copy()
    sitio_mapa = sitios.copy()
    zoom_level = 13
    center_lat = -2.8614725
    center_lon = -78.9644341
else:
    barrio_norm = normalizar_texto(barrio_sel)
    df_mapa = barrios_poblacion[barrios_poblacion["Barrio"] == barrio_norm]
    unidad_mapa = unidades[unidades["Barrios"] == barrio_norm]
    sitio_mapa = sitios[sitios["BARRIO"] == barrio_norm]
    zoom_level = 14
    center_lat = df_mapa["Lat"].mean()
    center_lon = df_mapa["Lon"].mean()

# KPI de población
total_poblacion = f"{df_mapa['Poblacion'].sum():,}"
st.markdown(f"""
<div style="
    background-color: rgba(255, 255, 255, 0.3);
    border: 2px solid rgba(0, 0, 0, 0.2);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    backdrop-filter: blur(4px);
    width: 200px;
">
    <div style="font-size: 36px; font-weight: bold; color: #0A2540;">{total_poblacion}</div>
    <div style="font-size: 16px; color: #0A2540;">POBLACIÓN</div>
</div>
""", unsafe_allow_html=True)

# Mapa interactivo
st.markdown('<h3 style="color: white;">🗺️ Mapa interactivo</h3>', unsafe_allow_html=True)
fig = px.scatter_mapbox(
    df_mapa,
    lat="Lat",
    lon="Lon",
    color="Barrio",
    size="Poblacion",
    hover_name="Barrio",
    zoom=zoom_level,
    center={"lat": center_lat, "lon": center_lon},
    height=600
)

fig.add_scattermapbox(
    lat=unidad_mapa["Lat"],
    lon=unidad_mapa["Lon"],
    mode="markers",
    marker=dict(size=10, color="purple"),
    text=unidad_mapa["Unidades"],
    name="Unidades Educativas"
)

fig.add_scattermapbox(
    lat=sitio_mapa["Lat"],
    lon=sitio_mapa["Lon"],
    mode="markers",
    marker=dict(size=10, color="green"),
    text=sitio_mapa["NOMBRE"],
    name="Sitios Recreacionales"
)

fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig, use_container_width=True)

# Función para mostrar tablas
def mostrar_tabla(df, columnas):
    html_table = df[columnas].to_html(index=False, classes='custom-table')
    st.markdown(html_table, unsafe_allow_html=True)

# Mostrar tablas por filtros
if barrio_sel != "Todos":
    st.markdown('<h3 style="color: white;">🏫 Todas las Unidades Educativas</h3>', unsafe_allow_html=True)
    filtro_u = unidad_mapa.copy()
    tipos_unidad = sorted(filtro_u["Unidad Educativa"].unique())
    tipo_u_sel = st.selectbox("Tipo de Unidad Educativa", ["Todos"] + tipos_unidad)
    if tipo_u_sel != "Todos":
        filtro_u = filtro_u[filtro_u["Unidad Educativa"] == tipo_u_sel]
    mostrar_tabla(filtro_u, ["Unidades", "Unidad Educativa"])

    st.markdown('<h3 style="color: white;">🌳 Todos los Sitios Recreacionales</h3>', unsafe_allow_html=True)
    filtro_s = sitio_mapa.copy()
    tipos_sitio = sorted(filtro_s["TIPO"].unique())
    tipo_s_sel = st.selectbox("Tipo de Sitio Recreacional", ["Todos"] + tipos_sitio)
    if tipo_s_sel != "Todos":
        filtro_s = filtro_s[filtro_s["TIPO"] == tipo_s_sel]
    mostrar_tabla(filtro_s, ["NOMBRE", "TIPO"])
else:
    st.markdown('<h3 style="color: white;">🏫 Todas las Unidades Educativas</h3>', unsafe_allow_html=True)
    mostrar_tabla(unidades, ["Unidades", "Unidad Educativa", "Barrios"])
    st.markdown('<h3 style="color: white;">🌳 Todos los Sitios Recreacionales</h3>', unsafe_allow_html=True)
    mostrar_tabla(sitios, ["NOMBRE", "TIPO", "BARRIO"])
