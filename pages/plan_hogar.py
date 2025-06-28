import streamlit as st
import pandas as pd
import base64
import plotly.express as px


# Configurar página
st.set_page_config(page_title="Hogar - Plan de Desarrollo", layout="wide")

# Ocultar sidebar completamente desde el inicio
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

def mostrar():
    if st.button("⬅️ Volver al Plan Principal"):
        st.session_state["pagina_actual"] = "plan"
        st.experimental_rerun()
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
            margin-bottom: 10px;
        }}
        section[data-testid="stSidebar"] > div:first-child {{
            background-color: #f37020;
        }}
        </style>
    """, unsafe_allow_html=True)

# Aplicar fondo
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
df_hogar = pd.read_csv("data_vinculacion/DATOS_HOGAR.csv", sep=";", encoding="utf-8")
df_pob = pd.read_csv("data_vinculacion/DATOS_POBLACION.csv", sep=";", encoding="utf-8")

# Título
st.markdown("<h2 style='text-align:center;'>🏡 Información sobre el Hogar</h2>", unsafe_allow_html=True)

# Fila de filtros y tarjeta
col1, col2, col3 = st.columns([1.5, 1, 1])

with col1:
    st.markdown("""
        <div class='box'>
            <div class='box-title'>¿SEPARA LA BASURA ORGÁNICA E INORGÁNICA?</div>
    """, unsafe_allow_html=True)
    filtro_basura = st.radio("", ["Si", "No"], horizontal=True, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    promedio = round(df_hogar["Total_personas_en_el_hogar"].mean(), 2)
    st.markdown(f"""
        <div style='background-color: rgba(255, 255, 255, 0.5); padding: 25px; border-radius: 15px;
                    text-align: center; height: 150px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='color: #003366; font-weight: bold; font-size: 14px;'>TAMAÑO PROMEDIO DEL HOGAR</div>
            <div style='color: #003366; font-size: 30px; margin-top: 10px;'>{promedio}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    miembros_opciones = ["Todas"] + sorted(df_hogar["Total_personas_en_el_hogar"].dropna().astype(int).astype(str).unique())
    seleccion_miembros = st.selectbox("MIEMBROS EN EL HOGAR", miembros_opciones)

# Filtro
df_filtrado = df_hogar[df_hogar["Acostumbra_separar_la_basura_orgánica_e_inorgánica"] == filtro_basura]
if seleccion_miembros != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Total_personas_en_el_hogar"] == int(seleccion_miembros)]

# Gráfico de barras
def grafico_barras(titulo, columna):
    st.markdown(f"<div class='box'><div class='box-title'>{titulo}</div>", unsafe_allow_html=True)
    datos = df_filtrado[columna].value_counts().reset_index()
    datos.columns = ["Categoría", "Cantidad"]
    fig = px.bar(datos, x="Categoría", y="Cantidad", text="Cantidad", color="Categoría",
                 color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_layout(
        xaxis=dict(showticklabels=False),
        yaxis_title=None,
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14),
    )
    fig.update_traces(textfont=dict(color='white', size=14))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Gráfico pie
def grafico_pie(titulo, data):
    st.markdown(f"<div class='box'><div class='box-title'>{titulo}</div>", unsafe_allow_html=True)
    fig = px.pie(data, names="Estado_conyugal", values="Cantidad", hole=0.5,
                 color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_layout(
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Mostrar gráficos
grafico_barras("ACOSTUMBRA A SEPARAR DESECHOS PARA ANIMALES/PLANTAS", "Acostumbra_separar_desperdicios_para_dar_a_los_animales_plantas")
grafico_barras("AGUA QUE BEBEN LOS MIEMBROS DEL HOGAR", "Agua_que_beben_los_miembros_hogar")
grafico_barras("TIPO DE PAREJA EN EL HOGAR", "TipoPareja")

# Estado conyugal desde datos población
df_estado = df_pob["Estado_conyugal"].value_counts().reset_index()
df_estado.columns = ["Estado_conyugal", "Cantidad"]
grafico_pie("ESTADO CONYUGAL", df_estado)
