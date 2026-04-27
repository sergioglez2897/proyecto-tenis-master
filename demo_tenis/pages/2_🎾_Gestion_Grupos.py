import streamlit as st
import pandas as pd

if not st.session_state.get('autenticado', False):
    st.warning("🔒 Por favor, inicia sesión en la página principal.")
    st.stop()

st.title("🎾 GESTIÓN DE GRUPOS")

@st.cache_data
def cargar_datos():
    df = pd.read_csv("demo_tenis/data/datos_escuela.csv")
    df['Grupo_Completo'] = df['Grupo'] + " (" + df['Sede'] + ")"
    return df

df = cargar_datos()

col_s, col_g, col_b = st.columns([1, 1, 1])
with col_s:
    all_s = st.checkbox("Todas las Sedes", value=True, key="gs_all")
    sedes_un = df['Sede'].unique()
    s_sel = sedes_un if all_s else st.multiselect("Sedes:", sedes_un, default=sedes_un[:1])
with col_g:
    g_disp = sorted(df[df['Sede'].isin(s_sel)]['Grupo'].unique())
    g_sel = st.multiselect("Grupos:", g_disp)
with col_b:
    busq = st.text_input("🔍 Buscar Alumno:")

modo_edicion = st.checkbox("✏️ Activar Edición")
df_show = df[df['Sede'].isin(s_sel) & (df['Estado'] == 'Activo')]
if g_sel: df_show = df_show[df_show['Grupo'].isin(g_sel)]
if busq: df_show = df_show[df_show['ID'].str.contains(busq, case=False)]

st.info(f"Viendo {len(df_show)} alumnos")

if modo_edicion:
    st.warning("Modo Edición Activado")
    edited = st.data_editor(df_show, disabled=['ID', 'Sede', 'Grupo_Completo'], hide_index=True, use_container_width=True)
    if edited is not None and not edited.equals(df_show):
        st.toast("✅ Cambios registrados temporalmente en la sesión")
else:
    st.dataframe(df_show[['ID', 'Grupo', 'Categoría', 'Licencia', 'Cuota']], hide_index=True, use_container_width=True)
