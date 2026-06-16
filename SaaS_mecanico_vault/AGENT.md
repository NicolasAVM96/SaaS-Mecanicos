# AGENT.md — Wiki del Proyecto SaaS Mecánico

Este archivo es el **schema** del agente wiki. Define cómo está organizado el vault, las convenciones de escritura, y qué hacer en cada operación.

---

## Estructura del vault

```
SaaS_mecanico_vault/
├── AGENT.md          ← este archivo (schema del agente)
├── index.md          ← índice de todas las páginas wiki (actualizar siempre)
├── log.md            ← log cronológico append-only
├── wiki/             ← páginas sintetizadas por el agente
│   ├── overview.md
│   ├── propuesta_valor.md
│   ├── modelo_negocio.md
│   ├── arquitectura_tecnica.md
│   ├── base_de_datos.md
│   ├── roadmap.md
│   ├── entrevistas_usuario.md
│   └── vhc.md
└── sources/          ← fuentes convertidas desde PDF (solo lectura)
    ├── modelo_negocio.md
    ├── estructura_base_datos.md
    ├── documentacion_inicial.md
    ├── historial_entrevistas_usuario.md
    └── VHC_inspeccion_vehicular.md
```

---

## Capas

- **`sources/`** — Inmutables. Conversión directa de los PDFs originales. El agente **lee** pero **nunca modifica** estos archivos.
- **`wiki/`** — El agente **escribe y mantiene** estas páginas. Son síntesis, no copias.
- **`index.md`** — El agente actualiza esto en cada ingestión o cambio relevante.
- **`log.md`** — El agente **solo agrega** entradas al final. Nunca edita entradas anteriores.

---

## Convenciones de páginas wiki

Cada página wiki sigue este frontmatter YAML:

```yaml
---
tags: [wiki, <categoría>]
updated: YYYY-MM-DD
sources: [sources/archivo.md, sources/otro.md]
---
```

### Tipos de páginas
- **Conceptos**: entidades del dominio (VHC, OT, patente, taller, mecánico)
- **Síntesis**: análisis cross-documento (modelo de negocio, arquitectura, roadmap)
- **Investigación**: hallazgos de entrevistas de usuario

### Links internos
Usar siempre `[[nombre_de_pagina]]` para referenciar otras páginas del vault.

---

## Operaciones

### Ingerir nueva fuente
1. Convertir PDF a markdown → guardar en `sources/`
2. Leer la fuente, discutir hallazgos clave
3. Escribir o actualizar páginas `wiki/` afectadas
4. Actualizar `index.md`
5. Agregar entrada a `log.md` con formato: `## [YYYY-MM-DD] ingest | Título`

### Responder consulta
1. Leer `index.md` para identificar páginas relevantes
2. Leer las páginas pertinentes de `wiki/`
3. Sintetizar respuesta con citas a las páginas (`[[pagina]]`)
4. Si la respuesta es valiosa, archivarla como nueva página wiki
5. Agregar entrada a `log.md`: `## [YYYY-MM-DD] query | Pregunta resumida`

### Lint / health-check
Buscar:
- Páginas wiki sin links entrantes (huérfanas)
- Contradicciones entre páginas
- Conceptos mencionados sin página propia
- Fuentes ingresadas pero no integradas al wiki

---

## Reglas del agente

1. **Nunca modificar** archivos en `sources/`
2. **Siempre actualizar** `index.md` al crear o modificar una página wiki
3. **Siempre agregar** entrada al `log.md` al finalizar una operación
4. Los links usan doble corchete: `[[nombre_sin_extension]]`
5. Las páginas wiki son síntesis, no copias — extraer lo esencial
6. Señalar contradicciones explícitamente con `> ⚠️ Contradicción: ...`
7. Señalar lagunas de información con `> ❓ Pendiente: ...`
