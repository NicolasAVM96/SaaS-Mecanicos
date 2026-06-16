---
tags: [wiki, tecnico]
updated: 2026-06-16
sources: [sources/estructura_base_datos.md]
---

# Base de Datos

Esquema PostgreSQL en Supabase. Organizado en fases de implementación.

→ Ver stack en [[arquitectura_tecnica]] | Ver fases en [[roadmap]]

---

## Fase MVP — Tablas actuales

### `talleres` (tabla raíz multi-tenant) ✅ implementada
| Campo | Tipo | Notas |
|---|---|---|
| id | uuid | PK, gen_random_uuid() |
| nombre_taller | varchar(150) | |
| fecha_creacion | timestamp | default now() |
| limite_usuarios | integer | default 3 |

### `perfiles` (extiende auth.users) ✅ implementada
| Campo | Tipo | Notas |
|---|---|---|
| id | uuid | PK, FK → auth.users.id (cascade) |
| taller_id | uuid | FK → talleres.id |
| nombre | varchar(100) | |
| rol | varchar(20) | Check: 'admin' o 'mecanico' |

> Por ahora todos los usuarios creados manualmente tienen `rol = 'admin'` y son dueños de su propio taller. El rol `mecanico` se activará en Fase 1.

### `fotos_servicios`
Evidencia fotográfica vinculada a un servicio.
| Campo | Tipo | Notas |
|---|---|---|
| id | bigint / uuid | PK |
| servicio_id | uuid | FK → servicios.id (cascade delete) |
| url_foto | text | URL en Supabase Storage |
| fecha_subida | timestamp | default now() |

### `clientes`
| Campo | Tipo | Notas |
|---|---|---|
| id | uuid | PK |
| taller_id | uuid | FK → talleres.id NOT NULL ✅ |
| nombre_completo | varchar(150) | |
| telefono | varchar(20) | |
| email | varchar(100) | Nullable |

### `vehiculos`
| Campo | Tipo | Notas |
|---|---|---|
| id | uuid | PK |
| cliente_id | uuid | FK → clientes.id |
| taller_id | uuid | FK → talleres.id NOT NULL ✅ |
| patente | varchar(10) | Índice único compuesto `(patente, taller_id)` ✅ |
| marca, modelo, color | varchar | |
| n_chasis, n_motor | varchar(50) | Nullable |
| ano | integer | Nullable |
| kilometraje | integer | |

> ⚠️ La patente es única POR taller — dos talleres distintos pueden tener el mismo vehículo. La lógica de deduplicación está en `database.guardar_servicio_relacional()`.

### `servicios`
Historial operativo de ingresos y órdenes de trabajo (OT). Aquí se engancha el [[vhc]].
| Campo | Tipo | Notas |
|---|---|---|
| id | uuid | PK |
| vehiculo_id | uuid | FK → vehiculos.id |
| taller_id | uuid | FK → talleres.id NOT NULL ✅ |
| diagnostico | text | |
| trabajo_a_realizar | text | |
| fecha_ingreso | timestamp | default now() |
| fecha_entrega | timestamp | Nullable |

### RLS multi-tenant ✅ implementado
Todas las tablas operativas filtran por `taller_id = auth_taller_id()`.
- `public.auth_taller_id()` — función helper `SECURITY DEFINER` que retorna el `taller_id` del usuario autenticado leyendo `perfiles`
- `fotos_servicios` se aísla via subquery a `servicios` (no necesita `taller_id` propio)

---

## Fase 1 — Nuevas tablas

### `vhc_plantillas`
Formularios dinámicos de inspección definidos por cada taller.
| Campo | Tipo | Notas |
|---|---|---|
| id | uuid | PK |
| taller_id | uuid | FK → talleres.id (cascade) |
| nombre_plantilla | varchar(100) | Ej: "Inspección Visual General" |
| descripcion | text | Nullable |
| estructura | jsonb | Árbol dinámico de secciones, preguntas, tipos de input |
| activa | boolean | default True — permite desactivar sin borrar historial |
| fecha_creacion | timestamp | default now() |

### `vhc_inspecciones`
Resultados del chequeo por vehículo/servicio.
| Campo | Tipo | Notas |
|---|---|---|
| id | uuid | PK |
| taller_id | uuid | FK → talleres.id (cascade) |
| plantilla_id | uuid | FK → vhc_plantillas.id (SET NULL si se borra plantilla) |
| servicio_id | uuid | FK → servicios.id (cascade) |
| mecanico_id | uuid | FK → perfiles.id |
| kilometraje_ingreso | integer | Congela el km exacto al momento del VHC |
| respuestas | jsonb | Estados de semáforos y comentarios |
| danos_esteticos | jsonb | default '[]' — coordenadas de rayones/abolladuras |
| estado | varchar(20) | default 'borrador'; valores: 'borrador', 'completado' |

### `historial_ediciones` (auditoría)
Trigger automático en PostgreSQL — cada modificación genera una fila.
| Campo | Tipo | Notas |
|---|---|---|
| id | bigint / uuid | PK |
| servicio_id | uuid | FK → servicios.id |
| modificado_por | uuid | FK → perfiles.id |
| fecha_modificacion | timestamp | default now() |
| datos_anteriores | jsonb | Estado previo del registro |

### Modificaciones a tablas existentes (Fase 1)
- ~~`clientes`, `vehiculos`, `servicios` agregan `taller_id` (FK → talleres.id)~~ → **ya implementado en MVP**
- `servicios` agrega: `mecanico_id`, `presupuesto_estimado`, `estado`, `autorizado_por_jefe`

---

## Fase 2 — Tablas planificadas

### `asignaciones_tareas`
Distribución de carga de trabajo por mecánico.
- Campos clave: `taller_id`, `servicio_id`, `mecanico_id`, `descripcion_tarea`, `estado_tarea`

### `gastos`
Egresos operacionales del taller.
- Campos clave: `monto`, `categoria` (Repuestos/Insumos/Sueldos/Arriendo/Herramientas/Otros), `tipo_documento`, `folio_documento`

### `ingresos_contables`
Facturación real para el SII.
- Campos clave: `monto_neto`, `monto_iva` (19%), `monto_total`, `tipo_documento_emitido`, `folio_sii`

---

## Relaciones clave

```
talleres
  └── perfiles (auth.users)
  └── clientes
        └── vehiculos
              └── servicios
                    └── fotos_servicios
                    └── vhc_inspecciones
                          └── vhc_plantillas
                    └── historial_ediciones
                    └── asignaciones_tareas (Fase 2)
  └── gastos (Fase 2)
  └── ingresos_contables (Fase 2)
```
