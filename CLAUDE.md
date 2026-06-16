# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Taller Mecánico — MVP

## Stack
- **Lenguaje**: Python (ver versión en `.python-version`)
- **Gestor de dependencias**: [uv](https://docs.astral.sh/uv/)
- **Dependencias y metadata del proyecto**: `pyproject.toml`
- **Frontend/UI**: Streamlit
- **Base de datos**: Supabase (PostgreSQL) — cliente Python `supabase`
- **Almacenamiento de archivos**: Supabase Storage buckets
- **Autenticación**: Supabase Auth (los registros de usuario se crean manualmente desde el panel de Supabase)
- NO leer ni modificar `uv.lock` — es generado automáticamente por uv
- Revisar .claudeignore para saber que archivos no debes leer

## Comandos esenciales
```bash
uv run streamlit run src/app.py                                    # ejecutar el proyecto de manera local
uv run streamlit run src/app.py --server.address 0.0.0.0          # visualizar en móviles (acceder en celular: http://192.168.1.4:8501)
uv add <paquete>                                                    # agregar dependencia
uv sync                                                             # sincronizar entorno
uv run pytest                                                       # correr tests (si aplica)
```

## Contexto del dominio
@SaaS_mecanico_vault/wiki/resumen.md

## Wiki del proyecto (contexto extendido)

Si necesitás más información sobre el proyecto — propuesta de valor, modelo de negocio, estructura de base de datos, roadmap, entrevistas de usuario, o el concepto del VHC — consultá el vault en `SaaS_mecanico_vault/`.

**Punto de entrada**: `SaaS_mecanico_vault/index.md` lista todas las páginas disponibles.

Páginas clave:
- `SaaS_mecanico_vault/wiki/resumen.md` — cambios recientes y estado actual del código
- `SaaS_mecanico_vault/wiki/overview.md` — visión general del proyecto
- `SaaS_mecanico_vault/wiki/base_de_datos.md` — tablas, campos y relaciones por fase
- `SaaS_mecanico_vault/wiki/roadmap.md` — MVP, Fase 1, Fase 2, Fase 3
- `SaaS_mecanico_vault/wiki/arquitectura_tecnica.md` — stack, módulos y decisiones técnicas
- `SaaS_mecanico_vault/wiki/propuesta_valor.md` — dolores que resuelve y ROI del cliente
- `SaaS_mecanico_vault/wiki/vhc.md` — concepto del VHC y su implementación digital

Las fuentes originales (PDFs convertidos a markdown) están en `SaaS_mecanico_vault/sources/`.

## Arquitectura de módulos

```
src/
├── app.py                     # Orquestador: inicializa DB, maneja sesión, define tabs, despacha notificaciones
├── components/
│   ├── login.py               # UI de login; bloquea con st.stop() hasta autenticar
│   ├── record_form.py         # Tab "Nuevo Ingreso": campos del formulario, reset por form_k
│   └── history_view.py        # Tab "Historial": filtros, paginación, tarjetas de servicio
├── controllers/
│   ├── auth_controller.py     # Login/logout, cookies persistentes (streamlit-cookies-controller)
│   └── record_controller.py   # Validación de inputs, construcción del payload, delega a database
├── data/
│   ├── database.py            # Cliente Supabase, guardar_servicio_relacional(), obtener_servicios(), _comprimir_imagen()
│   └── cars.json              # Referencia marcas/modelos (31 marcas, 200+ modelos)
└── utils/
    ├── utils.py               # validar_patente() — regex para formato patente chilena
    └── car_selector.py        # selectbox_marca() / selectbox_modelo() con @st.cache_data sobre cars.json
```

**Flujo de datos principal:**
1. `app.py` inicializa → `login.py` bloquea hasta autenticar vía `auth_controller`
2. Tab "Nuevo Ingreso": `record_form` → `record_controller.procesar_e_ingresar_servicio()` → `database.guardar_servicio_relacional()` → bucket Supabase
3. Tab "Historial": `history_view` → `database.obtener_servicios(filtros)` → JOINs `servicios ← vehiculos ← fotos_servicios`

## Session state clave

| Clave | Tipo | Propósito |
|---|---|---|
| `autenticado` | bool | Estado de login |
| `taller_id` | str | User ID de Supabase Auth |
| `email` | str | Email del usuario |
| `notificacion` | dict | Mensaje toast `{tipo, mensaje}` — se despacha y elimina en `app.py` |
| `procesando` | bool | Deshabilita botón submit durante guardado |
| `form_k` | int | Incrementar para resetear todos los inputs del formulario |
| `filtro_*` | varios | Estado de filtros de historial (patente, marca, modelo, diagnostico, trabajo, desde, hasta) |
| `limite_registros` | int | Paginación de historial (inicia en 5, +5 por "Cargar más") |

## Importaciones dentro de src/
Streamlit agrega `src/` al `sys.path` al ejecutar `src/app.py`. Por eso los módulos dentro de `src/` se importan **sin el prefijo `src.`**:
- ✅ `from controllers import record_controller`
- ✅ `from data import database`
- ✅ `from utils import utils`
- ❌ `from src.controllers import record_controller` ← incorrecto

`app.py` siempre debe estar en `src/`, nunca en la raíz del proyecto.

## Reglas de desarrollo
- **Después de cada cambio en el código, actualizar `SaaS_mecanico_vault/wiki/resumen.md`** indicando qué se cambió y con qué objetivo (resumen breve)
- No crear archivos de configuración alternativos sin avisar
- Preguntar antes de agregar dependencias nuevas
- Todo el código nuevo va dentro de `src/`
- Las variables de entorno se leen desde `.env` — nunca hardcodear credenciales
- Antes de crear una función nueva, verificar si ya existe lógica similar en `src/`

## Patrones y decisiones técnicas importantes
- **Imágenes**: siempre comprimir con Pillow antes de subir al bucket (máx 1080px ancho, calidad 65%). Nunca subir la imagen original directamente. Ver `database._comprimir_imagen()`.
- **Patentes**: al registrar un servicio nuevo, primero buscar si la patente ya existe en `vehiculos`. Si existe, reutilizar el registro — nunca crear duplicados. Ver `database.guardar_servicio_relacional()`.
- **Reset de formulario**: incrementar `st.session_state.form_k` para forzar re-render de todos los inputs con nuevas keys.
- **Notificaciones**: setear `st.session_state.notificacion = {"tipo": "success"|"error", "mensaje": "..."}` desde cualquier módulo; `app.py` lo consume y limpia en cada ciclo.
- **Timezone**: los timestamps de Supabase llegan en UTC — convertir a `America/Santiago` para mostrar al usuario. Ver `history_view.render_tarjeta_servicio()`.
- **Supabase Auth**: sesión manejada con `st.session_state` + cookies. No implementar lógica de roles — un solo tipo de usuario.
