from typing import Any
import streamlit as st
from data import database
from streamlit_cookies_controller import CookieController

# Centralizamos el manejo de cookies en el controlador
_cookies = CookieController()


def _obtener_perfil(user_id: str) -> dict:
    """Consulta la tabla perfiles y retorna {taller_id, rol, nombre} del usuario."""
    res = database.supabase.table("perfiles") \
        .select("taller_id, rol, nombre") \
        .eq("id", user_id) \
        .single() \
        .execute()
    return res.data


def restaurar_sesion_desde_cookies() -> None:
    """Revisa las cookies del navegador y restaura la sesión en session_state si existen."""
    cookie_autenticado = _cookies.get("session_autenticado")
    cookie_taller_id = _cookies.get("session_taller_id")
    cookie_email = _cookies.get("session_email")
    cookie_rol = _cookies.get("session_rol")

    if 'autenticado' not in st.session_state:
        if cookie_autenticado == "True" and cookie_taller_id and cookie_email:
            st.session_state.autenticado = True
            st.session_state.taller_id = cookie_taller_id
            st.session_state.email = cookie_email
            st.session_state.rol = cookie_rol or "admin"
        else:
            st.session_state.autenticado = False

def intentar_login(email_input: str, password_input: str) -> bool:
    """Valida credenciales en Supabase, inicializa el session_state y guarda cookies.

    Retorna True si el login fue exitoso, lanza una excepción si falla.
    """
    res = database.supabase.auth.sign_in_with_password({
        "email": email_input.strip(),
        "password": password_input
    })

    perfil = _obtener_perfil(res.user.id)

    st.session_state.autenticado = True
    st.session_state.taller_id = perfil["taller_id"]   # UUID del taller (no del usuario)
    st.session_state.rol = perfil["rol"]
    st.session_state.nombre = perfil.get("nombre", "")
    st.session_state.email = res.user.email
    st.session_state.supabase_session = res.session

    _cookies.set("session_autenticado", "True")
    _cookies.set("session_taller_id", str(perfil["taller_id"]))
    _cookies.set("session_email", str(res.user.email))
    _cookies.set("session_rol", str(perfil["rol"]))

    return True

def cambiar_contrasena(nueva: str, confirmar: str) -> tuple[bool, str]:
    if not nueva or not confirmar:
        return False, "❌ Completá ambos campos."
    if nueva != confirmar:
        return False, "❌ Las contraseñas no coinciden."
    if len(nueva) < 6:
        return False, "❌ La contraseña debe tener al menos 6 caracteres."

    try:
        session = st.session_state.get("supabase_session")
        if session:
            database.supabase.auth.set_session(session.access_token, session.refresh_token)
        database.supabase.auth.update_user({"password": nueva})
        # Re-autenticar para obtener sesión fresca (update_user invalida el token anterior)
        email = st.session_state.get("email", "")
        res = database.supabase.auth.sign_in_with_password({"email": email, "password": nueva})
        st.session_state.supabase_session = res.session
        return True, "✅ Contraseña actualizada con éxito."
    except Exception:
        return False, "❌ No se pudo cambiar la contraseña. Cerrá sesión, volvé a entrar e intentá de nuevo."


def cerrar_sesion() -> None:
    """Limpia de raíz la memoria volátil del servidor y destruye las cookies del cliente."""
    st.session_state.autenticado = False
    st.session_state.taller_id = None
    st.session_state.email = None
    st.session_state.rol = None
    st.session_state.nombre = None

    _cookies.remove("session_autenticado")
    _cookies.remove("session_taller_id")
    _cookies.remove("session_email")
    _cookies.remove("session_rol")
    st.rerun()