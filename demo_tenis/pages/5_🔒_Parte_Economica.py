import streamlit as st
import pandas as pd

# 1. Seguridad
if not st.session_state.get('autenticado', False):
    st.warning("🔒 Por favor, inicia sesión en la página principal.")
    st.stop()

st.title("💰 CONTROL ECONÓMICO Y PAGOS")
st.success("✅ Acceso Autorizado - Perfil Administrador")

# Carga de datos
@st.cache_data
def cargar_datos_eco():
    df = pd.read_csv("demo_tenis/data/datos_escuela.csv")
    df['Grupo_Completo'] = df['Grupo'] + " (" + df['Sede'] + ")"
    return df

df = cargar_datos_eco()

st.markdown("🔍 **Filtrar Listado de Pagos:**")
ce_sede, ce_grupo, ce_busq = st.columns(3)

with ce_sede:
    all_sedes_eco = st.checkbox("Todas las Sedes", value=True)
    sedes_un = df['Sede'].unique()
    s_eco_sel = sedes_un if all_sedes_eco else st.multiselect("Sede:", sedes_un, default=sedes_un[:1])

with ce_grupo:
    g_disp_eco = sorted(df[df['Sede'].isin(s_eco_sel)]['Grupo'].unique())
    g_eco_sel = st.multiselect("Filtrar por Grupos:", g_disp_eco)

with ce_busq:
    busq_eco = st.text_input("Buscar por nombre:")

# Filtrado para la tabla de pagos
df_pagos_show = df[(df['Sede'].isin(s_eco_sel)) & (df['Estado']=='Activo')]
if g_eco_sel:
    df_pagos_show = df_pagos_show[df_pagos_show['Grupo'].isin(g_eco_sel)]
if busq_eco:
    df_pagos_show = df_pagos_show[df_pagos_show['ID'].str.contains(busq_eco, case=False)]

# Crear columnas de meses para el control
meses = ['Sep', 'Oct', 'Nov', 'Dic', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
df_pagos_final = df_pagos_show[['ID', 'Grupo_Completo', 'Cuota']].copy()
for m in meses:
    df_pagos_final[m] = False

st.info(f"Mostrando {len(df_pagos_final)} alumnos activos para control de cobros.")

st.data_editor(
    df_pagos_final,
    column_config={m: st.column_config.CheckboxColumn(m, width="small") for m in meses},
    disabled=['ID', 'Grupo_Completo', 'Cuota'],
    hide_index=True,
    use_container_width=True
)
