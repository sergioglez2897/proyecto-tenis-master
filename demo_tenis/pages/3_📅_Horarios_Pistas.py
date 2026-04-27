import streamlit as st
import pandas as pd

if not st.session_state.get('autenticado', False):
    st.warning("🔒 Por favor, inicia sesión en la página principal.")
    st.stop()

st.title("📅 CUADRANTE DE PISTAS")

COLORES_PROFES = {'Isaias': '#DCD0FF', 'Carlos': '#BAE1FF', 'Ignacio': '#BAFFC9', 'Sergio': '#FFFFBA', 'Rober': '#FFDFBA'}

# Inicializar horarios en sesión si no existen
if 'horarios' not in st.session_state:
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    horas = [f"{h}:00" for h in range(16, 22)]
    pistas = ['Liceo 1', 'Liceo 2', 'San Marcos 1', 'San Marcos 2', 'La Vera 1']
    profes_base = ['Isaias', 'Carlos', 'Ignacio', 'Sergio', 'Rober']
    
    horarios = {}
    for i, dia in enumerate(dias):
        p_dia = profes_base[i:] + profes_base[:i]
        data = [[h] + p_dia for h in horas]
        horarios[dia] = pd.DataFrame(data, columns=['Hora'] + pistas)
    st.session_state['horarios'] = horarios

legend_html = ""
for p, c in COLORES_PROFES.items(): 
    legend_html += f"<span style='background-color:{c}; padding: 4px 10px; border-radius: 4px; margin-right: 10px; font-weight: bold;'>{p}</span>"
st.markdown(legend_html, unsafe_allow_html=True)
st.write("")

dia = st.selectbox("Día:", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
modo_edicion = st.checkbox("✏️ Editar Profesores", value=False)
df_h = st.session_state['horarios'][dia]

if modo_edicion:
    st.info("Modo Edición: Cambia los nombres en la tabla.")
    edited_h = st.data_editor(df_h, hide_index=True, use_container_width=True)
    if edited_h is not None and not edited_h.equals(df_h):
        st.session_state['horarios'][dia] = edited_h
        st.toast("Horario actualizado")
else:
    def colorear_tabla(val):
        color = COLORES_PROFES.get(val, "#ffffff")
        return f'background-color: {color}; color: #333'
    st.dataframe(df_h.style.map(colorear_tabla), use_container_width=True, hide_index=True)