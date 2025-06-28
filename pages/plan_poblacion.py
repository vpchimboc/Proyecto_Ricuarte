import streamlit as st
import pandas as pd
import base64
import plotly.express as px
import os

# Configuración de página
st.set_page_config(page_title="Población - Plan de Desarrollo", layout="wide")

# Ocultar sidebar completamente desde el inicio
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
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
            margin: 0;
            padding: 0;
        }}
        .kpi-button {{
            background-color: rgba(255, 255, 255, 0.5);
            border-radius: 15px;
            padding: 10px 15px;
            text-align: center;
            font-weight: bold;
            font-size: 20px;
            border: 1px solid #ccc;
            width: 100%;
            height: 140px;
        }}
        .kpi-img {{
            width: 60px;
            height: 60px;
            display: block;
            margin: auto;
        }}
        .box {{
            background-color: rgba(255, 255, 255, 0.5);
            border-radius: 15px;
            padding: 10px 15px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
        }}
        .box-title {{
            background-color: #007BFF;
            color: white;
            padding: 8px;
            border-radius: 10px 10px 0 0;
            text-align: center;
            font-weight: bold;
        }}
        button {{
            margin: 0 auto;
            display: block;
        }}
        </style>
    """, unsafe_allow_html=True)

# Aplica fondo
set_background("pages/imagen principal.jpeg")

st.markdown("""
    <form action='/Plan' method='get'>
        <button style='
            margin-top: 30px;
            margin-left: 20px;
            padding: 12px 25px;
            background-color: #0A2540;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
        '>
            📊 Volver a Plan
        </button>
    </form>
""", unsafe_allow_html=True)


# Cargar datos
df = pd.read_csv("data_vinculacion/DATOS_POBLACION.csv", sep=";", encoding="utf-8")
colores_gad = ['#0F5B97', '#A3007D', '#02A9A8', '#F37020', '#6E2594', '#8CC63F', '#F15A24', '#F7E017']

# Título centrado
st.markdown("<h2 style='text-align:center; margin-top: 20px;'>🔍 Información Demográfica de la Población</h2>", unsafe_allow_html=True)

# Función para convertir imagen a base64
def img_to_base64(image_name):
    if os.path.exists(image_name):
        with open(image_name, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        return f"data:image/png;base64,{img_base64}"
    return ""

# Tarjetas centradas con íconos que sí se muestran correctamente
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"""
        <form action='/ninos' method='get'>
            <button class='kpi-button' type='submit'>
                <img src='{img_to_base64("ninos.png")}' class='kpi-img'>
                Niños
            </button>
        </form>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <form action='/adultos' method='get'>
            <button class='kpi-button' type='submit'>
                <img src='{img_to_base64("adultos.png")}' class='kpi-img'>
                Adultos
            </button>
        </form>
    """, unsafe_allow_html=True)


# Filtros centrados
f1, f2, f3 = st.columns([1, 1, 1])

with f1:
    edades_validas = df["Años_cumplidos"].dropna()
    edades_validas = edades_validas[edades_validas.astype(str).str.isnumeric()].astype(int)
    edades = ["Todas"] + sorted(edades_validas.unique().tolist())
    edad_sel = st.selectbox("EDADES", edades, index=0)

with f2:
    actividades = ["Todas"] + sorted(df["Rama_actividad(nivel1)"].dropna().unique().tolist())
    act_sel = st.selectbox("ACTIVIDADES DE LA POBLACIÓN", actividades, index=0)

with f3:
    culturas = ["Todas"] + sorted(df["Como_se_identifica_segun_su_cultura_costumbres"].dropna().unique().tolist())
    cultura_sel = st.selectbox("CULTURA Y COSTUMBRES", culturas, index=0)

# Aplicar filtros
df_filtrado = df.copy()
if edad_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Años_cumplidos"].astype(str) == str(edad_sel)]
if act_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Rama_actividad(nivel1)"] == act_sel]
if cultura_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Como_se_identifica_segun_su_cultura_costumbres"] == cultura_sel]

# Categoría de ocupación
st.markdown("<div class='box'><div class='box-title'>CATEGORÍA DE OCUPACIÓN</div>", unsafe_allow_html=True)
ocup = df_filtrado["Categoria_ocupacion"].value_counts().reset_index()
ocup.columns = ["Categoría", "Cantidad"]
fig1 = px.bar(ocup, x="Categoría", y="Cantidad", text="Cantidad", color="Categoría", color_discrete_sequence=colores_gad)
fig1.update_traces(textposition="outside")
fig1.update_layout(xaxis_title=None, yaxis_title=None, height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig1, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Gráficos adicionales
g1, g2 = st.columns([1.2, 1])

with g1:
    st.markdown("<div class='box'><div class='box-title'>DIFICULTAD FUNCIONAL PERMANENTE</div>", unsafe_allow_html=True)
    diff = df_filtrado["Dificultad_funcional_permanente"].value_counts().reset_index()
    diff.columns = ["Condición", "Cantidad"]
    fig2 = px.bar(diff, x="Condición", y="Cantidad", text="Cantidad", color="Condición", color_discrete_sequence=colores_gad)
    fig2.update_traces(textposition="outside")
    fig2.update_layout(xaxis_title=None, yaxis_title=None, height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with g2:
    st.markdown("<div class='box'><div class='box-title'>CULTURA</div>", unsafe_allow_html=True)
    cult = df_filtrado["Como_se_identifica_segun_su_cultura_costumbres"].value_counts().reset_index()
    cult.columns = ["Identidad", "Cantidad"]
    fig3 = px.pie(cult, names="Identidad", values="Cantidad", hole=0.5, color_discrete_sequence=colores_gad)
    fig3.update_traces(textposition="inside", textinfo="percent+label")
    fig3.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
