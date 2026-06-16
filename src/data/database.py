import io
import streamlit as st
from typing import Any
from datetime import date
from supabase import create_client, Client
from dotenv import load_dotenv
from PIL import Image
import os
import uuid

load_dotenv()

SUPABASE_URL : str = os.getenv("SUPABASE_URL")
SUPABASE_KEY : str = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

MAX_FOTO_WIDTH = 1080
FOTO_QUALITY = 65
MAX_FOTOS_POR_SERVICIO = 8

def inicializar_db() -> None:
    pass

def _comprimir_imagen(foto_bytes: bytes) -> bytes:
    img = Image.open(io.BytesIO(foto_bytes))
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    if img.width > MAX_FOTO_WIDTH:
        ratio = MAX_FOTO_WIDTH / img.width
        img = img.resize((MAX_FOTO_WIDTH, int(img.height * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=FOTO_QUALITY, optimize=True)
    return buf.getvalue()

def buscar_vehiculo_por_patente(patente: str) -> dict | None:
    res = (
        supabase.table("vehiculos")
        .select("*, clientes(nombre_completo, rut, email, telefono, direccion)")
        .eq("patente", patente.upper().strip())
        .execute()
    )
    return res.data[0] if res.data else None


def guardar_servicio_relacional(payload: dict[str, Any]) -> str | None:
    cliente_data: dict = payload["cliente"]
    vehiculo_data: dict = payload["vehiculo"]
    servicio_data: dict = payload["servicio"]
    fotos_bytes: list[bytes] = servicio_data.pop("fotos_bytes", [])

    try:
        # 1. Verificar si la patente ya existe
        patente: str = vehiculo_data["patente"]
        existente = supabase.table("vehiculos").select("id").eq("patente", patente).execute()

        if existente.data:
            vehiculo_id: str = existente.data[0]["id"]
            if vehiculo_data.get("kilometraje"):
                supabase.table("vehiculos").update({"kilometraje": vehiculo_data["kilometraje"]}).eq("id", vehiculo_id).execute()
        else:
            # 2. Crear cliente
            cliente_res = supabase.table("clientes").insert(cliente_data).execute()
            cliente_id: str = cliente_res.data[0]["id"]

            # 3. Crear vehículo vinculado al cliente
            vehiculo_res = supabase.table("vehiculos").insert({
                **vehiculo_data,
                "cliente_id": cliente_id
            }).execute()
            vehiculo_id = vehiculo_res.data[0]["id"]

        # 4. Crear registro de servicio
        servicio_res = supabase.table("servicios").insert({
            "vehiculo_id": vehiculo_id,
            "diagnostico": servicio_data["diagnostico"],
            "trabajo_a_realizar": servicio_data["trabajo_a_realizar"],
        }).execute()
        servicio_id: str = servicio_res.data[0]["id"]

        # 5. Subir fotos al bucket y guardar URLs
        for foto in fotos_bytes[:MAX_FOTOS_POR_SERVICIO]:
            try:
                foto_comprimida = _comprimir_imagen(foto)
                file_path: str = f"{servicio_id}/{uuid.uuid4()}.jpg"
                supabase.storage.from_("fotos-servicios").upload(
                    path=file_path,
                    file=foto_comprimida,
                    file_options={"content-type": "image/jpeg"}
                )
                url_res = supabase.storage.from_("fotos-servicios").get_public_url(file_path)
                url_publica: str = getattr(url_res, "public_url", url_res)
                supabase.table("fotos_servicios").insert({
                    "servicio_id": servicio_id,
                    "url_foto": url_publica
                }).execute()
            except Exception as e_foto:
                print(f"ERROR en foto: {e_foto}")
                continue

        return servicio_id

    except Exception as e:
        print(f"ERROR CRÍTICO: {e}")
        st.error(f"Error al guardar el registro: {e}")
        return None


def obtener_servicios(
    patente: str = "",
    marca: str = "",
    modelo: str = "",
    diagnostico: str = "",
    trabajo: str = "",
    fecha_inicio: date | None = None,
    fecha_fin: date | None = None,
    nombre_cliente: str = "",
    rut_cliente: str = "",
    limite: int = 5,
) -> list[dict[str, Any]]:
    try:
        query = (
            supabase.table("servicios")
            .select("*, vehiculos!inner(patente, tipo_vehiculo, marca, modelo, color, kilometraje, ano, n_chasis, clientes(nombre_completo, rut, email)), fotos_servicios(url_foto)")
            .order("fecha_ingreso", desc=True)
            .limit(limite)
        )

        if nombre_cliente or rut_cliente:
            sub = supabase.table("vehiculos").select("id, clientes!inner(nombre_completo, rut)")
            if nombre_cliente:
                sub = sub.filter("clientes.nombre_completo", "ilike", f"%{nombre_cliente}%")
            if rut_cliente:
                sub = sub.filter("clientes.rut", "ilike", f"%{rut_cliente}%")
            ids = [r["id"] for r in sub.execute().data]
            if not ids:
                return []
            query = query.in_("vehiculo_id", ids)

        if patente:
            query = query.filter("vehiculos.patente", "ilike", f"%{patente}%")
        if marca:
            query = query.filter("vehiculos.marca", "ilike", f"%{marca}%")
        if modelo:
            query = query.filter("vehiculos.modelo", "ilike", f"%{modelo}%")
        if diagnostico:
            query = query.ilike("diagnostico", f"%{diagnostico}%")
        if trabajo:
            query = query.ilike("trabajo_a_realizar", f"%{trabajo}%")
        if fecha_inicio:
            query = query.gte("fecha_ingreso", f"{fecha_inicio}T00:00:00")
        if fecha_fin:
            query = query.lte("fecha_ingreso", f"{fecha_fin}T23:59:59")

        return query.execute().data

    except Exception as e:
        st.error(f"Error al obtener datos: {e}")
        return []


def contar_visitas_vehiculo(patente: str) -> int:
    try:
        res = (
            supabase.table("servicios")
            .select("id, vehiculos!inner(patente)", count="exact")
            .filter("vehiculos.patente", "eq", patente)
            .execute()
        )
        return res.count or 0
    except Exception:
        return 0
