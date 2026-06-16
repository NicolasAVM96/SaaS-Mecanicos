---
tags: [source, documentacion_inicial]
source_pdf: docs/initial_documentation.pdf
---

# Documentacion Inicial

<!-- page 1 -->
📑
DOCUMENTACIÓN GENERAL DEL
PROYECTO: SAAS AUTOMOTRIZ
1. Definición del Proyecto y Propuesta de Valor
Este proyecto consiste en un SaaS (Software as a Service) en la nube diseñado
específicamente para optimizar la gestión operativa, comercial y financiera de talleres
mecánicos, abarcando desde mecánicos independientes hasta talleres medianos con
equipos de trabajo.
El sistema digitaliza el flujo completo de un vehículo desde su ingreso hasta su entrega,
resolviendo tres dolores críticos de la industria automotriz:
1. Pérdida de tiempo en burocracia (Efecto VHC): Un taller promedio gasta valioso
tiempo hombre rellenando el Vehicle Health Check (VHC) y la Orden de Trabajo (OT)
en papel o planillas rígidas. Este SaaS reduce ese tiempo drásticamente mediante
un flujo optimizado para dispositivos móviles.
2. Falta de respaldo legal y visual: La omisión de registro de defectos previos (como
rayones o abolladuras) genera disputas costosas con los clientes. El sistema mitiga
esto integrando una galería fotográfica obligatoria de evidencias vinculada
directamente a la ficha del vehículo.
3. Fricción en la comunicación: Centraliza el envío de actualizaciones de estado,
presupuestos y evidencias extras directamente al cliente a través de canales
digitales automatizados (WhatsApp), evitando llamadas constantes que interrumpen
el trabajo técnico.
2. Stack Tecnológico Actual (Fase MVP)
Para el desarrollo del Producto Mínimo Viable (MVP) se seleccionó un ecosistema de
herramientas que prioriza la velocidad de despliegue, el bajo costo de infraestructura y la
robustez en el manejo de datos:
● Lenguaje de Programación: Python + uv. Elegido por su versatilidad, velocidad de
desarrollo y madurez en el ecosistema de software e integraciones.
● Framework de Frontend/UI: Streamlit. Permite prototipar interfaces de usuario
interactivas directamente en Python sin requerir un equipo dedicado a
JavaScript/HTML/CSS. Facilita la implementación de lógica del lado del servidor y
estados de sesión (st.session_state).
● Base de Datos (Backend as a Service): Supabase (PostgreSQL). Proporciona
una base de datos relacional potente con capacidades nativas de autenticación de
usuarios, políticas de seguridad a nivel de fila (RLS) y escalabilidad automática.
● Almacenamiento de Archivos (Storage): Supabase Storage buckets. Utilizado
para el almacenamiento seguro y eficiente de las imágenes de alta resolución
capturadas como evidencia de los servicios automotrices.

<!-- page 2 -->
3. Mapa de Ruta de Desarrollo (Roadmap Técnico)
El desarrollo del software está estructurado en tres bloques incrementales y acumulativos.
Esto garantiza una validación progresiva en el mercado utilizando una base arquitectónica
robusta y escalable desde el primer día.
Qué hace el MVP hoy
Un sistema de gestión para un mecánico independiente, accesible desde el celular, con
estas funciones:
Login:
Autenticación con Supabase Auth. La sesión persiste entre recargas de página mediante
cookies del navegador.
Tab 1 — Nuevo Ingreso
● Registra un servicio completo en un formulario:
○ Cliente: nombre y teléfono
○ Vehículo: patente, kilometraje, marca (selectbox), modelo (selectbox
dinámico), color
○ Servicio: diagnóstico, trabajo a realizar, fotos de evidencia (máx. 8)
○ Reglas aplicadas automáticamente:
○ Si la patente ya existe en la base de datos, reutiliza ese vehículo — no crea
duplicados
○ Las fotos se comprimen antes de subir (máx. 1080px, calidad 65%)
Tab 2 — Historial
● Busca y filtra todos los servicios registrados:
○ Filtros por patente, marca, modelo, diagnóstico, trabajo y rango de fechas
○ Muestra los últimos 5 registros por defecto, con botón "Cargar más" (+5 por
click)
○ Cada resultado se expande mostrando datos del vehículo, diagnóstico,
trabajo y galería de fotos
Base de datos: 4 tablas relacionales — clientes → vehiculos → servicios → fotos_servicios
— con RLS activo en Supabase.
Usuario único: no hay roles ni multi-tenant. El mecánico es el único usuario del sistema.

<!-- page 3 -->
🚀 Fase 1: Arquitectura Multi-tenant y Gestión de Talleres
Alcance: Diseñado de forma nativa para soportar desde un mecánico independiente
(taller de un solo usuario) hasta talleres medianos con equipos de trabajo.
Aislamiento de Datos: Toda consulta en la base de datos se filtra estrictamente
mediante un taller_id único. Esto garantiza que la información de cada negocio esté
completamente aislada de la competencia.
Automatización de notificaciones: Cada vez que un mecánico registra un
vehículo, modifica un diagnóstico/trabajo o el vehículo está listo para el retiro porque
el trabajo se completó, el mecánico le cambia el estado del vehiculo en la aplicacion
([“Registrado y en espera de aprobación de presupuesto”,”En proceso”,””Terminado
y listo para el retiro, “”Entregado”] el sistema le notifica al jefe en cada una de estos
estados; este valida la información que genera el sistema y autoriza/envia la
notificación al cliente para que el cliente actúe de acuerdo a lo notificado (El jefe
SOLO AUTORIZARA el envio del VHC + el presupuesto, todas las demas solo seran
notificaciones)
TIP de código:
Utiliza Deep Links de WhatsApp (wa.me). Cuando el jefe aprueba un presupuesto
en Streamlit, el sistema simplemente debe generar una URL dinámica (ej:
https://wa.me/56912345678?text=Hola%20tu%20auto...) incrustada en un
botón que diga "Enviar al Cliente". Al hacer clic, se abrirá el WhatsApp web o la app
nativa del jefe con el mensaje prearmado. Es 100% seguro, gratuito y no requiere
infraestructura extra.
Control de Roles y Jerarquía: Implementación de una tabla intermedia de perfiles
vinculada a auth.users de Supabase. Se introducen dos roles jerárquicos clave:
Admin (Jefe de Taller): Panel de administración para revisar información
técnica, gestionar el equipo y autorizar flujos informativos. En este caso
tendrá el poder de aceptar peticiones de registro de vehiculos,
modificaciones importantes y enviar las notificaciones al cliente (previamente
revisadas por el jefe)
Mecánico (Staff): Interfaz móvil optimizada y simplificada. Permite registrar
nuevos ingresos vehiculares, llenar el VHC digital al lado del motor y capturar
fotografías de evidencia en el Storage. Cada ingreso, modificación de ficha o
término de servicio genera una solicitud automática de revisión enviada al
jefe.
Estructura de Datos Normalizada: Desacoplamiento relacional de entidades. El
formulario básico del MVP ahora separa de forma estricta:
Servicios (OT / VHC): Gestión del flujo operativo por estados ('Ingresado',
'En Diagnostico', 'Esperando Autorizacion', 'En Reparacion', 'Listo para
Retiro', 'Entregado') y actualizar según VHC utilizada por la empresa.
Implementar nuevas tablas: vhc_plantillas y vhc_inspecciones

<!-- page 4 -->
Modo Edición Múltiple: Capacidad integrada para que el personal autorizado
modifique registros de vehículos e historiales de servicio de forma indefinida
directamente desde la interfaz.
Tabla de Auditoría (historial_ediciones): Implementación de un Trigger automático
a nivel de base de datos en PostgreSQL (Supabase). Cada vez que un mecánico o
administrador altere un registro operativo, el estado anterior de los datos se respalda
automáticamente en un objeto JSONB junto con la fecha, hora y el ID del usuario
responsable, asegurando una total transparencia e integridad de los datos en
terreno.
📈 Fase 2: Control de Cambios Avanzado, Automatización y
Dashboard de Flujo Vehicular
● Alcance: Robustez de datos, optimización en tiempos de ingreso y herramientas
avanzadas de supervisión.
● Características:
Asignación Dinámica de Tareas: Herramienta para el Jefe de Taller que
permite delegar vehículos o reparaciones específicas a mecánicos del
personal, realizando un seguimiento del estado de cada tarea en tiempo real.
Dashboard de Rotación Operativa: Panel visual para el administrador que
muestra métricas de flujo vehicular diarios/semanales, cuellos de botella en
las fosas de trabajo y los ingresos totales proyectados en base a los
presupuestos aprobados.
Integración de API Externa de Patentes: Conexión con servicios de
consulta de patentes automotrices en Chile. Al ingresar la patente del
vehículo, el sistema prellenará automáticamente campos avanzados como
Marca, Modelo, Año de fabricación, Número de Chasis y Número de Motor,
reduciendo el error humano y acelerando el ingreso móvil.
💎 Fase 3: Módulo Contable y Dashboard Financiero (Módulo
Premium)
● Alcance: Gestión administrativa y tributaria total del negocio para el dueño del taller.
● Características:
Módulo de Egresos y Costos: Creación de la tabla de gastos para registrar
de forma detallada compras de repuestos, insumos de taller, arriendos de
infraestructura y pago de sueldos de mecánicos.
Métricas Financieras en Tiempo Real: Integración de componentes
visuales interactivos (st.metric y st.bar_chart) en la interfaz del administrador
para calcular de forma automatizada el flujo de caja, los márgenes de
ganancia e ingresos netos.
Generación de Reportes de Cumplimiento SII: Exportación de reportes
contables y libros de compra/venta formateados estrictamente según las
exigencias del Servicio de Impuestos Internos (SII) de Chile. Diseñado para
simplificar drásticamente las declaraciones mensuales de IVA (F29) y los
balances mensuales del negocio.

<!-- page 5 -->
🔮 Horizonte de Escalabilidad Futura (Migración Arquitectónica)
Cuando el volumen de usuarios simultáneos en terreno genere latencia o degrade el
rendimiento del renderizado de Streamlit, el sistema transicionará hacia un desacoplamiento
absoluto de sus capas:
● Backend: FastAPI. Migración hacia una API REST asíncrona en Python de alto
rendimiento, optimizada para procesar miles de peticiones simultáneas de subida de
imágenes a Storage y escrituras concurrentes en la base de datos relacional.
● Frontend: Flet (Python sobre Flutter). Compilación de la plataforma como una
aplicación móvil nativa para sistemas Android e iOS. Esto ofrecerá una experiencia
fluida e industrial en terreno : funcionamiento Offline-first para trabajar dentro de
fosas sin señal, uso directo de la API nativa de la cámara para evidencias rápidas y
envío de notificaciones push en tiempo real.