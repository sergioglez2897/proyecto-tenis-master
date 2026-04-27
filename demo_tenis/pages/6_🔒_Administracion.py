import streamlit as st
import pandas as pd

# 1. Seguridad
if not st.session_state.get('autenticado', False):
    st.warning("🔒 Por favor, inicia sesión en la página principal.")
    st.stop()

st.title("⚙️ PANEL DE ADMINISTRACIÓN")
st.success("✅ Acceso Autorizado")

# Inicializar el DataFrame en la sesión si no existe para que los cambios se mantengan al navegar
if 'df_alumnos' not in st.session_state:
    df_base = pd.read_csv("demo_tenis/data/datos_escuela.csv")
    df_base['Fecha Alta'] = pd.to_datetime(df_base['Fecha Alta'])
    st.session_state['df_alumnos'] = df_base

tab1, tab2, tab3 = st.tabs(["➕ ALTA DE JUGADOR", "❌ TRAMITAR BAJA", "⏳ LISTA DE RESERVA"])

with tab1:
    st.markdown("### Registrar Nuevo Alumno")
    with st.form("formulario_alta"):
        c1, c2 = st.columns(2)
        nuevo_nom = c1.text_input("Nombre y Apellidos")
        nueva_sede = c2.selectbox("Sede", ["Liceo de Taoro", "San Marcos", "La Vera"])
        nueva_cat = c1.selectbox("Categoría", ["Pre-Tenis", "Infantil", "Competición", "Adultos"])
        nueva_cuota = c2.number_input("Cuota Mensual (€)", value=45)
        
        if st.form_submit_button("✅ GUARDAR ALTA"):
            nuevo_registro = {
                "ID": nuevo_nom, "Sede": nueva_sede, "Estado": "Activo", 
                "Categoría": nueva_cat, "Cuota": nueva_cuota, "Fecha Alta": pd.Timestamp.now()
            }
            st.session_state['df_alumnos'] = pd.concat([st.session_state['df_alumnos'], pd.DataFrame([nuevo_registro])], ignore_index=True)
            st.success(f"¡{nuevo_nom} ha sido registrado correctamente!")

with tab2:
    st.markdown("### Gestión de Bajas")
    df_activos = st.session_state['df_alumnos'][st.session_state['df_alumnos']['Estado'] == 'Activo']
    baja_id = st.selectbox("Selecciona el alumno que causa baja:", df_activos['ID'].unique())
    
    if st.button("⚠️ CONFIRMAR BAJA DEFINITIVA"):
        idx = st.session_state['df_alumnos'][st.session_state['df_alumnos']['ID'] == baja_id].index
        st.session_state['df_alumnos'].loc[idx, 'Estado'] = 'Baja'
        st.session_state['df_alumnos'].loc[idx, 'Fecha Baja'] = pd.Timestamp.now()
        st.success(f"Se ha procesado la baja de {baja_id}.")

with tab3:
    st.markdown("### Lista de Espera / Reserva")
    st.info("Aquí puedes anotar a personas interesadas que aún no tienen grupo.")
    reserva_nom = st.text_input("Nombre interesado:")
    reserva_tel = st.text_input("Teléfono contacto:")
    if st.button("Añadir a Reserva"):
        st.toast(f"{reserva_nom} añadido a la lista de espera.")
