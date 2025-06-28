import streamlit as st
import pandas as pd
import base64
import plotly.express as px
import os

st.set_page_config(page_title="Niños - Plan de Desarrollo", layout="wide")

# Ocultar sidebar
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
        }}
        .box {{
            background-color: rgba(255, 255, 255, 0.6);
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
        }}
        .box-title {{
            background-color: #003366;
            color: white;
            padding: 6px;
            border-radius: 10px 10px 0 0;
            text-align: center;
            font-weight: bold;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("imagen principal.jpeg")

# Botón volver
st.markdown("""
    <form action='/plan_poblacion' method='get'>
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
            👥  Volver a Población
        </button>
    </form>
""", unsafe_allow_html=True)

# Cargar data
df = pd.read_csv("data_vinculacion/DATOS_POBLACION.csv", sep=";", encoding="utf-8")
df_emig = pd.read_csv("data_vinculacion/DATOS_EMIGRACION.csv", sep=";", encoding="utf-8")

# Colores oficiales GAD
colores_gad = ['#0F5B97', '#A3007D', '#02A9A8', '#F37020', '#6E2594', '#8CC63F', '#F15A24', '#F7E017']
colores_sexo = {'Hombre': '#0F5B97', 'Mujer': '#F370A0'}

# Filtrar niños
df_ninos = df[df["Grupos_de_edad_por_etapas_de_vida"] == "Niñas/os de 0 a 11 años"]

# === TARJETA CENTRADA ===
st.markdown(f"""
    <div style='display:flex; justify-content:center; margin-top: 20px; margin-bottom: 10px;'>
        <div class='box' style='width: 250px; text-align:center;'>
            <div class='box-title'>TOTAL NIÑOS</div>
            <div style='font-size: 36px; font-weight: bold; color: #0A2540; margin-top: 10px;'>{len(df_ninos):,}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Filtros
f1, f2 = st.columns(2)

with f1:
    educacion_opciones = ["Todas"] + sorted(df_ninos["Asiste_actualmente_a_educacion_regular_o_formal"].dropna().unique())
    educ_sel = st.selectbox("ASISTE A EDUCACIÓN REGULAR", educacion_opciones, index=0)

with f2:
    edades_opciones = ["Todas"] + sorted(df_ninos["Años_cumplidos"].dropna().astype(int).unique().tolist())
    edad_sel = st.selectbox("EDADES", edades_opciones, index=0)

# Aplicar filtros
df_filtrado = df_ninos.copy()
if educ_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Asiste_actualmente_a_educacion_regular_o_formal"] == educ_sel]
if edad_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Años_cumplidos"].astype(str) == str(edad_sel)]

# === G1: Educación formal ===
g1_data = df_filtrado["Asiste_actualmente_a_educacion_regular_o_formal"].value_counts().reset_index()
g1_data.columns = ["Respuesta", "Cantidad"]
fig1 = px.bar(g1_data, x="Respuesta", y="Cantidad", text="Cantidad", title="CONDICIÓN ASISTENCIA EDUCATIVA",
              color="Respuesta", color_discrete_sequence=colores_gad)
fig1.update_layout(title_x=0.5, plot_bgcolor='rgba(255,255,255,0.1)', paper_bgcolor='rgba(255,255,255,0.1)')

# === G2: Analfabetismo ===
g2_data = df_filtrado["Condicion_analfabetismo"].value_counts().reset_index()
g2_data.columns = ["Condición", "Cantidad"]
fig2 = px.bar(g2_data, x="Condición", y="Cantidad", text="Cantidad", title="CONDICIÓN ANALFABETISMO",
              color="Condición", color_discrete_sequence=colores_gad)
fig2.update_layout(title_x=0.5, plot_bgcolor='rgba(255,255,255,0.1)', paper_bgcolor='rgba(255,255,255,0.1)')

# === G3: Dificultad funcional ===
g3_data = df_filtrado["Dificultad_funcional_permanente"].value_counts().reset_index()
g3_data.columns = ["Condición", "Cantidad"]
fig3 = px.bar(g3_data, x="Condición", y="Cantidad", text="Cantidad", title="DIFICULTAD FUNCIONAL PERMANENTE",
              color="Condición", color_discrete_sequence=colores_gad)
fig3.update_layout(title_x=0.5, plot_bgcolor='rgba(255,255,255,0.1)', paper_bgcolor='rgba(255,255,255,0.1)')

# === G4: Año emigración ===
df_emi_ninos = df_emig[df_emig["Edad_salida"] <= 11]
g4_data = df_emi_ninos["Año_salida"].value_counts().sort_index().reset_index()
g4_data.columns = ["Año", "Cantidad"]
fig4 = px.bar(g4_data, x="Año", y="Cantidad", text="Cantidad", title="AÑO QUE EMIGRARON",
              color="Año", color_discrete_sequence=colores_gad)
fig4.update_layout(title_x=0.5, plot_bgcolor='rgba(255,255,255,0.1)', paper_bgcolor='rgba(255,255,255,0.1)')

# === G5: Sexo al nacer ===
g5_data = df_filtrado["Sexo_al_nacer"].value_counts().reset_index()
g5_data.columns = ["Sexo", "Cantidad"]
fig5 = px.pie(g5_data, names="Sexo", values="Cantidad", hole=0.4, title="SEXO AL NACER",
              color="Sexo", color_discrete_map=colores_sexo)
fig5.update_layout(title_x=0.5, plot_bgcolor='rgba(255,255,255,0.1)', paper_bgcolor='rgba(255,255,255,0.1)')

# === Mostrar gráficos ===
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig3, use_container_width=True)
with col4:
    st.plotly_chart(fig4, use_container_width=True)

st.plotly_chart(fig5, use_container_width=True)
