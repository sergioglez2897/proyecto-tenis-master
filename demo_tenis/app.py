import streamlit as st

st.set_page_config(page_title="WikiTeam", page_icon="🎾", layout="wide")

# --- CONTROL DE SESIÓN GLOBAL ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

def login():
    # Centramos el login un poco
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔑 Acceso al Sistema WikiTeam")
        st.write("Por favor, introduce tus credenciales para continuar.")
        
        with st.form("login_form"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Entrar")
            
            if submit:
                # El profesor exige que sea admin / admin
                if u == "admin" and p == "admin":
                    st.session_state['autenticado'] = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas. Pruebe de nuevo.")

# Si NO está autenticado, mostramos el login y paramos la app
if not st.session_state['autenticado']:
    login()
    st.stop()

# --- HOME PAGE (Solo se ve si el login es correcto) ---
st.title("🏠 Bienvenido al Panel de Gestión TheWikiTeam")
st.write("Has iniciado sesión correctamente. Utiliza el menú lateral para navegar por las distintas áreas del club.")

try:
    st.image("data/image_0.png", width=300)
except Exception as e:
    st.warning("No se pudo cargar el logo. Asegúrate de que image_0.png está en la carpeta data.")