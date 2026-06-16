import streamlit as st
from typing import Any
from datetime import datetime, date
from zoneinfo import ZoneInfo
from data import database
from utils import car_selector, utils


def render_historial_tab() -> None:
    st.subheader("Historial de Servicios")

    inicializar_estados_historial()

    patente, marca, modelo, fecha_ini, fecha_fin, diagnostico, trabajo, nombre_cliente, rut_cliente = render_filtros_historial()

    with st.spinner("Cargando historial desde la nube..."):
        registros: list[dict[str, Any]] = database.obtener_servicios(
            patente=patente,
            marca=marca,
            modelo=modelo,
            diagnostico=diagnostico,
            trabajo=trabajo,
            fecha_inicio=fecha_ini,
            fecha_fin=fecha_fin,
            nombre_cliente=nombre_cliente,
            rut_cliente=rut_cliente,
            limite=st.session_state.limite_registros,
        )

    if registros:
        if utils.validar_patente(patente):
            total = database.contar_visitas_vehiculo(patente)
            render_ficha_vehiculo(registros[0], total)
            st.divider()

        st.write(f"Mostrando {len(registros)} registros encontrados:")

        for reg in registros:
            render_tarjeta_servicio(reg)

        st.write("")
        if len(registros) == st.session_state.limite_registros:
            col_btn_centrar = st.columns([2, 1, 2])
            with col_btn_centrar[1]:
                if st.button("Cargar más", type="secondary", use_container_width=True):
                    st.session_state.limite_registros += 5
                    st.rerun()
        else:
            st.info("Has llegado al final del historial. No hay más registros.")
    else:
        tipo_busqueda = st.session_state.get("filtro_tipo_busqueda", "Vehículo")
        hay_filtros = patente or marca or modelo or diagnostico or trabajo or nombre_cliente or rut_cliente
        if not hay_filtros:
            st.warning("El taller aún no tiene registros guardados.")
        elif tipo_busqueda == "Cliente":
            st.warning("No hay registros para ese cliente.")
        else:
            st.warning(f"No hay registros con la patente '{patente}'." if patente else "No se encontraron registros con esos filtros.")


def inicializar_estados_historial() -> None:
    if "limite_registros" not in st.session_state:
        st.session_state.limite_registros = 5
    for key in ("filtro_patente", "filtro_marca", "filtro_modelo", "filtro_diagnostico", "filtro_trabajo", "filtro_nombre_cliente", "filtro_rut_cliente"):
        if key not in st.session_state:
            st.session_state[key] = ""
    for key in ("filtro_desde", "filtro_hasta"):
        if key not in st.session_state:
            st.session_state[key] = None
    if "filtro_tipo_busqueda" not in st.session_state:
        st.session_state.filtro_tipo_busqueda = "Vehículo"


def limpiar_filtros_callback() -> None:
    for key in ("filtro_patente", "filtro_marca", "filtro_modelo", "filtro_diagnostico", "filtro_trabajo", "filtro_nombre_cliente", "filtro_rut_cliente"):
        st.session_state[key] = ""
    st.session_state.filtro_desde = None
    st.session_state.filtro_hasta = None
    st.session_state.limite_registros = 5


def _reset_filtro_modelo() -> None:
    st.session_state.filtro_modelo = ""


def render_filtros_historial() -> tuple[str, str, str, date, date, str, str, str, str]:
    st.radio(
        "Buscar por",
        ["Vehículo", "Cliente"],
        horizontal=True,
        key="filtro_tipo_busqueda",
    )
    tipo = st.session_state.filtro_tipo_busqueda

    nombre_cliente = ""
    rut_cliente = ""
    patente = ""
    marca = ""
    modelo = ""
    fecha_ini = None
    fecha_fin = None
    diagnostico = ""
    trabajo = ""

    if tipo == "Cliente":
        col_nombre, col_rut = st.columns(2)
        with col_nombre:
            nombre_cliente = st.text_input("Nombre del cliente", placeholder="Ej: Juan Pérez", key="filtro_nombre_cliente").strip()
        with col_rut:
            rut_cliente = st.text_input("RUT del cliente", placeholder="Ej: 12345678-9", key="filtro_rut_cliente").strip()
    else:
        col_patente, col_marca, col_modelo, col_desde, col_hasta = st.columns([1.2, 1.2, 1.2, 1.5, 1.5])
        with col_patente:
            patente = st.text_input("Patente", placeholder="Ej: ABCD12", key="filtro_patente").upper().strip()
        with col_marca:
            marca = car_selector.selectbox_marca(key="filtro_marca", label="Marca", on_change=_reset_filtro_modelo)
        with col_modelo:
            modelo = car_selector.selectbox_modelo(marca, key="filtro_modelo", label="Modelo")
        with col_desde:
            fecha_ini = st.date_input("Desde", key="filtro_desde", format="DD/MM/YYYY")
        with col_hasta:
            fecha_fin = st.date_input("Hasta", key="filtro_hasta", format="DD/MM/YYYY")

        col_diagn, col_trabaj = st.columns([3, 3])
        with col_diagn:
            diagnostico = st.text_input("Buscar en Diagnóstico", placeholder="Ej: fuga...", key="filtro_diagnostico").upper().strip()
        with col_trabaj:
            trabajo = st.text_input("Buscar en Trabajo a realizar", placeholder="Ej: frenos...", key="filtro_trabajo").upper().strip()

    hay_filtros = patente or marca or modelo or diagnostico or trabajo or nombre_cliente or rut_cliente or fecha_ini or fecha_fin
    if hay_filtros:
        st.button("Limpiar Filtros", type="secondary", on_click=limpiar_filtros_callback)

    return patente, marca, modelo, fecha_ini, fecha_fin, diagnostico, trabajo, nombre_cliente, rut_cliente


def render_ficha_vehiculo(reg: dict[str, Any], total_visitas: int) -> None:
    vehiculo: dict = reg.get("vehiculos", {})
    cliente: dict = vehiculo.get("clientes", {})

    patente = vehiculo.get("patente", "—")
    propietario = cliente.get("nombre_completo") or "—"
    marca = vehiculo.get("marca", "")
    modelo = vehiculo.get("modelo", "")

    header = f"Resumen del vehiculo — Patente: {patente} — Marca: {marca} — Modelo: {modelo}"

    with st.expander(header, expanded=True):
        st.markdown("### Datos del Vehículo")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Kilometraje", f"{vehiculo.get('kilometraje', 0):,} km")
        with c2:
            st.write("**Tipo:**")
            st.write(vehiculo.get("tipo_vehiculo") or "—")
        with c3:
            ano = vehiculo.get("ano")
            st.write("**Año / Color:**")
            st.write(f"{ano or '—'} / {vehiculo.get('color') or '—'}")
        with c4:
            n_chasis = vehiculo.get("n_chasis")
            st.write("**N° Chasis:**")
            st.write(n_chasis if n_chasis else "—")

        st.divider()

        st.markdown("### Último Servicio Registrado")
        col_diag, col_trab = st.columns(2)
        with col_diag:
            st.info(f"**Diagnóstico:**\n\n{reg.get('diagnostico') or '—'}")
        with col_trab:
            st.success(f"**Trabajo a Realizar:**\n\n{reg.get('trabajo_a_realizar') or '—'}")

        st.caption(f"Visitas totales registradas: {total_visitas}")


def render_tarjeta_servicio(reg: dict[str, Any]) -> None:
    vehiculo: dict = reg.get("vehiculos", {})

    try:
        fecha_utc = datetime.fromisoformat(reg["fecha_ingreso"].replace("Z", "+00:00"))
        fecha_chile = fecha_utc.astimezone(ZoneInfo("America/Santiago"))
        fecha_formateada = fecha_chile.strftime("%d/%m/%Y %H:%M")
    except Exception:
        fecha_formateada = reg.get("fecha_ingreso", "Sin fecha")

    header = (
        f"Patente: {vehiculo.get('patente')} — "
        f"Marca: {vehiculo.get('marca')} — "
        f"Modelo: {vehiculo.get('modelo')} — "
        f"Ingreso: {fecha_formateada}"
    )

    with st.expander(header):
        st.markdown("### Ficha Técnica")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Kilometraje", f"{vehiculo.get('kilometraje', 0):,} km")
        with c2:
            tipo = vehiculo.get("tipo_vehiculo") or "—"
            st.write("**Tipo:**")
            st.write(tipo)
        with c3:
            ano = vehiculo.get("ano")
            st.write("**Año / Color:**")
            st.write(f"{ano or '—'} / {vehiculo.get('color') or '—'}")
        with c4:
            n_chasis = vehiculo.get("n_chasis")
            if n_chasis:
                st.write("**N° Chasis:**")
                st.write(n_chasis)

        st.divider()

        st.markdown("### Detalles del Servicio")
        col_diag, col_trab = st.columns(2)
        with col_diag:
            st.info(f"**Diagnóstico:**\n\n{reg.get('diagnostico')}")
        with col_trab:
            st.success(f"**Trabajo a Realizar:**\n\n{reg.get('trabajo_a_realizar')}")

        fotos: list[dict] = reg.get("fotos_servicios", [])
        if fotos:
            st.divider()
            st.markdown("### Galería de Evidencias")
            cols = st.columns(3)
            for idx, foto_obj in enumerate(fotos):
                with cols[idx % 3]:
                    st.image(foto_obj["url_foto"], caption=f"Evidencia {idx + 1}", width="stretch")
