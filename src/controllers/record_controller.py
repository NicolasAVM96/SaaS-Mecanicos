from typing import Any
from data import database
from utils import utils

TIPOS_VEHICULO = ["Sedan", "Hatchback", "SUV", "Pickup", "Camioneta", "Station Wagon", "Furgón", "Coupe", "Van", "Otro"]

def procesar_e_ingresar_servicio(
    nombre_cliente: str,
    telefono: str,
    rut: str,
    email_raw: str,
    direccion: str,
    patente_raw: str,
    km_raw: int,
    tipo_vehiculo: str,
    marca_raw: str,
    modelo_raw: str,
    color_raw: str,
    ano_raw: int | None,
    n_chasis_raw: str,
    diagnostico_raw: str,
    trabajo_raw: str,
    fotos_raw: list[Any],
) -> tuple[bool, str]:
    # 1. Sanitización
    patente: str = patente_raw.upper().strip()
    marca: str = marca_raw.upper().strip()
    modelo: str = modelo_raw.upper().strip()
    color: str = color_raw.upper().strip()
    diagnostico: str = diagnostico_raw.strip()
    trabajo: str = trabajo_raw.strip()
    nombre: str = nombre_cliente.strip()
    telefono_clean: str = telefono.strip()
    rut_clean: str = rut.strip()
    direccion_clean: str = direccion.strip()
    email_clean: str = email_raw.strip().lower()
    n_chasis_clean: str = n_chasis_raw.strip()

    # 2. Validaciones
    if not nombre or not telefono_clean:
        return False, "❌ Por favor, ingresa el nombre y teléfono del cliente."

    if not rut_clean or not utils.validar_rut(rut_clean):
        return False, "❌ RUT inválido. Usa el formato 12345678-9 (con o sin puntos)."

    if not direccion_clean:
        return False, "❌ Por favor, ingresa la dirección del cliente."

    if not utils.validar_patente(patente):
        return False, "❌ Patente inválida."

    if not diagnostico or not trabajo:
        return False, "❌ Por favor, completa el diagnóstico y el trabajo."

    # 3. Conversión de fotos a bytes
    fotos_bytes: list[bytes] = [f.getvalue() for f in fotos_raw] if fotos_raw else []

    # 4. Payload relacional
    vehiculo_data: dict[str, Any] = {
        "patente": patente,
        "tipo_vehiculo": tipo_vehiculo if tipo_vehiculo else None,
        "marca": marca,
        "modelo": modelo,
        "color": color,
        "kilometraje": km_raw,
    }
    if ano_raw:
        vehiculo_data["ano"] = ano_raw
    if n_chasis_clean:
        vehiculo_data["n_chasis"] = n_chasis_clean

    payload: dict[str, Any] = {
        "cliente": {
            "nombre_completo": nombre,
            "telefono": telefono_clean,
            "rut": rut_clean,
            "direccion": direccion_clean,
            **({"email": email_clean} if email_clean else {}),
        },
        "vehiculo": vehiculo_data,
        "servicio": {
            "diagnostico": diagnostico,
            "trabajo_a_realizar": trabajo,
            "fotos_bytes": fotos_bytes,
        },
    }

    servicio_id = database.guardar_servicio_relacional(payload)

    if servicio_id:
        return True, f"✅ ¡Vehículo {patente} registrado con éxito!"
    return False, "❌ No se pudo guardar el registro en la base de datos."


def procesar_servicio_vehiculo_existente(
    patente: str,
    km_raw: int,
    diagnostico_raw: str,
    trabajo_raw: str,
    fotos_raw: list[Any],
) -> tuple[bool, str]:
    diagnostico = diagnostico_raw.strip()
    trabajo = trabajo_raw.strip()

    if not diagnostico or not trabajo:
        return False, "❌ Por favor, completa el diagnóstico y el trabajo."

    if not database.buscar_vehiculo_por_patente(patente):
        return False, "❌ Patente no encontrada en el sistema."

    fotos_bytes: list[bytes] = [f.getvalue() for f in fotos_raw] if fotos_raw else []

    payload: dict[str, Any] = {
        "cliente": {},
        "vehiculo": {"patente": patente, "kilometraje": km_raw},
        "servicio": {
            "diagnostico": diagnostico,
            "trabajo_a_realizar": trabajo,
            "fotos_bytes": fotos_bytes,
        },
    }

    servicio_id = database.guardar_servicio_relacional(payload)
    if servicio_id:
        return True, f"✅ ¡Servicio registrado para el vehículo {patente}!"
    return False, "❌ No se pudo guardar el registro en la base de datos."
