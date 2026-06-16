import re

def validar_patente(patente):
    patron = r"^[A-Z]{2,4}-?[0-9]{2,4}$"
    return re.match(patron, patente)

def validar_rut(rut: str) -> bool:
    """Valida formato RUT chileno: 12345678-9 o 12.345.678-9 (con/sin puntos). No valida dígito verificador."""
    rut_limpio = rut.replace(".", "").strip()
    return bool(re.match(r"^\d{7,8}-[\dkK]$", rut_limpio))