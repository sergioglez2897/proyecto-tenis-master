import streamlit as st
import pandas as pd
import altair as alt
import requests

# 1. SEGURIDAD
if not st.session_state.get('autenticado', False):
    st.warning("🔒 Por favor, inicia sesión en la página principal.")
    st.stop()

# 2. FUENTES DE DATOS
@st.cache_data
def cargar_datos():
    df = pd.read_csv("data/datos_escuela.csv")
    df['Fecha Alta'] = pd.to_datetime(df['Fecha Alta'])
    df['Fecha Baja'] = pd.to_datetime(df['Fecha Baja'])
    df['Grupo_Completo'] = df['Grupo'] + " (" + df['Sede'] + ")"
    return df

@st.cache_data
def obtener_clima():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=28.41&longitude=-16.54&current_weather=true"
        respuesta = requests.get(url).json()
        temp = respuesta['current_weather']['temperature']
        vel_viento = respuesta['current_weather']['windspeed']
        return f"{temp}°C (Viento: {vel_viento} km/h)"
    except:
        return "No disponible"

try:
    df = cargar_datos()
except FileNotFoundError:
    st.error("⚠️ No se encuentra el archivo 'datos_escuela.csv' en la carpeta 'data'.")
    st.stop()

# 3. INTERFAZ Y VISUALIZACIÓN
st.title("📊 DASHBOARD GENERAL")

st.info(f"🌤️ **Meteorología actual en el club (API Externa):** {obtener_clima()}")

st.markdown("⚙️ **Configuración de Vista:**")
f1, f2, f3 = st.columns(3)

with f1:
    todas_sedes = st.checkbox("Todas las sedes", value=True)
    lista_sedes = df['Sede'].unique()
    sedes_sel = lista_sedes if todas_sedes else st.multiselect("Elige sedes:", lista_sedes, default=lista_sedes[:1])

with f2:
    temporada = st.selectbox("Curso:", ["2024-2025", "2023-2024"])

with f3:
    todos_meses = st.checkbox("Curso Completo", value=True)
    lista_meses = ['Septiembre', 'Octubre', 'Noviembre', 'Diciembre', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio']
    meses_sel = lista_meses if todos_meses else st.multiselect("Elige meses:", lista_meses, default=['Septiembre', 'Octubre'])

st.write("---")

df_filtrado = df[df['Sede'].isin(sedes_sel)]
activos = df_filtrado[df_filtrado['Estado']=='Activo']

# AQUI EMPIEZAN TODOS LOS GRAFICOS BIEN ALINEADOS
if not activos.empty:
    # FILA 1
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Distribución Sede")
        st.altair_chart(alt.Chart(activos).mark_bar().encode(x='Sede', y='count()', color='Sede'), use_container_width=True)
    with c2:
        st.subheader("Niveles")
        st.altair_chart(alt.Chart(activos).mark_arc().encode(theta='count()', color='Categoría'), use_container_width=True)
    with c3:
        st.subheader("Evolución Altas")
        evol = activos.set_index('Fecha Alta').resample('ME')['ID'].count().reset_index()
        st.altair_chart(alt.Chart(evol).mark_line(point=True).encode(x='Fecha Alta', y='ID'), use_container_width=True)

    # FILA 2
    st.markdown("---")
    c4, c5, c6 = st.columns(3)
    with c4:
        st.subheader("Top 5 Grupos")
        top = activos['Grupo_Completo'].value_counts().head(5).reset_index()
        st.altair_chart(alt.Chart(top).mark_bar().encode(x='count', y=alt.Y('Grupo_Completo', sort='-x')), use_container_width=True)
    with c5:
        st.subheader("Menores vs Adultos")
        df_t = activos.copy()
        df_t['Tipo'] = df_t['Categoría'].apply(lambda x: 'Adultos' if x=='Adultos' else 'Menores')
        st.altair_chart(alt.Chart(df_t).mark_arc(innerRadius=40).encode(theta='count()', color='Tipo'), use_container_width=True)
    with c6:
        st.subheader("Ingresos Estimados")
        st.altair_chart(alt.Chart(activos).mark_bar().encode(x='Sede', y='sum(Cuota)', color='Sede'), use_container_width=True)

    # FILA 3
    st.markdown("---")
    c7, c8, c9 = st.columns(3)
    with c7:
        st.subheader("Ingresos por Categoría")
        st.altair_chart(alt.Chart(activos).mark_arc(innerRadius=60).encode(theta='sum(Cuota)', color=alt.Color('Categoría', scale=alt.Scale(scheme='pastel1'))), use_container_width=True)
    with c8:
        st.subheader("Retención")
        st.altair_chart(alt.Chart(df_filtrado).mark_bar().encode(x='Sede', y='count()', color=alt.Color('Estado', scale=alt.Scale(domain=['Activo', 'Baja'], range=['#4CAF50', '#FF5252']))), use_container_width=True)
    with c9:
        st.subheader("Tendencia Altas")
        evol_area = activos.set_index('Fecha Alta').resample('ME')['ID'].count().reset_index()
        st.altair_chart(alt.Chart(evol_area).mark_area(opacity=0.3, color='#6C63FF').encode(x='Fecha Alta', y='ID'), use_container_width=True)

else:
    st.warning("⚠️ No hay datos activos para estos filtros.")

# 4. BOTONES DE EXPORTACIÓN
st.markdown("---")
st.subheader("🖨️ Exportación de Informes")
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    btn_imprimir = """
    <button onclick="window.print()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
        🖨️ Imprimir Página
    </button>
    """
    st.markdown(btn_imprimir, unsafe_allow_html=True)

with col_btn2:
    reporte_txt = f"REPORTE DEL CLUB DE TENIS\nCurso: {temporada}\nTotal Activos: {len(activos)}\n"
    st.download_button(
        label="📄 Exportar Resumen a PDF/TXT",
        data=reporte_txt,
        file_name="Reporte_Vision_General.txt",
        mime="text/plain"
    )
    