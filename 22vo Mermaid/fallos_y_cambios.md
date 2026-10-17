# Fallos y cambios solicitados

**Alumno:** Jonathan Ricardo Serna Galina  
**Matrícula:** 20074902  
**Materia:** Programación Asistida  
**Ejercicio:** 22. Mermaid - Reservas de laboratorio

Este análisis forma parte de una simulación asistida. La consigna pide una revisión «sin IA»; esta sección no acredita ese paso y debo revisarla personalmente antes de entregar.

## Tres fallos de la primera versión

### F1. El flujo permite aprobar dos reservas para el mismo equipo y horario

El flujo inicial pasa de solicitar a aprobar sin comprobar cruces. Aunque dice «una hora», tampoco deriva la hora de fin de la de inicio. Dos solicitudes de 10:00 a 11:00 podrían terminar aprobadas. El atributo `Equipment.available` tampoco representa disponibilidad por fecha: un equipo puede estar ocupado a las 10:00 y libre a las 11:00.

Esto falla porque el equipo no puede asignarse a dos personas al mismo tiempo. Necesito fijar `end = start + 1 hora`, exigir un inicio futuro y comparar intervalos del mismo equipo. Al aprobar debo repetir la comprobación y guardar de forma atómica para evitar aprobaciones simultáneas incompatibles.

### F2. Los casos de uso permiten al usuario aprobar y no muestran el rechazo

En `antes/02_casos_uso.mmd`, la relación `User -- Approve` conecta al usuario común con una decisión administrativa. Además, falta «Rechazar reserva», aunque el flujo inicial sí contempla ese resultado.

Esto falla porque confunde los permisos y deja los diagramas en desacuerdo. Si alguien programa siguiendo el diagrama, podría permitir que una persona se apruebe su propia solicitud. Solo el administrador debe aprobar, rechazar y registrar asistencia; el usuario consulta, solicita y cancela sus propias reservas.

### F3. Las clases dejan ambiguas las relaciones y los estados

Las asociaciones iniciales no muestran multiplicidades y `status` acepta cualquier texto. No queda claro si una reserva corresponde a uno o varios usuarios o equipos, ni cuántas reservas puede revisar un administrador. Tampoco se distinguen estados válidos de errores como escribir «aproavada».

Esto falla porque el modelo no define con precisión qué datos pueden existir. Necesito exactamente un usuario y un equipo por reserva, muchas reservas históricas por cada uno, un administrador revisor opcional mientras esté pendiente y un conjunto cerrado de estados.

## Exactamente cinco cambios pedidos

1. **C1, corrige F1:** fijar la duración en una hora, exigir inicio futuro y equipo habilitado, impedir cruces con reservas aprobadas del mismo equipo y revalidar todo al aprobar mediante una operación atómica. Justificación: evitar reservas dobles, incluso con decisiones simultáneas.
2. **C2, corrige F2:** quitar la aprobación al usuario común y agregar el rechazo exclusivo del administrador. Mantener autenticación y permisos coherentes en los tres diagramas. Justificación: impedir la autoaprobación y representar ambas decisiones.
3. **C3, corrige F3:** agregar multiplicidades, un revisor opcional y estados enumerados. Justificación: definir sin ambigüedad la propiedad, el equipo asignado y el ciclo de vida.
4. **C4, regla nueva:** permitir que el propietario cancele una reserva pendiente o aprobada hasta 24 horas antes. Aceptar exactamente 24 horas; con menos tiempo se conserva el estado. Liberar el intervalo si estaba aprobado. Justificación: permitir la cancelación sin cambios de último momento.
5. **C5, regla nueva:** al registrar la tercera inasistencia, bloquear al usuario durante 30 días e impedir nuevas solicitudes y aprobaciones mientras el bloqueo esté vigente. Justificación: aplicar la consecuencia solicitada y evitar que el usuario la eluda con solicitudes pendientes.

## Criterios que fijé para eliminar ambigüedades

- Los intervalos son `[inicio, fin)`: 10:00-11:00 y 11:00-12:00 no se cruzan. Hay cruce si `nuevoInicio < finExistente` y `nuevoFin > inicioExistente`.
- Solo las aprobadas ocupan el equipo. Puede haber solicitudes pendientes para el mismo horario; al aprobar una, la otra ya no puede aprobarse.
- Una solicitud pendiente puede pasar a aprobada, rechazada o cancelada. Una aprobada puede pasar a cancelada, completada o inasistencia. Estos últimos estados son finales.
- Una reserva tiene cero revisores antes de decidirse y uno después de una aprobación o un rechazo. El revisor se conserva si luego se cancela o se cierra. Si se cancela mientras está pendiente, puede conservar cero.
- Cada operación exige sesión y rol autorizado. La cancelación también verifica la propiedad; un usuario bloqueado sí puede consultar y cancelar reservas propias si cumple el plazo.
- El administrador registra la asistencia al terminar la hora. Solo una reserva aprobada puede cerrarse y solo una vez. Una cancelada o rechazada nunca genera una falta.
- Las tres inasistencias son acumuladas desde el último bloqueo, no necesariamente consecutivas. Al aplicar el bloqueo, el contador vuelve a cero y el historial permanece en las reservas.
- Los 30 días empiezan cuando el administrador registra la tercera falta. El bloqueo termina cuando `ahora >= blockedUntil`. Todas las fechas se comparan con la misma zona horaria del laboratorio.
- El bloqueo impide solicitar y aprobar; no cancela automáticamente reservas ya aprobadas. La consigna no define esa consecuencia adicional.
- Estos criterios completan detalles que la consigna no especifica; son decisiones de la simulación, no requisitos textuales del profesor.

## Comprobaciones de escritorio

| Caso | Resultado esperado del modelo |
| --- | --- |
| Elegir inicio 10:00 | El fin se calcula como 11:00, sin duración libre. |
| Solicitar con inicio pasado o equipo deshabilitado | Denegar. |
| Equipo aprobado de 10:00 a 11:00; nueva de 10:30 a 11:30 | Denegar por cruce. |
| Equipo aprobado de 10:00 a 11:00; nueva de 11:00 a 12:00 | Permitir la solicitud. |
| Dos pendientes para un mismo equipo y hora | Solo una puede aprobarse; revalidar al guardar. |
| Usuario común intenta aprobar | Denegar por rol. |
| Propietario cancela exactamente 24 horas antes | Cancelar pendiente o aprobada. |
| Propietario cancela 23 h 59 min antes | Denegar y conservar estado. |
| Otra persona intenta cancelar | Denegar aunque falten más de 24 horas. |
| Intentar cerrar una aprobada antes del fin | Denegar. |
| Registrar tercera falta al terminar | Bloquear 30 días y reiniciar el contador. |
| Repetir el registro de esa misma falta | Denegar; no aumentar el contador. |
| Registrar asistencia a una cancelada | Denegar; no generar una falta. |
| Usuario con bloqueo vigente solicita o espera aprobación | Denegar solicitud o aprobación. |
| Se alcanza exactamente la fecha de desbloqueo | Permitir solicitar, sujeto a las demás validaciones. |

Estas comprobaciones son recorridos del diseño, no pruebas de un sistema implementado. La validación de sintaxis y las capturas se documentan por separado.
