---
tags: [source, estructura_base_datos]
source_pdf: docs/DB_structure.pdf
---

# Estructura Base Datos

<!-- page 1 -->
Estructura de Tablas
FASE MVP:
1. Tabla: fotos_servicios (tabla de evidencia fotografica)
● id: bigint o uuid (Primary Key).
● servicio_id: uuid (Foreign Key ➡ servicios.id con borrado en cascada).
● url_foto: text.
● fecha_subida: timestamp (Por defecto now()).
2. Tabla: clientes (información del cliente)
● id: uuid (Primary Key).
● taller_id: uuid (Foreign Key ➡ talleres.id).
● nombre_completo: varchar(150).
● telefono: varchar(20).
● email: varchar(100) (Nullable).
3. Tabla: vehiculos (información del vehículo)
● id: uuid (Primary Key).
● cliente_id: uuid (Foreign Key ➡ clientes.id).
● patente: varchar(10) (Indexada de forma única por taller).
● marca, modelo, color: varchar.
● n_chasis, n_motor: varchar(50) (Nullable).
● ano: integer (Nullable).
● kilometraje: integer.
4. Tabla: servicios (información del servicio o trabajo que se realizará)
Representa el historial operativo de ingresos y las órdenes de trabajo. Aquí se enganchará
el VHC.
● id: uuid (Primary Key - Se recomienda estandarizar a uuid para acoplarse
nativamente con Supabase).
● vehiculo_id: uuid (Foreign Key ➡ vehiculos.id).
● diagnostico, trabajo_a_realizar: text.
● fecha_ingreso: timestamp (Por defecto now()).
● fecha_entrega: timestamp (Nullable).
🛠
FASE 1
(Esto junta la gestión relacional por talleres, la separación de clientes vs. autos, el control de
roles y el historial de auditoría automática desde el primer día).

<!-- page 2 -->
2.1 Modificación Tabla: clientes (información del cliente)
Se agregan las siguientes filas
● taller_id: uuid (Foreign Key ➡ talleres.id).
3.1 Modificación Tabla: vehículos (información del vehículo)
Se agregan las siguientes filas
● taller_id: uuid (Foreign Key ➡ talleres.id).
4.1 Modificación Tabla: servicios (información del servicio o trabajo que
se realizará)
Se agregan las siguientes filas
● taller_id: uuid (Foreign Key ➡ talleres.id).
● mecanico_id: uuid (Foreign Key ➡ perfiles.id).
● presupuesto_estimado: numeric(12,2).
● estado: varchar(30) (Valores: 'Ingresado', 'En Diagnostico', etc.).
● autorizado_por_jefe: boolean (Por defecto False).
5. Tabla: talleres
Es la tabla raíz del esquema multi-tenant. Cada taller que se registre en tu plataforma tendrá
una fila aquí.
● id: uuid (Primary Key, generado por defecto con gen_random_uuid()).
● nombre_taller: varchar(150) (Ej: "Taller Nico Pro").
● fecha_creacion: timestamp (Por defecto now()).
● limite_usuarios: integer (Por defecto 3).
6. Tabla: perfiles
Extiende la tabla nativa de autenticación de Supabase (auth.users).
● id: uuid (Primary Key, Foreign Key ➡ auth.users.id con borrado en cascada).
● taller_id: uuid (Foreign Key ➡ talleres.id).
● nombre: varchar(100).
● rol: varchar(20) (Check constraint: 'admin' o 'mecanico').
7. Tabla: vhc_plantillas
Almacena los diferentes formatos de formularios que cada jefe de taller decida crear o
importar mediante la IA.
● id: uuid (Primary Key, por defecto gen_random_uuid()).
● taller_id: uuid (Foreign Key ➡ talleres.id con borrado en cascada).

<!-- page 3 -->
● nombre_plantilla: varchar(100) (Ej: "Inspección Visual General", "Checklist de
Frenos").
● descripcion: text (Nullable).
● estructura: jsonb (Contiene el árbol dinámico de secciones, preguntas, tipos de
input y si son obligatorios).
● activa: boolean (Por defecto True. Permite desactivar plantillas viejas sin borrar el
historial de inspecciones).
● fecha_creacion: timestamp (Por defecto now()).
8. Tabla: vhc_inspecciones
Almacena los resultados del chequeo del auto. Se llena una sola vez por servicio o
recepción.
● id: uuid (Primary Key, por defecto gen_random_uuid()).
● taller_id: uuid (Foreign Key ➡ talleres.id con borrado en cascada para facilitar
políticas RLS).
● plantilla_id: uuid (Foreign Key ➡ vhc_plantillas.id con restricción SET NULL por si
se borra la plantilla base).
● servicio_id: uuid (Foreign Key ➡ servicios.id con borrado en cascada. Relación
1-a-1 o 1-a-Muchos con la OT).
● mecanico_id: uuid (Foreign Key ➡ perfiles.id, registra qué técnico hizo la inspección
en terreno).
● kilometraje_ingreso: integer (Congela el kilometraje exacto del auto al momento de
hacer el VHC).
● respuestas: jsonb (Diccionario de Python con los estados de los semáforos y
comentarios escritos o extraídos por la IA).
● danos_esteticos: jsonb (Por defecto '[]'::jsonb. Guarda las coordenadas o zonas
con rayones/abolladuras).
● estado: varchar(20) (Por defecto 'borrador', valores: 'borrador', 'completado').
● fecha_creacion: timestamp (Por defecto now()).
● fecha_actualizacion: timestamp (Por defecto now()).
9. Tabla: historial_ediciones (Auditoría)
● id: bigint o uuid (Primary Key).
● servicio_id: uuid (Foreign Key ➡ servicios.id).
● modificado_por: uuid (Foreign Key ➡ perfiles.id).
● fecha_modificacion: timestamp (Por defecto now()).
● datos_anteriores: jsonb.
🚀
FASE 2: Planificación de Tablas para las Futuras
Fases

<!-- page 4 -->
Fase 2: Control, Asignaciones y Flujo Vehicular
10. Tabla: asignaciones_tareas
Permite al jefe de taller distribuir la carga de trabajo diaria de forma modular.
● id: bigint (Primary Key).
● taller_id: uuid (Foreign Key ➡ talleres.id).
● servicio_id: bigint o uuid (Foreign Key ➡ servicios.id).
● mecanico_id: uuid (Foreign Key ➡ perfiles.id).
● descripcion_tarea: text (Ej: "Desarmar culata y sacar fotos de las válvulas").
● estado_tarea: varchar(20) ('Pendiente', 'En Proceso', 'Terminada').
11. Tabla: gastos
Captura de forma masiva las fugas de dinero y egresos operacionales del local.
● id: bigint (Primary Key).
● taller_id: uuid (Foreign Key ➡ talleres.id).
● registrado_por: uuid (Foreign Key ➡ perfiles.id).
● monto: numeric(12,2).
● categoria: varchar(50) (Valores: 'Repuestos', 'Insumos', 'Sueldos', 'Arriendo',
'Herramientas', 'Otros').
● descripcion: text (Ej: "Compra de empaquetaduras y aceite de motor 10W40").
● tipo_documento: varchar(30) ('Factura', 'Boleta', 'Voucher', 'Ninguno').
● folio_documento: varchar(50) (Nullable, para registrar el número de factura para el
SII).
● fecha_gasto: date.
12. Tabla: ingresos_contables
Cruza el cierre de los servicios con la facturación real del SII para el cálculo del IVA y
balance neto.
● id: bigint (Primary Key).
● taller_id: uuid (Foreign Key ➡ talleres.id).
● servicio_id: bigint o uuid (Foreign Key ➡ servicios.id).
● monto_neto: numeric(12,2).
● monto_iva: numeric(12,2) (Calculado automáticamente con el 19% si aplica).
● monto_total: numeric(12,2).
● tipo_documento_emitido: varchar(30) ('Boleta Electronica', 'Factura Electronica',
'Efectivo/Transferencia sin documento').
● folio_sii: varchar(50) (Identificador correlativo del documento tributario).
🚀
FASE 3: Planificación de Tablas para las Futuras
Fases
🎯 Conclusión del Diseño
Al separar las entidades clientes y vehiculos de la orden de servicios, logramos que tu base
de datos sea altamente eficiente.

<!-- page 5 -->
Cuando implementemos la consulta externa de la API de Patentes en la Fase 2, la función
de Python simplemente golpeará la API, traerá la información técnica y la guardará o
actualizará directamente en la tabla vehiculos de forma limpia, sin tener que alterar el
historial de servicios pasados.
¿Qué te parece este mapa de base de datos relacional para arrancar con el nuevo MVP
unificado, Nico? Si te convence, podemos escribir el script SQL para que lo ejecutes
directamente en el editor de Supabase y dejes las tablas creadas.