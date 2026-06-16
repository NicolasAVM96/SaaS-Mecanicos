---
tags: [wiki, concepto, dominio]
updated: 2026-06-12
sources: [sources/VHC_inspeccion_vehicular.md, sources/documentacion_inicial.md, sources/historial_entrevistas_usuario.md]
---

# VHC — Vehicle Health Check (Hoja de Inspección Visual)

El VHC es el documento central del negocio. Es el "examen de sangre del vehículo" (término del entrevistado). Se llena al ingreso del vehículo y al finalizar el trabajo.

→ Ver tablas relacionadas en [[base_de_datos]] | Ver impacto en tiempo en [[propuesta_valor]] | Ver implementación digital en [[roadmap]]

---

## ¿Qué es?

Formulario que registra el estado completo del vehículo al ingresar al taller:
- Estado de luces, vidrios, llantas, frenos, fluidos, correas, batería, escape, dirección, suspensión
- Medidas de neumáticos (marca, medida, profundidad del dibujo en mm por posición)
- Datos del cliente: nombre, OT, fecha, patente, VIN, kilometraje actual
- Observaciones y trabajos a realizar por área
- Inspector que realizó el chequeo

---

## Ejemplo real (VHC del 13/5/2026)

**Vehículo**: Patente HPHX11 | VIN 9BGKT69T0HG122532 | KM: 95.447
**Cliente**: Francisca Cecilia González Saavedra | OT: 2898

| Área | Estado | Observación |
|---|---|---|
| Luces obligatorias | ✅ OK | |
| Llantas / Neumáticos | ⚠️ Atención | Objeto incrustado neum. tras. izq / Neum. del. der. vencido |
| Estado correas | 🔴 Atención | Reemplazar |
| Dirección y suspensión delantera | ⚠️ Obs | Leve holguras en bandejas |
| Dirección y suspensión trasera | ⚠️ Obs | Leve humedad en amortiguador derecho |
| Frenos traseros | ✅ OK | Tambores con rebaba |

**Neumáticos**:
| Posición | Marca | Medida | Ext | Med | Int |
|---|---|---|---|---|---|
| Del. Izq. | Ovation | 185/65 R15 | 6mm | 6mm | 6mm |
| Del. Der. | Ovation | 185/65 R15 | 6mm | 6mm | 6mm |
| Tras. Izq. | Ovation | 185/65 R15 | 5mm | 6mm | 6mm |
| Tras. Der. | Westlake | 185/65 R15 | 2mm ⚠️ | 3mm ⚠️ | 2mm ⚠️ |

---

## Problema actual (sin SaaS)

- Se llena **en papel** desde el celular
- Tarda ~30 min por vehículo
- Con 3 vehículos/día → **4 días al mes por mecánico** en puro papeleo
- Se omiten defectos a veces → disputas con clientes

---

## Implementación digital (Fase 1)

La tabla `vhc_plantillas` almacena el formulario de forma dinámica (estructura en `jsonb`) para que cada taller pueda personalizar sus secciones y preguntas. La tabla `vhc_inspecciones` almacena los resultados por servicio.

**Flujo digital:**
1. Mecánico abre VHC en el celular desde la fosa
2. Marca estados (OK / En observación / Atención) por área
3. Escribe observaciones
4. Registra medidas de neumáticos
5. Guarda → el jefe recibe notificación → decide qué enviar al cliente

---

## Relación con OT

- **VHC**: estado físico del vehículo al ingresar ("examen de sangre")
- **OT (Orden de Trabajo)**: qué se va a hacer, por qué, diagnóstico, presupuesto

Según el entrevistado:
> *"OT: este auto viene por esto, esto y esto, este es el diagnostico — lo hace el jefe del taller"*

Ambos documentos se envían al cliente al ingresar el vehículo y al finalizar.

---

## Potencial: prellenado con API de patentes

Al ingresar la patente, prellenar automáticamente marca, modelo, año, chasis y motor con una API externa (ej: app "Patentes Chile"). Planificado para [[roadmap]] Fase 2.
