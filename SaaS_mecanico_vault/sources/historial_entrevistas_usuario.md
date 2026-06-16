---
tags: [source, historial_entrevistas_usuario]
source_pdf: docs/user_history.pdf
---

# Historial Entrevistas Usuario

<!-- page 1 -->
Bloque 1: Entender el dolor actual (La Oportunidad)
El objetivo es descubrir qué procesos hacen hoy de forma manual, lenta o desordenada.
● "¿Cómo registran hoy el ingreso de un auto? (¿Usan una pizarra, un cuaderno,
WhatsApp, un Excel o papel carbón?)"
R: excel/planillas solo el jefe
● "¿Cuál es el mayor dolor de cabeza o el error más común que cometen al anotar los
datos de un vehículo?"
R: Se omiten defectos vehiculares como rayones (falta respaldo visual).
● "Cuando hay 3 o 4 autos desarmados al mismo tiempo, ¿cómo sabe cada mecánico
qué repuestos faltan o qué tarea sigue sin tener que preguntarle a cada rato al
resto?"
R: El jefe manda x wsp toda la info de lo que sabe del vehículo
Se pasan información entre compañeros por wsp o presencialmente.
Bloque 2: La relación y comunicación con el cliente (El Valor
Agregado)
Aquí descubrirás cómo tu SaaS puede ahorrarles horas de gestión y mejorar la confianza
con sus clientes.
● "¿Cómo le avisan hoy a un cliente que su auto ya está diagnosticado, cuánto va a
salir la reparación o que ya está listo para retiro?"
R: se le avisa todo via wsp al cliente. Después del diagnóstico se concidera el
presupiesto junto del trabajo + repuestos.
Para el retiro del vehiculo avisa el jefe del taller al cliente directo por wsp
Por otra parte se envia una OT al cliente cuando se ingresa el vehículo y tambien el
VHC al.momento del registro y luego se envia el VHC al finalizar con el auto ya
arreglado
VHC: (examen de sangre del vehiculo)
OT: este auto viene por esto, esto y esto, este es el diagnostico por lo cual lo hace el
jefe del taller
● "¿Qué pasa cuando desarman un motor, encuentran una falla extra que no estaba
planificada y necesitan la aprobación del cliente rápido?"
R: se envia directamente x wsp, lo manda el mismo jefe. Los mecanicos enciam
fotos y detalles al jefe, luego el jefe contacta al cliente
● "¿Los clientes les piden fotos o evidencias de los repuestos viejos que cambiaron?
¿Cómo se las envían actualmente?"

<!-- page 2 -->
R; No todos los clientes piden fotos, pero siempre se le mandan las fotos y full
transparencia con el cliente. Se envian x wsp
Mensajes personalizados del taller al cliente como reciclar los repiestos o piezas
sobrantes u otras cosas que hagan destacar el taller y diferenciarse del resto
Bloque 3: Flujo de trabajo interno y roles (Multi-tenant y Seguridad)
Esto te ayudará a validar técnicamente la estructura de jerarquía (Dueño vs. Mecánico Staff)
que conversamos antes.
● "En el taller, ¿todos hacen de todo (recibir el auto, meter mano, cobrar) o hay roles
claros (un jefe que recibe y los demás que reparan)?"
R: solo el jefe se mete al excel y los mecanicos hacen la mecanica. El contacto via
wsp de los clientes es solo con el jefe del taller.
● "¿Te ha pasado alguna vez que un mecánico anotó algo mal por error en una orden
y otro la borró o la modificó sin querer? ¿Cómo solucionan ese enredo?"
R: Problemas con el llenado del VHC y traspaso de información del vehiculo como
arreglos, cambios de focos, etc; entre personal
● "¿Al dueño del taller le interesaría ver un resumen a fin de mes de cuántos autos
reparó cada mecánico o cuánto dinero ingresó, o solo quieren la plataforma para
ordenar las fichas?"
R: Seria muy bueno un dashboard (cobro extra) para ver el historial financiero,
movimiento vehicular, repuestos, horas hombres trabajadas en general al mes en
relación al ingreso del mes.
Bloque 4: Validación del "Modo Edición y Permisos" (Lo que
acabamos de diseñar)
Aprovecha de testear la idea híbrida de auditoría que planificamos.
● "Si un mecánico se equivoca al anotar el kilometraje o la patente, ¿debería poder
corregirlo directo o crees que el jefe debería autorizarlo para evitar que se alteren
estos datos sensibles?"
R: Generalmente no se equivocan, no es tanto problema, ademas si encuentran una
discordancia, se arregla de inmediato.
● "¿Qué tan común es que el trabajo final que se le hace al auto sea muy diferente al
diagnóstico inicial con el que ingresó?"
R: Minimo 30% de las veces y se dice en el momento que es lo nuevo q se le
encontro y despues de ese diagnostica y se le entrega el precio final.
Para trabajos mas dificiles o caros se le solicita al cliente venir presencial para ver
presencial o envían documentación, videos, fotos en el caso que el cliente no pueda
ir.
Si el cliente cancela solo se cancela el diagnóstico o hasta el trabajo que se realizo.

<!-- page 3 -->
1. Sobre el contexto de uso (Ergonomía del software)
● "Cuando estás revisando un auto o metido en el motor, ¿con qué dispositivo andas
en la mano o tienes más cerca? ¿El celular, una tablet del taller, o tienes que ir a
mirar un computador que está en el escritorio de la recepción?"
R: Mecánicos: Generalmente celular. El VHC se llena desde el celular.
Jefe: Celular y PC
Por qué importa: Como Analista Programador, esto te dirá si debes optimizar la interfaz
pensando en el dedo con grasa usando un smartphone (botones grandes, inputs simples) o
si el foco principal debe ser la pantalla de escritorio.
2. Sobre el "historial" del auto vs. el "historial" del cliente
● "Si te ingresa un auto que nunca ha venido al taller, pero el dueño es un cliente
antiguo que tiene otros vehículos, ¿te interesa saber quién es el dueño y qué otros
autos te ha traído, o para ustedes el historial muere y nace con la patente del auto?"
R: quitaria confusión de cliente nuevo, además por llevar mas vehiculos puede tener
referencias o descuentos especiales, etc
Por qué importa: Esto nos dirá si en el futuro el modelo relacional de tu base de datos
necesita una tabla independiente de clientes vinculada a servicios, o si basta con seguir
indexando todo por la patente como lo tienes ahora.
3. Sobre la "Venta" del software (Tu validación comercial)
● "Si existiera una aplicación que te permitiera registrar el auto en 1 minuto, subir las
fotos de una, cambiar el estado del proceso y que le mande un WhatsApp
automático al cliente cuando el auto esté listo para que no te esté llamando cada dos
horas... ¿Crees que el dueño del taller pagaría una suscripción mensual por usarla?
¿Cuánto crees que sería un precio justo para el flujo de un taller como el tuyo?"
R: Si, claramente lo contrataría pero hay que ver bien los costos. Piensa que en
llenar un VHC se demora aprox 30min x vehiculo e ingresan 3 en promedio = 1 y ½
horas al dia = 4 dias al mes x hombre SOLO EN LLENAR EL VHC.
40 lucas vale un cambio de aceite considerando los insumos(6-15 a la semana)
80-140 lucas una mantención completa contemplando los insumos (2-4 al mes
aprox)
EXTRA:
Aplicacion: Patentes Chile, obtiene la información de todo el vehiculo sólo con la patente,
podría prellenar el VHC. No se ocupa toda la información. Podría extraerse información con
alguna API?