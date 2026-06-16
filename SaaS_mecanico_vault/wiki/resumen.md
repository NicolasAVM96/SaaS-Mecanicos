# Resumen del Proyecto — SaaS Automotriz MVP

## ¿Qué es este proyecto?
Sistema de gestión para un **mecánico independiente**. El objetivo es digitalizar el flujo completo de un vehículo: desde su ingreso hasta su entrega, de forma rápida, simple y ordenada desde el celular.

Resuelve tres problemas concretos:
1. **Tiempo en burocracia**: registrar el vehículo y la orden de trabajo en papel es lento. Este sistema lo hace desde el celular en minutos.
2. **Disputas con clientes**: sin registro fotográfico de daños previos, el mecánico queda expuesto. El sistema obliga a registrar fotos de evidencia vinculadas al servicio.
3. **Desorden en el historial**: sin base de datos, es difícil encontrar el historial de un auto. Aquí se puede buscar por patente, marca, modelo, diagnóstico, tipo de trabajo y rango de fechas.

## Estado actual
El sistema ya tiene:
- Login con Supabase Auth
- Registro de vehículo con datos de cliente (nombre, RUT, teléfono, dirección), vehículo (patente, tipo, KM, año, marca, modelo, color, n° chasis) y servicio (diagnóstico, trabajo, fotos)
- Deduplicación de patentes: si la patente ya existe en `vehiculos`, se reutiliza el registro en lugar de crear uno nuevo
- Historial vehicular con filtros (patente, marca, modelo, diagnóstico, trabajo, rango de fechas) mostrando los últimos 5 registros (expandible)
- Ficha resumen del vehículo (tipo, marca/modelo, año, visitas totales) al buscar por patente en el historial
- Modelo de datos relacional implementado: `clientes` → `vehiculos` → `servicios` → `fotos_servicios` con RLS activo en todas las tablas

Pendiente de implementar:
- (ninguno para el MVP core)

## Historial de cambios
- **2026-06-16**: Modo "Vehículo existente" en el formulario de ingreso. Se agregó radio toggle "Vehículo nuevo / Vehículo existente" al tope del formulario. En modo existente: el mecánico ingresa la patente, se busca automáticamente con `on_change` (`database.buscar_vehiculo_por_patente()`), si existe muestra una ficha read-only con datos del vehículo y propietario, y solo pide KM, diagnóstico, trabajo y fotos. El KM se actualiza en el registro existente del vehículo. Se agregó `buscar_vehiculo_por_patente()` en `database.py`, `procesar_servicio_vehiculo_existente()` en `record_controller.py`, y se refactorizó `record_form.py` separando `_render_form_nuevo()` y `_render_form_existente()`. Objetivo: evitar re-ingresar datos estáticos del vehículo en visitas repetidas.
- **2026-06-16**: Filtros de historial por cliente + email + ficha de vehículo mejorada. Se agregó toggle radio "Buscar por: Vehículo / Cliente" en el historial; al elegir Cliente se muestran filtros por nombre y RUT (via sub-query vehiculos→clientes). Se agregó campo email opcional al formulario de ingreso y al payload del cliente (columna `clientes.email` ya existía). La ficha del vehículo ahora solo aparece con patente completa y válida (`validar_patente()`), muestra propietario, 2 filas de métricas (tipo, marca/modelo, año, color, KM, visitas reales via `contar_visitas_vehiculo()`), y último diagnóstico/trabajo. SELECT de `obtener_servicios()` actualizado para incluir `clientes` anidado en `vehiculos`. Objetivo: permitir buscar por cliente, registrar email y mostrar ficha completa del vehículo.
- **2026-06-11**: Migración al modelo relacional. Se crearon las tablas `clientes`, `vehiculos`, `servicios` y `fotos_servicios` en Supabase con RLS habilitado. Se reescribió `database.py` con `guardar_servicio_relacional()` (deduplicación por patente) y `obtener_servicios()` (join con vehiculos). Se actualizó `record_controller.py`, `record_form.py` (agrega campos de cliente) y `history_view.py` (nuevos nombres de columna). Objetivo: pasar de una tabla plana a un esquema normalizado.
- **2026-06-11**: Compresión de imágenes y límite de fotos. Se agregó Pillow como dependencia. Se implementó `_comprimir_imagen()` en `database.py` (máx 1080px ancho, calidad 65%, conversión a JPEG). Las fotos se comprimen antes de subir al bucket. Se definió `MAX_FOTOS_POR_SERVICIO = 8` como constante compartida entre `database.py` y `record_form.py`. El formulario muestra advertencia si se suben más de 8 fotos y descarta las excedentes. Objetivo: reducir uso de almacenamiento y establecer límite operativo.
- **2026-06-16**: Fix cambiar_contrasena — error falso y sesión invalidada. `update_user()` retorna `UserResponse` sin atributo `.session`, lo que lanzaba `AttributeError` capturado por el `except`, mostrando error al usuario aunque la contraseña sí cambiaba. Además, `update_user` invalida el token anterior, rompiendo RLS en queries posteriores. Fix: eliminar acceso a `res.session` tras `update_user`; en su lugar, llamar `sign_in_with_password` con el email y la nueva contraseña para obtener sesión fresca y guardarla en `supabase_session`. Objetivo: que el cambio de contraseña muestre éxito y el historial siga funcionando sin necesidad de cerrar sesión.
- **2026-06-16**: Cambio de contraseña desde el sidebar. Se agregó `cambiar_contrasena()` en `auth_controller.py` (valida campos, longitud mínima y coincidencia). El formulario vive en un expander del sidebar en `app.py`. Requiere sesión activa de Supabase — se guarda `supabase_session` en `session_state` al hacer login. Objetivo: permitir al mecánico cambiar su contraseña sin acceder al panel de Supabase.
- **2026-06-16**: Campos extendidos de cliente y vehículo. Se agregaron RUT (con validación de formato chileno en `utils.validar_rut()`) y dirección como campos obligatorios del cliente. Se agregó tipo de vehículo (dropdown: Sedan, Hatchback, SUV, Pickup, etc.), año y n° de chasis al formulario de ingreso. Se actualizó la BD con 3 nuevas columnas (`clientes.rut`, `clientes.direccion`, `vehiculos.tipo_vehiculo`). En el historial, al filtrar por patente, se muestra una ficha resumen del vehículo con tipo, marca/modelo, año y cantidad de visitas. Objetivo: cubrir el feedback de usuario sobre datos faltantes de cliente y vehículo.
- **2026-06-11**: Selectboxes buscables para marca y modelo. Se agregó `src/utils/car_selector.py` con dos funciones reutilizables (`selectbox_marca`, `selectbox_modelo`) que leen `src/data/cars.json` (30 marcas con sus modelos). Se integró en `record_form.py` (fuera del form para rerenderizado dinámico) y en `history_view.py` (filtros con callback de reset de modelo al cambiar marca). Objetivo: reemplazar text inputs libres por selectboxes con búsqueda para estandarizar datos de marca y modelo.

## Alcance del MVP — qué está dentro y qué no
**Dentro del MVP:**
- Un solo usuario (el mecánico independiente)
- Registro y gestión de servicios/órdenes de trabajo
- Historial por vehículo con fotos de evidencia
- Búsqueda y filtros del historial

**Fuera del MVP (fases posteriores):**
- Multi-tenant (soporte para múltiples talleres)
- Roles y jerarquía (admin / mecánico)
- Notificaciones por WhatsApp
- VHC digital (Vehicle Health Check) con plantillas
- Auditoría de ediciones
- Dashboard financiero y contabilidad
- Integración con API de patentes chilenas
- Asignación de tareas a mecánicos

## Modelo de datos (4 tablas)

### `clientes`
| Campo | Tipo | Notas |
|---|---|---|
| id | uuid | PK |
| nombre_completo | varchar(150) | |
| telefono | varchar(20) | |
| email | varchar(100) | Nullable |

### `vehiculos`
| Campo | Tipo | Notas |
|---|---|---|
| id | uuid | PK |
| cliente_id | uuid | FK → clientes.id |
| patente | varchar(10) | Única |
| marca | varchar | |
| modelo | varchar | |
| color | varchar | |
| ano | integer | Nullable |
| kilometraje | integer | |
| n_chasis | varchar(50) | Nullable |
| n_motor | varchar(50) | Nullable |

### `servicios`
| Campo | Tipo | Notas |
|---|---|---|
| id | uuid | PK |
| vehiculo_id | uuid | FK → vehiculos.id |
| diagnostico | text | |
| trabajo_a_realizar | text | |
| fecha_ingreso | timestamp | Default now() |
| fecha_entrega | timestamp | Nullable |


### `fotos_servicios`
| Campo | Tipo | Notas |
|---|---|---|
| id | uuid | PK |
| servicio_id | uuid | FK → servicios.id (cascade delete) |
| url_foto | text | URL pública del bucket de Supabase |
| fecha_subida | timestamp | Default now() |

## Reglas de negocio críticas
- **Patentes únicas**: no pueden existir dos vehículos con la misma patente. Al ingresar una patente, buscar primero si ya existe y reutilizar ese registro.
- **Fotos**: máximo 8-10 por servicio. Siempre comprimir con Pillow (1080px max, calidad 65%) antes de subir al bucket.
- **Un usuario**: no hay roles ni permisos. El mecánico es el único usuario del sistema.

## Hoja de ruta
- **MVP** (actual): mecánico independiente, registro y gestión básica ← estamos aquí
- **Fase 1**: multi-tenant, roles, notificaciones WhatsApp, VHC digital, auditoría
- **Fase 2**: dashboard operativo, asignación de tareas, API de patentes
- **Fase 3**: módulo contable, reportes SII, dashboard financiero
