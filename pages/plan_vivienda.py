import streamlit as st
import pandas as pd
import base64
import os
import plotly.express as px


# Configuración de página
st.set_page_config(page_title="Vivienda - Plan de Desarrollo", layout="wide")
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
        .box {{
            background-color: rgba(255, 255, 255, 0.5);
            border-radius: 15px;
            padding: 10px 15px;
            margin-top: 30px;
            margin-bottom: 30px;
            border: 1px solid #ccc;
        }}
        .box-title {{
            background-color: #003366;
            color: white;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
        }}
        section[data-testid="stSidebar"] > div:first-child {{
            background-color: #f37020;
        }}
        .card {{
            background-color: rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .card h4 {{
            color: #003366;
            font-size: 18px;
            margin-bottom: 10px;
        }}
        .card h2 {{
            color: #003366;
            font-size: 30px;
            margin: 0;
        }}
        </style>
    """, unsafe_allow_html=True)

# Aplica fondo
set_background("pages/imagen principal.jpeg")
# Ocultar sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <form action='/Plan' method='get'>
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
            📊 Volver a Plan
        </button>
    </form>
""", unsafe_allow_html=True)


# Cargar datos
df = pd.read_csv("data_vinculacion/DATOS_VIVIENDA.csv", sep=";", encoding="utf-8")

# -------------------- FILTROS --------------------
st.markdown("<h2 style='text-align:center;'>🏠 Información sobre Vivienda</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    tipos = ["Todas"] + sorted(df["Tipo_vivienda"].dropna().unique().tolist())
    tipo_sel = st.selectbox("TIPO VIVIENDA", tipos, index=0)

with col2:
    energias = ["Todas"] + sorted(df["Disponibilidad_de_energia_electrica_por_red_publica"].dropna().unique().tolist())
    energia_sel = st.selectbox("DISPONIBILIDAD DE ENERGÍA ELÉCTRICA", energias, index=0)

# Aplicar filtros
df_filtrado = df.copy()
if tipo_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Tipo_vivienda"] == tipo_sel]
if energia_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Disponibilidad_de_energia_electrica_por_red_publica"] == energia_sel]

# -------------------- TARJETAS --------------------
tarjetas = st.columns(3)

with tarjetas[0]:
    st.markdown(f"""
        <div style='background-color: rgba(255, 255, 255, 0.5); padding: 25px; border-radius: 15px; 
                    text-align: center; height: 150px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='color: #003366; font-weight: bold; font-size: 16px;'>PROMEDIO DE PERSONAS POR VIVIENDA</div>
            <div style='color: #003366; font-size: 32px; margin-top: 10px;'>{round(df_filtrado["Total_personas_de_la_vivienda"].mean(), 2)}</div>
        </div>
    """, unsafe_allow_html=True)

with tarjetas[1]:
    st.markdown(f"""
        <div style='background-color: rgba(255, 255, 255, 0.5); padding: 25px; border-radius: 15px; 
                    text-align: center; height: 150px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='color: #003366; font-weight: bold; font-size: 16px;'>VIVIENDAS PARTICULARES</div>
            <div style='color: #003366; font-size: 32px; margin-top: 10px;'>{len(df_filtrado[df_filtrado["Condicion_ocupacion_vivienda_particular"].notna()]):,}</div>
        </div>
    """, unsafe_allow_html=True)

with tarjetas[2]:
    st.markdown(f"""
        <div style='background-color: rgba(255, 255, 255, 0.5); padding: 25px; border-radius: 15px; 
                    text-align: center; height: 150px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='color: #003366; font-weight: bold; font-size: 16px;'>VIVIENDAS COLECTIVAS</div>
            <div style='color: #003366; font-size: 32px; margin-top: 10px;'>{len(df_filtrado[df_filtrado["Condicion_ocupacion_vivienda_colectiva"].notna()]):,}</div>
        </div>
    """, unsafe_allow_html=True)

# -------------------- GRÁFICOS --------------------
def grafico_barras(titulo, columna, key_suffix=""):
    st.markdown(f"<div class='box'><div class='box-title'>{titulo}</div>", unsafe_allow_html=True)
    datos = df_filtrado[columna].value_counts().reset_index()
    datos.columns = ["Categoría", "Cantidad"]
    fig = px.bar(datos, x="Categoría", y="Cantidad", text="Cantidad", color="Categoría",
                 color_discrete_sequence=px.colors.qualitative.Safe)

    fig.update_layout(
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            tickfont=dict(color="#FFFFFF", size=14, family="sans-serif")
        ),
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', size=14, family="sans-serif")
    )

    fig.update_traces(textfont=dict(color='white', size=14, family="sans-serif"))
    st.plotly_chart(fig, use_container_width=True, key=columna + key_suffix)
    st.markdown("</div>", unsafe_allow_html=True)

def grafico_pie(titulo, columna):
    st.markdown(f"<div class='box'><div class='box-title'>{titulo}</div>", unsafe_allow_html=True)
    datos = df_filtrado[columna].value_counts().reset_index()
    datos.columns = ["Categoría", "Cantidad"]
    fig = px.pie(datos, names="Categoría", values="Cantidad", hole=0.5,
                 color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_layout(
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', size=14, family="sans-serif")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Mostrar gráficos
grafico_barras("TENENCIA DE LA PROPIEDAD", "Condicion_ocupacion_vivienda_particular", key_suffix="_propiedad")
grafico_barras("EL AGUA LLEGA A LA VIVIENDA POR:", "El_agua_que_recibe_la_vivienda_es")
grafico_barras("EL AGUA QUE RECIBE LA VIVIENDA PROVIENE DE:", "El_agua_que_recibe_la_vivienda_proviene_o_es_suministrada_por")
grafico_pie("ELIMINACIÓN DE BASURA", "Eliminacion_de_la_basura")
grafico_barras("CONDICIÓN DE OCUPACIÓN DE VIVIENDA", "Condicion_ocupacion_vivienda_particular", key_suffix="_ocupacion")
grafico_barras("OTRAS FUENTES DE ENERGÍA ELÉCTRICA", "Disponibilidad_de_otra_fuente_de_energia_electrica")
