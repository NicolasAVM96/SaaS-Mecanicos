import streamlit as st
from controllers import auth_controller

def render_login_screen() -> None:
    """Ejecuta el flujo de seguridad y dibuja la interfaz de login si no hay sesión."""
    # 1. Intentamos recuperar sesión si el usuario tiró un F5
    auth_controller.restaurar_sesion_desde_cookies()

    # 2. Si no está autenticado, bloqueamos la app con el formulario visual
    if not st.session_state.autenticado:
        st.title("🔐 Acceso al Sistema")
        
        # Variables locales de interfaz para aislar datos entre usuarios concurrentes
        email_input : str = st.text_input("Correo Electrónico")
        password_input : str = st.text_input("Contraseña", type="password")
        
        if st.button("Ingresar"):
            if not email_input or not password_input:
                st.error("Por favor, rellena todos los campos.")
                st.stop()
                
            try:
                # Delegamos la validación al controlador lógico
                if auth_controller.intentar_login(email_input, password_input):
                    st.toast("¡Bienvenido al sistema!", icon="🚀")
                    st.rerun()
            except Exception:
                st.error("Credenciales incorrectas. Revisa tu correo y contraseña.")
        
        # Detiene la ejecución para proteger las pestañas internas de app.py
        st.stop()