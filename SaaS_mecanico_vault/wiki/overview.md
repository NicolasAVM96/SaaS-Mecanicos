---
tags: [wiki, overview]
updated: 2026-06-12
sources: [sources/documentacion_inicial.md, sources/modelo_negocio.md]
---

# Overview del Proyecto

SaaS para talleres mecánicos chilenos. Digitaliza el flujo completo de un vehículo desde su ingreso hasta su entrega, reemplazando el trabajo en papel, Excel y WhatsApp.

**Estado actual**: MVP funcional — un usuario, un taller, sin roles.

Ver detalles en:
- [[propuesta_valor]] — por qué existe este producto
- [[modelo_negocio]] — pricing y estrategia comercial
- [[arquitectura_tecnica]] — stack y módulos
- [[base_de_datos]] — tablas actuales y planificadas
- [[roadmap]] — fases de desarrollo
- [[entrevistas_usuario]] — validación con usuario real
- [[vhc]] — concepto central del producto

---

## Dolores que resuelve

1. **Burocracia en papel (Efecto VHC)**: un mecánico gasta ~30 min por vehículo llenando el VHC. Con 3 vehículos/día → 4 días/mes perdidos solo en papeles. El SaaS lo reduce a ~3 min.
2. **Falta de respaldo visual**: sin fotos de defectos previos, el taller queda expuesto a disputas con clientes. El sistema obliga el registro fotográfico.
3. **Comunicación manual vía WhatsApp**: el jefe del taller coordina todo por WhatsApp (diagnósticos, presupuestos, estado del vehículo). El SaaS automatiza esas notificaciones.

---

## Stack actual (MVP)

| Capa | Tecnología |
|---|---|
| Lenguaje | Python + uv |
| Frontend | Streamlit |
| Base de datos | Supabase (PostgreSQL) |
| Storage | Supabase Storage buckets |
| Auth | Supabase Auth |

→ Ver detalles en [[arquitectura_tecnica]]

---

## Qué hace el MVP hoy

- Login con sesión persistente (cookies)
- **Tab "Nuevo Ingreso"**: registra cliente, vehículo (patente, marca, modelo, km, color), diagnóstico, trabajo y hasta 8 fotos de evidencia
- **Tab "Historial"**: filtros por patente, marca, modelo, diagnóstico, rango de fechas; paginación de 5 en 5
- Reutiliza vehículos existentes por patente (no crea duplicados)
- Comprime fotos antes de subir (máx 1080px, calidad 65%)

→ Base de datos: 4 tablas — `clientes → vehiculos → servicios → fotos_servicios`
