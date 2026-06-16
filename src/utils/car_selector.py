import json
import streamlit as st
from pathlib import Path
from typing import Callable

@st.cache_data
def _cargar_autos() -> dict[str, list[str]]:
    path = Path(__file__).parent.parent / "data" / "cars.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def selectbox_marca(
    key: str,
    label: str = "Marca",
    required: bool = False,
    on_change: Callable | None = None,
) -> str:
    datos = _cargar_autos()
    opciones = list(datos.keys())
    if not required:
        opciones = [""] + opciones
    return st.selectbox(
        label,
        options=opciones,
        key=key,
        on_change=on_change,
        format_func=lambda x: "Todas las marcas" if x == "" else x,
    )

def selectbox_modelo(
    marca: str,
    key: str,
    label: str = "Modelo",
    required: bool = False,
) -> str:
    datos = _cargar_autos()
    modelos = list(datos.get(marca, [])) if marca else []
    if not required:
        modelos = [""] + modelos
    return st.selectbox(
        label,
        options=modelos,
        key=key,
        disabled=(not bool(marca) and not required),
        format_func=lambda x: "Todos los modelos" if x == "" else x,
    )
