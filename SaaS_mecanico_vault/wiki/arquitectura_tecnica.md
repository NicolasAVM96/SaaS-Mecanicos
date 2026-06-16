---
tags: [wiki, tecnico]
updated: 2026-06-12
sources: [sources/documentacion_inicial.md]
---

# Arquitectura Técnica

→ Ver overview en [[overview]] | Ver tablas en [[base_de_datos]] | Ver fases en [[roadmap]]

---

## Stack actual (MVP)

| Capa | Tecnología | Razón de elección |
|---|---|---|
| Lenguaje | Python + uv | Versatilidad, velocidad de desarrollo, ecosistema maduro |
| Frontend/UI | Streamlit | Prototipado rápido sin JS/HTML/CSS; st.session_state nativo |
| Base de datos | Supabase (PostgreSQL) | BaaS con Auth, RLS y escalabilidad automática |
| Storage | Supabase Storage buckets | Almacenamiento seguro de evidencias fotográficas |
| Auth | Supabase Auth + cookies | Sesión persistente entre recargas |

---

## Módulos (`src/`)

```
src/
├── app.py                     # Orquestador: inicializa DB, sesión, tabs, despacha notificaciones
├── components/
│   ├── login.py               # UI de login; bloquea con st.stop() hasta autenticar
│   ├── record_form.py         # Tab "Nuevo Ingreso": campos del formulario, reset por form_k
│   └── history_view.py        # Tab "Historial": filtros, paginación, tarjetas de servicio
├── controllers/
│   ├── auth_controller.py     # Login/logout, cookies persistentes
│   └── record_controller.py   # Validación de inputs, construcción del payload, delega a database
├── data/
│   ├── database.py            # Cliente Supabase, guardar_servicio_relacional(), obtener_servicios()
│   └── cars.json              # Referencia marcas/modelos (31 marcas, 200+ modelos)
└── utils/
    ├── utils.py               # validar_patente() — regex formato patente chilena
    └── car_selector.py        # selectbox_marca() / selectbox_modelo() con @st.cache_data
```

---

## Flujo de datos principal

```
app.py inicializa
  → login.py bloquea hasta autenticar (auth_controller)
  → Tab "Nuevo Ingreso":
      record_form → record_controller.procesar_e_ingresar_servicio()
                 → database.guardar_servicio_relacional()
                 → bucket Supabase (fotos comprimidas)
  → Tab "Historial":
      history_view → database.obtener_servicios(filtros)
                  → JOINs: servicios ← vehiculos ← fotos_servicios
```

---

## Decisiones técnicas clave

| Patrón | Implementación |
|---|---|
| Imágenes | Comprimir siempre con Pillow antes de subir (máx 1080px, calidad 65%) — ver `database._comprimir_imagen()` |
| Patentes | Buscar en `vehiculos` antes de crear — reutilizar si existe, nunca duplicar |
| Reset formulario | Incrementar `st.session_state.form_k` para forzar re-render de todos los inputs |
| Notificaciones | `st.session_state.notificacion = {tipo, mensaje}` — se consume y limpia en `app.py` |
| Timezone | Timestamps de Supabase llegan en UTC → convertir a `America/Santiago` para mostrar |
| Roles | MVP: sin roles. Fase 1: tabla `perfiles` con roles `admin` / `mecanico` |

---

## Session state clave

| Clave | Tipo | Propósito |
|---|---|---|
| `autenticado` | bool | Estado de login |
| `taller_id` | str | User ID de Supabase Auth |
| `email` | str | Email del usuario |
| `notificacion` | dict | Toast `{tipo, mensaje}` |
| `procesando` | bool | Deshabilita botón submit durante guardado |
| `form_k` | int | Incrementar para resetear inputs del formulario |
| `filtro_*` | varios | Filtros de historial (patente, marca, modelo, etc.) |
| `limite_registros` | int | Paginación (inicia en 5, +5 por "Cargar más") |

---

## Migración futura (Horizonte)

Cuando Streamlit genere latencia por volumen de usuarios:
- **Backend**: migrar a FastAPI (API REST asíncrona)
- **Frontend**: migrar a Flet (Python sobre Flutter) → app móvil nativa Android/iOS
  - Offline-first para trabajar en fosas sin señal
  - API nativa de cámara
  - Notificaciones push en tiempo real
