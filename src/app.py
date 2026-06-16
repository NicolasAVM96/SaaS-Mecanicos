import streamlit as st
from components import history_view, login
from data import database
from controllers import auth_controller
from components import record_form  

st.set_page_config(page_title="Gestion de Taller", layout="centered")

# --- Lógica de Notificaciones ---
if "notificacion" in st.session_state:
    n = st.session_state.notificacion
    if n["tipo"] == "success":
        st.toast(n["texto"], icon="🚗")
    del st.session_state.notificacion


# --- Inicialización y Seguridad Modular ---
database.inicializar_db()
login.render_login_screen() # Protege la app. Si falla, gatilla st.stop() internamente

# --- Sidebar ---
st.sidebar.write(f"Conectado: **{st.session_state.get('email', '')}**")
rol = st.session_state.get("rol", "")
if rol:
    st.sidebar.caption(f"Rol: {rol}")

with st.sidebar.expander("🔑 Cambiar contraseña"):
    nueva = st.text_input("Nueva contraseña", type="password", key="sb_nueva_pass")
    confirmar = st.text_input("Confirmar contraseña", type="password", key="sb_confirmar_pass")
    if st.button("Actualizar contraseña", use_container_width=True):
        ok, msg = auth_controller.cambiar_contrasena(nueva, confirmar)
        if ok:
            st.success(msg)
        else:
            st.error(msg)

st.sidebar.divider()
if st.sidebar.button("Cerrar Sesión"):
    auth_controller.cerrar_sesion()

st.title("🔧 Gestión de Taller")
tab1, tab2 = st.tabs(["🆕 Nuevo Ingreso", "📜 Historial"])

with tab1:
    record_form.render_registro_tab()

with tab2:
    history_view.render_historial_tab()