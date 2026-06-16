---
tags: [wiki, investigacion]
updated: 2026-06-12
sources: [sources/historial_entrevistas_usuario.md]
---

# Entrevistas de Usuario

Hallazgos de entrevista con dueño/operador de taller mecánico real (taller de 3-4 personas).

→ Ver cómo se tradujeron en producto: [[propuesta_valor]] | [[roadmap]] | [[vhc]]

---

## Operaciones actuales (antes del SaaS)

| Proceso | Cómo lo hacen hoy |
|---|---|
| Registro de vehículos | Excel/planillas — solo el jefe tiene acceso |
| Comunicación interna | WhatsApp entre mecánicos y jefe |
| Comunicación con cliente | Solo el jefe, todo por WhatsApp |
| VHC | Se llena desde el celular (~30 min/vehículo) |
| Evidencia fotográfica | Fotos por WhatsApp, siempre se envían al cliente |
| OT y VHC al cliente | Se envían al ingresar el vehículo y al finalizar |

---

## Dolores validados

1. **Falta de respaldo visual**: se omiten defectos previos como rayones → disputas potenciales
2. **Tiempo del VHC**: 30 min × 3 vehículos/día = 4 días al mes por persona
3. **Coordinación por WhatsApp**: el jefe es el cuello de botella de toda la comunicación

---

## Flujo de trabajo validado

```
Mecánico registra vehículo
  → llena VHC (celular, en la fosa)
  → sube fotos al jefe por WhatsApp
  → jefe diagnostica + presupuesta
  → jefe contacta al cliente por WhatsApp
  → si hay falla extra: mecánico → jefe → cliente (presencial o WhatsApp + fotos)
  → vehículo listo: jefe avisa al cliente por WhatsApp
```

---

## Validación de roles

- **Solo el jefe** usa el Excel y habla con los clientes
- **Los mecánicos** hacen la mecánica y se comunican internamente por WhatsApp
- El jefe quiere un dashboard financiero (validado como funcionalidad de cobro extra)

---

## Validación de precios

- Cambio de aceite ≈ $40.000 CLP (con insumos, 6-15/semana)
- Mantención completa ≈ $80.000–$140.000 CLP (2-4/mes)
- El entrevistado dijo que **sí pagaría** suscripción mensual si el software resuelve el dolor del VHC
- "Claramente lo contrataría pero hay que ver bien los costos"

---

## Hallazgos adicionales

- **Historial por cliente, no solo por patente**: si un cliente tiene múltiples vehículos, asociarlos le permite dar descuentos y referencias. Valida la tabla `clientes` separada de `vehiculos`.
- **30% de casos**: el trabajo final difiere del diagnóstico inicial — los cambios se comunican inmediatamente al cliente
- **API de patentes**: el entrevistado menciona la app "Patentes Chile" que prellenan info del vehículo solo con la patente → validaría automatizar este paso en [[roadmap]] Fase 2
- **Dispositivos**: mecánicos usan celular en fosa; jefe usa celular y PC → la app debe ser primero mobile

---

## Citas literales del entrevistado

> *"En llenar un VHC se demora aprox 30min x vehiculo e ingresan 3 en promedio = 1 y ½ horas al dia = 4 dias al mes x hombre SOLO EN LLENAR EL VHC"*

> *"Solo el jefe se mete al excel y los mecanicos hacen la mecanica"*

> *"Seria muy bueno un dashboard (cobro extra) para ver el historial financiero, movimiento vehicular, repuestos, horas hombres trabajadas en general al mes"*
