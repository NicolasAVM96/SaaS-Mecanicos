import streamlit as st
from typing import Any
from controllers import record_controller
from utils import car_selector
from data import database
from data.database import MAX_FOTOS_POR_SERVICIO


def render_registro_tab() -> None:
    if "procesando" not in st.session_state:
        st.session_state.procesando = False
    if "form_k" not in st.session_state:
        st.session_state.form_k = 0
    if "vehiculo_buscado" not in st.session_state:
        st.session_state.vehiculo_buscado = None

    st.radio(
        "Tipo de ingreso",
        ["Vehículo nuevo", "Vehículo existente"],
        horizontal=True,
        key="modo_ingreso",
    )

    k = st.session_state.form_k

    if st.session_state.modo_ingreso == "Vehículo existente":
        _render_form_existente(k)
    else:
        _render_form_nuevo(k)


# ── Modo: Vehículo existente ────────────────────────────────────────────────

def _buscar_patente_callback() -> None:
    k = st.session_state.form_k
    patente = st.session_state.get(f"exist_patente_{k}", "").upper().strip()
    if patente:
        st.session_state.vehiculo_buscado = database.buscar_vehiculo_por_patente(patente)
    else:
        st.session_state.vehiculo_buscado = None


def _render_form_existente(k: int) -> None:
    st.markdown("### Buscar vehículo por patente")
    st.text_input(
        "Patente",
        placeholder="Ej: ABCD12",
        key=f"exist_patente_{k}",
        on_change=_buscar_patente_callback,
    )

    patente_actual = st.session_state.get(f"exist_patente_{k}", "").upper().strip()
    vehiculo = st.session_state.vehiculo_buscado

    if not patente_actual:
        st.info("Ingresa la patente del vehículo para cargar sus datos.")
        return

    if vehiculo is None:
        st.warning(f"No se encontró ningún vehículo con la patente **{patente_actual}**. Usá el modo 'Vehículo nuevo' para registrarlo.")
        return

    cliente: dict = vehiculo.get("clientes") or {}
    _render_ficha_readonly(vehiculo, cliente)

    st.markdown("### Datos del Servicio")
    km = st.number_input("Kilometraje actual", min_value=0, step=1000, value=vehiculo.get("kilometraje", 0), key=f"exist_km_{k}")
    diagnostico = st.text_area("Diagnóstico", placeholder="Escribe el síntoma o falla...", height=100, key=f"exist_diagnostico_{k}")
    trabajo = st.text_area("Trabajo a realizar", placeholder="Describe las tareas a ejecutar...", height=120, key=f"exist_trabajo_{k}")
    fotos: list[Any] = st.file_uploader(
        f"Fotos de evidencia (máx {MAX_FOTOS_POR_SERVICIO})",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key=f"exist_fotos_{k}",
    )
    if fotos and len(fotos) > MAX_FOTOS_POR_SERVICIO:
        st.warning(f"Solo se subirán las primeras {MAX_FOTOS_POR_SERVICIO} fotos.")

    st.write("")
    if st.button("Guardar Registro", type="primary", use_container_width=True, disabled=st.session_state.procesando):
        st.session_state.procesando = True
        with st.spinner("Guardando registro..."):
            exito, mensaje = record_controller.procesar_servicio_vehiculo_existente(
                patente=patente_actual,
                km_raw=km,
                diagnostico_raw=diagnostico,
                trabajo_raw=trabajo,
                fotos_raw=fotos,
            )
        if exito:
            st.session_state.notificacion = {"tipo": "success", "texto": mensaje}
            st.session_state.form_k += 1
            st.session_state.vehiculo_buscado = None
            st.session_state.procesando = False
            st.rerun()
        else:
            st.error(mensaje)
            st.session_state.procesando = False


def _render_ficha_readonly(vehiculo: dict, cliente: dict) -> None:
    marca = vehiculo.get("marca", "")
    modelo = vehiculo.get("modelo", "")
    patente = vehiculo.get("patente", "—")
    propietario = cliente.get("nombre_completo") or "—"

    with st.expander(f"Vehículo encontrado — Patente: {patente} — {marca} {modelo}", expanded=True):
        st.markdown("### Datos del Vehículo")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.write("**Tipo:**")
            st.write(vehiculo.get("tipo_vehiculo") or "—")
        with c2:
            st.write("**Marca / Modelo:**")
            st.write(f"{marca} {modelo}".strip() or "—")
        with c3:
            ano = vehiculo.get("ano")
            st.write("**Año / Color:**")
            st.write(f"{ano or '—'} / {vehiculo.get('color') or '—'}")
        with c4:
            n_chasis = vehiculo.get("n_chasis")
            st.write("**N° Chasis:**")
            st.write(n_chasis if n_chasis else "—")

        st.divider()

        st.markdown("### Datos del Propietario")
        c5, c6, c7 = st.columns(3)
        with c5:
            st.write("**Nombre:**")
            st.write(propietario)
        with c6:
            st.write("**RUT:**")
            st.write(cliente.get("rut") or "—")
        with c7:
            st.write("**Teléfono:**")
            st.write(cliente.get("telefono") or "—")


# ── Modo: Vehículo nuevo ────────────────────────────────────────────────────

def _render_form_nuevo(k: int) -> None:
    st.markdown("### Datos del Cliente")
    nombre = st.text_input("Nombre completo", placeholder="Ej: Juan Pérez", key=f"reg_nombre_{k}")
    col_rut, col_tel = st.columns(2)
    with col_rut:
        rut = st.text_input("RUT", placeholder="Ej: 12.345.678-9", key=f"reg_rut_{k}")
    with col_tel:
        telefono = st.text_input("Teléfono / WhatsApp", placeholder="Ej: +56912345678", key=f"reg_tel_{k}")
    col_email, col_dir = st.columns([1, 1])
    with col_email:
        email = st.text_input("Email (opcional)", placeholder="Ej: juan@gmail.com", key=f"reg_email_{k}")
    with col_dir:
        direccion = st.text_input("Dirección", placeholder="Ej: Av. Principal 123, Santiago", key=f"reg_direccion_{k}")

    st.markdown("### Datos del Vehículo")
    col_patente, col_tipo = st.columns(2)
    with col_patente:
        patente = st.text_input("Patente", placeholder="Ej: ABCD12", key=f"reg_patente_{k}")
    with col_tipo:
        tipo_vehiculo = st.selectbox(
            "Tipo de vehículo",
            options=[""] + record_controller.TIPOS_VEHICULO,
            format_func=lambda x: "Selecciona..." if x == "" else x,
            key=f"reg_tipo_{k}",
        )

    col_km, col_ano = st.columns(2)
    with col_km:
        km = st.number_input("Kilometraje actual", min_value=0, step=1000, value=0, key=f"reg_km_{k}")
    with col_ano:
        ano = st.number_input("Año", min_value=1970, max_value=2030, value=None, placeholder="Ej: 2018", key=f"reg_ano_{k}")

    marca = car_selector.selectbox_marca(key=f"reg_marca_{k}", label="Marca", required=True)
    modelo = car_selector.selectbox_modelo(marca, key=f"reg_modelo_{k}", label="Modelo", required=True)

    col_color, col_chasis = st.columns(2)
    with col_color:
        color = st.text_input("Color", placeholder="Ej: GRIS METÁLICO", key=f"reg_color_{k}")
    with col_chasis:
        n_chasis = st.text_input("N° de Chasis (opcional)", placeholder="Ej: 9FBSS57H2AB123456", key=f"reg_chasis_{k}")

    st.markdown("### Detalles del Servicio")
    diagnostico = st.text_area("Diagnóstico", placeholder="Escribe el síntoma o falla...", height=100, key=f"reg_diagnostico_{k}")
    trabajo = st.text_area("Trabajo a realizar", placeholder="Describe las tareas a ejecutar...", height=120, key=f"reg_trabajo_{k}")
    fotos: list[Any] = st.file_uploader(
        f"Fotos de evidencia (máx {MAX_FOTOS_POR_SERVICIO})",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key=f"reg_fotos_{k}",
    )
    if fotos and len(fotos) > MAX_FOTOS_POR_SERVICIO:
        st.warning(f"Solo se subirán las primeras {MAX_FOTOS_POR_SERVICIO} fotos.")

    st.write("")
    if st.button("Guardar Registro", type="primary", use_container_width=True, disabled=st.session_state.procesando):
        st.session_state.procesando = True

        with st.spinner("Guardando registro..."):
            exito, mensaje = record_controller.procesar_e_ingresar_servicio(
                nombre_cliente=nombre,
                telefono=telefono,
                rut=rut,
                email_raw=email,
                direccion=direccion,
                patente_raw=patente,
                km_raw=km,
                tipo_vehiculo=tipo_vehiculo,
                marca_raw=marca,
                modelo_raw=modelo,
                color_raw=color,
                ano_raw=int(ano) if ano else None,
                n_chasis_raw=n_chasis,
                diagnostico_raw=diagnostico,
                trabajo_raw=trabajo,
                fotos_raw=fotos,
            )

        if exito:
            st.session_state.notificacion = {"tipo": "success", "texto": mensaje}
            st.session_state.form_k += 1
            st.session_state.procesando = False
            st.rerun()
        else:
            st.error(mensaje)
            st.session_state.procesando = False
