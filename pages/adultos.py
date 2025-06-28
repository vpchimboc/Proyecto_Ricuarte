import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

# Configuración de página
st.set_page_config(page_title="Adultos Mayores - Plan de Desarrollo", layout="wide")

# Ocultar sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Colores institucionales del GAD
colores_gad = ['#0F5B97', '#A3007D', '#02A9A8', '#F37020', '#6E2594', '#8CC63F', '#F15A24', '#F7E017']

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
        .kpi-box {{
            background-color: rgba(255, 255, 255, 0.5);
            border-radius: 15px;
            padding: 15px;
            margin: auto;
            text-align: center;
            border: 1px solid #ccc;
        }}
        .kpi-title {{
            background-color: #0F5B97;
            color: white;
            padding: 10px;
            border-radius: 10px 10px 0 0;
            font-weight: bold;
        }}
        .kpi-value {{
            font-size: 40px;
            font-weight: bold;
            color: #0F5B97;
        }}
        .box {{
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
        }}
        .box-title {{
            background-color: #0F5B97;
            color: white;
            padding: 8px;
            border-radius: 10px 10px 0 0;
            text-align: center;
            font-weight: bold;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("imagen principal.jpeg")

# Botón de regreso
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

# Cargar datos
poblacion = pd.read_csv("data_vinculacion/DATOS_POBLACION.csv", sep=';', encoding='utf-8')
vivienda = pd.read_csv("data_vinculacion/DATOS_VIVIENDA.csv", sep=';', encoding='utf-8')

# Filtrar adultos mayores (65 a 107 años)
poblacion_filtrada = poblacion[
    (poblacion["Años_cumplidos"].apply(lambda x: str(x).isnumeric())) &
    (poblacion["Años_cumplidos"].astype(int) >= 65) &
    (poblacion["Años_cumplidos"].astype(int) <= 107)
]

# Tarjeta central
st.markdown("""
    <div class='kpi-box' style='width: 300px;'>
        <div class='kpi-title'>TOTAL ADULTOS MAYORES</div>
        <div class='kpi-value'>{:,}</div>
    </div>
""".format(len(poblacion_filtrada)), unsafe_allow_html=True)

# Filtros
f1, f2 = st.columns(2)
with f1:
    sexo = ["Todas"] + sorted(poblacion_filtrada["Sexo_al_nacer"].dropna().unique().tolist())
    sexo_sel = st.selectbox("SEXO", sexo, index=0)

with f2:
    edades = poblacion_filtrada["Años_cumplidos"].dropna().astype(int).unique().tolist()
    edades.sort()
    edad_sel = st.multiselect("EDAD", edades, default=edades)

# Aplicar filtros
filtrado = poblacion_filtrada.copy()
if sexo_sel != "Todas":
    filtrado = filtrado[filtrado["Sexo_al_nacer"] == sexo_sel]
if edad_sel:
    filtrado = filtrado[filtrado["Años_cumplidos"].astype(int).isin(edad_sel)]

# Gráfico 1: Aporta actualmente
g1 = filtrado["Aporta_actualmente"].value_counts().reset_index()
g1.columns = ["Tipo", "Cantidad"]
fig1 = px.pie(g1, names="Tipo", values="Cantidad", hole=0.4, color_discrete_sequence=colores_gad)
fig1.update_layout(paper_bgcolor='rgba(255,255,255,0.1)', plot_bgcolor='rgba(255,255,255,0.1)')

# Gráfico 2: Ocupación
g2 = filtrado["Categoria_ocupacion"].value_counts().reset_index()
g2.columns = ["Categoría", "Cantidad"]
fig2 = px.bar(g2, x="Categoría", y="Cantidad", text="Cantidad", color="Categoría", color_discrete_sequence=colores_gad)
fig2.update_layout(
    showlegend=True,
    legend_orientation="h",
    legend_y=-0.3,
    legend_x=0.5,
    legend_xanchor="center",
    legend_yanchor="top",
    xaxis_title=None,
    xaxis_ticktext=[],
    xaxis_tickvals=[],
    paper_bgcolor='rgba(255,255,255,0.1)',
    plot_bgcolor='rgba(255,255,255,0.1)'
)

# Gráfico 3: Tipo de vivienda
g3 = vivienda["Tipo_vivienda"].value_counts().reset_index()
g3.columns = ["Tipo", "Cantidad"]
fig3 = px.bar(g3, x="Tipo", y="Cantidad", text="Cantidad", color="Tipo", color_discrete_sequence=colores_gad)
fig3.update_layout(
    showlegend=True,
    legend_orientation="h",
    legend_y=-0.3,
    legend_x=0.5,
    legend_xanchor="center",
    legend_yanchor="top",
    xaxis_title=None,
    yaxis_title="Cantidad",
    xaxis_ticktext=[],
    xaxis_tickvals=[],
    paper_bgcolor='rgba(255,255,255,0.1)',
    plot_bgcolor='rgba(255,255,255,0.1)'
)

# Gráfico 4: Grupos quinquenales
g4 = filtrado["Grupos_de_edad_quinquenales"].value_counts().reset_index()
g4.columns = ["Grupo", "Cantidad"]
fig4 = px.bar(g4, x="Grupo", y="Cantidad", text="Cantidad", color="Grupo", color_discrete_sequence=colores_gad)
fig4.update_layout(
    showlegend=True,
    legend_orientation="h",
    legend_y=-0.3,
    legend_x=0.5,
    legend_xanchor="center",
    legend_yanchor="top",
    xaxis_title=None,
    yaxis_title="Cantidad",
    xaxis_ticktext=[],
    xaxis_tickvals=[],
    paper_bgcolor='rgba(255,255,255,0.1)',
    plot_bgcolor='rgba(255,255,255,0.1)'
)

# Mostrar gráficos
c1, c2 = st.columns([1.3, 1])
with c1:
    st.markdown("<div class='box'><div class='box-title'>APORTA ACTUALMENTE</div>", unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='box'><div class='box-title'>OCUPACIÓN</div>", unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

c3, c4 = st.columns([1.3, 1])
with c3:
    st.markdown("<div class='box'><div class='box-title'>TOTAL DE ADULTOS MAYORES SEGÚN GRUPOS QUINQUENALES</div>", unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c4:
    st.markdown("<div class='box'><div class='box-title'>TIPO DE VIVIENDA</div>", unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
