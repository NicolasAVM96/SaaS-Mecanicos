---
tags: [wiki, producto]
updated: 2026-06-12
sources: [sources/documentacion_inicial.md, sources/estructura_base_datos.md]
---

# Roadmap de Desarrollo

Tres fases incrementales y acumulativas. Cada fase agrega tablas y funcionalidades sobre la anterior.

→ Ver tablas por fase en [[base_de_datos]] | Ver pricing por plan en [[modelo_negocio]]

---

## ✅ MVP — Estado actual

**Un mecánico, un taller, sin roles.**

- Login con sesión persistente (cookies)
- Registro de servicios: cliente + vehículo + diagnóstico + fotos
- Historial con filtros y paginación
- Tablas: `clientes → vehiculos → servicios → fotos_servicios`
- RLS activo en Supabase

→ Ver detalles en [[overview]]

---

## 🚀 Fase 1 — Multi-tenant, Roles y VHC Digital

**Alcance**: Soportar desde mecánico independiente hasta taller mediano con equipo.

**Nuevas funcionalidades:**

**Multi-tenant**
- Cada taller aislado por `taller_id` en todas las consultas
- Nueva tabla `talleres` como raíz del esquema

**Control de roles (Jefe / Mecánico)**
- `Jefe (admin)`: recibe solicitudes, autoriza envíos al cliente, ve dashboard
- `Mecánico (staff)`: registra ingresos, llena VHC, sube fotos — interfaz móvil optimizada
- Cada acción del mecánico genera una solicitud de revisión para el jefe

**Flujo de estados del vehículo**
`Registrado y en espera de aprobación` → `En proceso` → `Terminado y listo para retiro` → `Entregado`

**Notificaciones WhatsApp**
- El mecánico cambia el estado → el jefe recibe notificación
- El jefe autoriza → se genera URL `wa.me` con mensaje prearmado → el jefe envía al cliente
- **Solo el jefe autoriza el envío del VHC + presupuesto** — el resto son notificaciones internas

**VHC Digital**
- `vhc_plantillas`: formularios dinámicos configurables por taller (estructura en jsonb)
- `vhc_inspecciones`: resultados del chequeo, estados semáforo, daños estéticos con coordenadas

**Auditoría**
- `historial_ediciones`: trigger automático guarda estado anterior + timestamp + usuario en cada modificación

**Nuevas tablas**: `talleres`, `perfiles`, `vhc_plantillas`, `vhc_inspecciones`, `historial_ediciones`

---

## 📈 Fase 2 — Control Avanzado y Dashboard Vehicular

**Nuevas funcionalidades:**

- **Asignación dinámica de tareas**: el jefe distribuye vehículos o reparaciones a mecánicos específicos con seguimiento en tiempo real
- **Dashboard de rotación operativa**: métricas de flujo vehicular diario/semanal, cuellos de botella, ingresos proyectados
- **API de patentes chilenas**: al ingresar la patente, prellenar automáticamente marca, modelo, año, número de chasis y motor

**Nuevas tablas**: `asignaciones_tareas`

> ❓ Pendiente: investigar API de patentes disponible en Chile. El entrevistado menciona la app "Patentes Chile" como referencia. Ver [[propuesta_valor]].

---

## 💎 Fase 3 — Módulo Contable y Dashboard Financiero (Plan Premium)

**Nuevas funcionalidades:**

- **Módulo de egresos**: tabla `gastos` para repuestos, insumos, arriendos, sueldos
- **Métricas financieras en tiempo real**: flujo de caja, márgenes, ingresos netos
- **Reportes SII**: exportación formateada para declaraciones IVA (F29) y balances mensuales

**Nuevas tablas**: `gastos`, `ingresos_contables`

---

## 🔮 Horizonte futuro — Migración arquitectónica

Cuando Streamlit genere latencia:
- **Backend** → FastAPI (API REST asíncrona)
- **Frontend** → Flet (Python sobre Flutter): app móvil nativa iOS/Android
  - Offline-first (sin señal en fosa)
  - Cámara nativa
  - Notificaciones push
