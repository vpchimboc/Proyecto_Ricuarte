
import streamlit as st
import pandas as pd
import base64
import plotly.express as px
import os

st.set_page_config(page_title="Proyecciones", layout="wide")

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




set_background("imagen principal.jpg")

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
data_path = os.path.join(os.path.dirname(__file__), '..', 'data_vinculacion', 'DATOS_VIVIENDA.csv')
vivienda_df = pd.read_csv(data_path, sep=None, engine='python', on_bad_lines='skip')
vivienda_ricaurte = vivienda_df[vivienda_df['PARROQ'].str.strip().str.lower() == 'ricaurte']

# Calcular población y viviendas actuales
poblacion_actual = 26919
viviendas_actuales = vivienda_ricaurte[
    vivienda_ricaurte['Condicion_ocupacion_de_la_vivienda_particular(recodificada)'].str.contains("Ocupada", na=False)
].shape[0]

# Parámetros
personas_por_hogar = st.slider("Promedio de personas por vivienda", 3, 6, 4)

# Proyecciones
anios = list(range(2025, 2036))
poblacion = [round(poblacion_actual * ((1 + 0.021) ** i)) for i in range(len(anios))]
viviendas = [round(p / personas_por_hogar) for p in poblacion]
df = pd.DataFrame({'Año': anios, 'Población proyectada': poblacion, 'Viviendas proyectadas': viviendas})
df['Déficit'] = df['Viviendas proyectadas'] - viviendas_actuales

# KPIs
st.markdown(f"""
    <div style='display:flex; justify-content:center; gap:40px; margin-top: 20px; margin-bottom: 10px;'>
        <div class='box' style='width: 280px; text-align:center;'>
            <div class='box-title'>🏘️ VIVIENDAS ACTUALES</div>
            <div style='font-size: 36px; font-weight: bold; color: #0A2540; margin-top: 10px;'>{viviendas[0]:,}</div>
        </div>
        <div class='box' style='width: 280px; text-align:center;'>
            <div class='box-title'>📈 PROYECCIÓN 2035</div>
            <div style='font-size: 36px; font-weight: bold; color: #0A2540; margin-top: 10px;'>{viviendas[-1]:,}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Gráfico principal
fig = px.bar(df, x="Año", y="Viviendas proyectadas", title="Proyección de viviendas necesarias", text_auto=True)
fig.update_layout(title_x=0.5, plot_bgcolor='rgba(255,255,255,0.0)', paper_bgcolor='rgba(255,255,255,0.0)')
st.plotly_chart(fig, use_container_width=True)

# Tabla
st.dataframe(df, use_container_width=True)

# Tipos de vivienda
st.markdown("## 🏘️ Proyección por tipo de vivienda")
tipo_viv = vivienda_ricaurte['Tipo_vivienda'].value_counts(normalize=True)
df_tipov = pd.DataFrame({ 'Tipo': tipo_viv.index, 'Porcentaje actual': tipo_viv.values })
df_tipov['Proyectado 2035'] = (df_tipov['Porcentaje actual'] * viviendas[-1]).astype(int)
fig = px.bar(df_tipov, x='Tipo', y='Proyectado 2035', title="Tipos de vivienda proyectados a 2035")
fig.update_layout(title_x=0.5, plot_bgcolor='rgba(255,255,255,0.0)', paper_bgcolor='rgba(255,255,255,0.0)')
st.plotly_chart(fig, use_container_width=True)

# Servicios básicos
st.markdown("## 🚰 Proyección de servicios básicos")
servicios = ['El_agua_que_recibe_la_vivienda_es', 'Disponibilidad_de_energia_electrica_por_red_publica']
for col in servicios:
    acceso = vivienda_ricaurte[col].value_counts(normalize=True).head(5)
    df_serv = pd.DataFrame({ 'Condición': acceso.index, 'Porcentaje actual': acceso.values })
    df_serv['Proyectado 2035'] = (df_serv['Porcentaje actual'] * viviendas[-1]).astype(int)
    fig = px.bar(df_serv, x='Condición', y='Proyectado 2035', title=f"Proyección servicio: {col.replace('_',' ')}")
    fig.update_layout(title_x=0.5, plot_bgcolor='rgba(255,255,255,0.0)', paper_bgcolor='rgba(255,255,255,0.0)')
    st.plotly_chart(fig, use_container_width=True)

# Déficit acumulado
st.markdown("## 📉 Déficit acumulado de viviendas")
df['Déficit acumulado'] = df['Déficit'].cumsum()
fig = px.area(df, x='Año', y='Déficit acumulado', title="Déficit acumulado proyectado")
fig.update_layout(title_x=0.5, plot_bgcolor='rgba(255,255,255,0.0)', paper_bgcolor='rgba(255,255,255,0.0)')
st.plotly_chart(fig, use_container_width=True)
