import streamlit as st
import urllib.parse

# 1. Seguridad
if not st.session_state.get('autenticado', False):
    st.warning("🔒 Por favor, inicia sesión en la página principal.")
    st.stop()

st.title("📲 CENTRO DE COMUNICACIÓN WHATSAPP")
st.markdown("Herramienta para enviar recordatorios y formularios de forma directa.")

col_ws1, col_ws2 = st.columns(2)

with col_ws1:
    st.markdown("### 1. Datos del Destinatario")
    telefono = st.text_input("Teléfono (Ej: 34600123456)", value="34")
    nombre_dest = st.text_input("Nombre del Alumno")
    tipo_mensaje = st.selectbox("Plantilla de mensaje:", 
                                ["Solicitud de Datos", "Bienvenida al Grupo", "Recordatorio de Pago"])

with col_ws2:
    st.markdown("### 2. Previsualización")
    if tipo_mensaje == "Solicitud de Datos":
        texto_base = f"Hola {nombre_dest}, ¡bienvenido al club! 🎾\nPara completar tu ficha, envíanos:\n- DNI:\n- Fecha de nacimiento:\n- Correo electrónico:"
    elif tipo_mensaje == "Bienvenida al Grupo":
        texto_base = f"¡Hola {nombre_dest}! Te confirmo que ya estás en la lista del grupo. ¡Nos vemos en la pista!"
    else:
        texto_base = f"Hola {nombre_dest}, te escribimos del club para recordarte que la cuota de este mes está pendiente. Saludos."
    
    msg_area = st.text_area("Mensaje a enviar:", value=texto_base, height=150)
    
    # Generar el enlace de WhatsApp
    link = f"https://wa.me/{telefono}?text={urllib.parse.quote(msg_area)}"
    
    st.write("")
    st.link_button("🚀 ENVIAR POR WHATSAPP", link)
    st.caption("Se abrirá WhatsApp Web o la App en una nueva pestaña.")