import streamlit as st
import pandas as pd
import base64
import plotly.express as px
import os

st.set_page_config(page_title="Predicciones", layout="wide")

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
    import base64
    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), /* Mantener el degradado para contraste */
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
        /* Estilos para hacer el texto más visible */
        h1, h2, h3, h4, h5, h6 {{
            color: white !important; /* Texto blanco para títulos */
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important; /* Sombra para mejor contraste */
        }}
        .stMarkdown p, .stDataFrame, .stDataFrame th, .stDataFrame td {{
            color: white !important; /* Color blanco para texto de párrafos y tablas */
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6) !important;
        }}
        .stMarkdown {{
            color: white !important; /* Asegura que el texto general de markdown sea blanco */
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6) !important;
        }}
        /* Asegurarse que el texto de los KPIs tenga el color correcto */
        .box > div:last-child {{ /* Selecciona el último div dentro de .box (donde están los números de los KPIs) */
            color: #FFFF66 !important; /* Usa el color amarillo vibrante */
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important; /* Agrega sombra para contraste */
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("imagen principal.jpeg")

# ... (El resto de tu código Streamlit permanece igual)

# Botón volver al inicio
st.markdown("""
    <form action='/' method='get'>
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
            🔙 Volver al Inicio
        </button>
    </form>
""", unsafe_allow_html=True)

# Cargar datos reales
data_path = os.path.join(os.path.dirname(__file__), '..', 'data_vinculacion', 'DATOS_POBLACION.csv')
poblacion_df = pd.read_csv(data_path, sep=None, engine='python', on_bad_lines='skip')
poblacion_ricaurte = poblacion_df[poblacion_df['PARROQ'].str.strip().str.lower() == 'ricaurte']

# Parámetro interactivo
tasa = st.slider("Tasa de crecimiento anual (%)", 1.0, 3.0, 2.1, step=0.1)

# Recalcular proyección
anios = list(range(2025, 2036))
poblacion_actual = poblacion_ricaurte.shape[0]
poblacion = [round(poblacion_actual * ((1 + tasa/100) ** i)) for i in range(len(anios))]
df = pd.DataFrame({"Año": anios, "Población proyectada": poblacion})
df["Crecimiento absoluto"] = df["Población proyectada"].diff().fillna(0).astype(int)

# KPIs
st.markdown(f"""
    <div style='display:flex; justify-content:center; gap:40px; margin-top: 20px; margin-bottom: 10px;'>
        <div class='box' style='width: 280px; text-align:center;'>
            <div class='box-title'>👥 POBLACIÓN ACTUAL</div>
            <div style='font-size: 36px; font-weight: bold; color: #FFFF66; margin-top: 10px;'>{poblacion[0]:,}</div>
        </div>
        <div class='box' style='width: 280px; text-align:center;'>
            <div class='box-title'>📈 PROYECCIÓN 2035</div>
            <div style='font-size: 36px; font-weight: bold; color: #FFFF66; margin-top: 10px;'>{poblacion[-1]:,}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Gráfico interactivo
fig = px.line(df, x="Año", y="Población proyectada", markers=True,
              title="Proyección de crecimiento poblacional")
fig.update_layout(title_x=0.5, plot_bgcolor='rgba(255,255,255,0)', paper_bgcolor='rgba(255,255,255,0)',
                  font=dict(color="white")) # Color de la fuente del gráfico
st.plotly_chart(fig, use_container_width=True)

# Tabla
st.markdown("#### Tabla de datos proyectados")
st.dataframe(df, use_container_width=True)

# Acceso por grupo etario
st.markdown("## 🧒👴 Predicción por grupos etarios")
etarios = poblacion_ricaurte['Grupos_de_edad_por_etapas_de_vida'].value_counts(normalize=True)
df_etario = pd.DataFrame({ 'Grupo': etarios.index, 'Porcentaje actual': etarios.values })
df_etario['Proyectado 2035'] = (df_etario['Porcentaje actual'] * poblacion[-1]).astype(int)
st.dataframe(df_etario)
fig = px.bar(df_etario, x='Grupo', y='Proyectado 2035', title="Proyección población por grupo etario 2035")
fig.update_layout(title_x=0.5, plot_bgcolor='rgba(255,255,255,0)', paper_bgcolor='rgba(255,255,255,0)',
                  font=dict(color="white")) # Color de la fuente del gráfico
st.plotly_chart(fig, use_container_width=True)

# Alfabetismo
st.markdown("## 🧠 Predicción de alfabetismo") # Este es el texto que quieres visible
alfabetismo = poblacion_ricaurte['Condicion_analfabetismo'].value_counts(normalize=True)
df_alf = pd.DataFrame({ 'Condición': alfabetismo.index, 'Proporción actual': alfabetismo.values })
df_alf['Proyectado 2035'] = (df_alf['Proporción actual'] * poblacion[-1]).astype(int)
fig = px.pie(df_alf, names='Condición', values='Proyectado 2035', title="Distribución de alfabetismo proyectada")
fig.update_layout(title_x=0.5, plot_bgcolor='rgba(255,255,255,0)', paper_bgcolor='rgba(255,255,255,0)',
                  font=dict(color="white")) # Color de la fuente del gráfico
st.plotly_chart(fig, use_container_width=True)

# Tecnología
st.markdown("## 🌐 Proyección de acceso digital")
tecnologia = ['En_los_ultimos_tres_meses_ha_utilizado_internet', 'En_los_ultimos_tres_meses_ha_utilizado_telefono_celular']
data_tec = []
for col in tecnologia:
    acceso = poblacion_ricaurte[col].value_counts(normalize=True)
    for k, v in acceso.items():
        data_tec.append({'Tecnología': col.split('_')[-1], 'Condición': k.strip(), 'Porcentaje': v})
df_tec = pd.DataFrame(data_tec)
fig = px.bar(df_tec, x='Tecnología', y='Porcentaje', color='Condición', barmode='group', title="Acceso a tecnologías digitales")
fig.update_layout(title_x=0.5, plot_bgcolor='rgba(255,255,255,0)', paper_bgcolor='rgba(255,255,255,0)',
                  font=dict(color="white")) # Color de la fuente del gráfico
st.plotly_chart(fig, use_container_width=True)