# Conversación con la IA

**Ejercicio 22. Mermaid - Reservas de laboratorio**  
**Alumno:** Jonathan Ricardo Serna Galina, 20074902  
**Modalidad:** simulación directa en ChatGPT/Codex; no se ejecutó OpenCode.

Este registro conserva completos los cuatro turnos de la simulación académica, incluidos los seis bloques Mermaid. Los mensajes del estudiante son un guion elaborado con asistencia a petición del usuario; no son mensajes humanos adicionales ni una exportación del historial completo de la aplicación. La primera respuesta es una propuesta inicial con limitaciones para comparar el antes y el después.

## Turno 1. Estudiante - Prompt inicial de la consigna

Hazme los diagramas de flujo, casos de uso y clases en mermaid de un sistema de reservas de laboratorio. Los usuarios reservan equipos por una hora y el admin aprueba las reservas. Los diagramas deben estar completos y seguir buenas prácticas. Entrégamelos en código para que pueda pegarlos en un visor.

## Turno 2. IA - Primera versión

Propongo tres diagramas: un flujo desde la solicitud hasta la decisión del administrador, los casos de uso de los actores y las clases principales. Cada bloque se pega por separado en un visor. Para el diagrama nativo de casos de uso se necesita Mermaid 12 o posterior.

### Diagrama de flujo - Antes

```mermaid
flowchart TD
    Start([Inicio]) --> Login[Iniciar sesión]
    Login --> Select[Elegir equipo y horario]
    Select --> Request[Solicitar reserva de una hora]
    Request --> Pending[Guardar como pendiente]
    Pending --> Review{¿El administrador aprueba?}
    Review -->|Sí| Approved[Marcar como aprobada]
    Review -->|No| Rejected[Marcar como rechazada]
    Approved --> Use[Usar el equipo]
    Use --> Finish([Fin])
    Rejected --> Finish
```

### Casos de uso - Antes

```mermaid
usecase-beta
direction LR
actor User("Usuario")
actor Admin("Administrador")
systemBoundary Lab["Sistema de reservas de laboratorio"]
    Browse("Consultar equipos")
    Request("Solicitar reserva de una hora")
    View("Consultar mis reservas")
    Approve("Aprobar reserva")
end
User -- Browse
User -- Request
User -- View
User -- Approve
Admin -- Approve
```

### Diagrama de clases - Antes

```mermaid
classDiagram
    class User {
        +int id
        +string name
        +requestReservation()
    }
    class Administrator {
        +int id
        +string name
        +approveReservation()
    }
    class Equipment {
        +int id
        +string name
        +bool available
    }
    class Reservation {
        +int id
        +datetime start
        +datetime end
        +string status
    }
    User --> Reservation : solicita
    Administrator --> Reservation : aprueba
    Reservation --> Equipment : utiliza
```

## Turno 3. Estudiante - Revisión y cinco cambios concretos

Al revisar la propuesta encontré tres problemas: el flujo no revisa choques de horario, el usuario aparece con permiso para aprobar y el diagrama de clases no indica multiplicidades ni estados definidos. Los justifico por separado en `fallos_y_cambios.md`. Te pido exactamente estos cinco cambios:

1. Fija cada reserva en una hora, con inicio futuro y equipo habilitado. Evita cruces con aprobadas del mismo equipo y revalida al aprobar en una operación atómica.
2. Quita al usuario común el permiso de aprobar y agrega el rechazo exclusivo del administrador. Mantén los permisos coherentes en los tres diagramas.
3. Completa las clases con multiplicidades, un administrador revisor opcional y estados enumerados para las reservas.
4. Agrega la cancelación de una reserva propia pendiente o aprobada hasta 24 horas antes. Acepta exactamente 24 horas y libera el horario si estaba aprobado.
5. Agrega que tres inasistencias bloqueen al usuario durante 30 días. Registra cada falta una sola vez e impide solicitar y aprobar durante el bloqueo.

Los primeros tres corrigen los fallos que señalé. Los últimos dos agregan las reglas que pide la actividad. Actualiza los tres diagramas y conserva los originales.

## Turno 4. IA - Versión corregida

Apliqué los cinco cambios. La solicitud queda pendiente hasta una decisión autorizada. La disponibilidad se calcula por equipo y horario, y se vuelve a comprobar al aprobar. Los casos de uso separan los permisos de los actores; las clases indican relaciones, estados y las operaciones que aplican las reglas.

En los casos de uso, `include` indica una validación obligatoria y `extend` una conducta condicional: registrar una falta solo cuando el usuario no asistió y bloquear solo al acumular la tercera. La autenticación es una precondición de todas las operaciones.

### Diagrama de flujo - Después

```mermaid
flowchart LR
    subgraph Request["1. Solicitud del usuario"]
        direction TB
        R0([Solicitar reserva]) --> R1{"¿Sesión válida y<br/>sin bloqueo vigente?"}
        R1 -->|No| R2[Denegar solicitud]
        R1 -->|Sí| R3[Elegir equipo e inicio futuro<br/>Fin = inicio + 1 hora]
        R3 --> R4{"¿Equipo habilitado y<br/>sin cruce con aprobadas?"}
        R4 -->|No| R5[Informar indisponibilidad]
        R4 -->|Sí| R6[Guardar PENDIENTE<br/>Avisar al administrador]
    end
    subgraph Review["2. Decisión del administrador"]
        direction TB
        A0([Admin autenticado:<br/>seleccionar pendiente]) --> A1{¿Aprobar?}
        A1 -->|No| A2[RECHAZADA y notificar]
        A1 -->|Sí| A3{"Revalidar al guardar:<br/>sigue pendiente, inicio futuro,<br/>usuario sin bloqueo,<br/>equipo habilitado y sin cruce"}
        A3 -->|Sí| A4[APROBADA y notificar<br/>Ocupar intervalo de forma atómica]
        A3 -->|No| A5[No aprobar y notificar<br/>Si sigue pendiente, rechazar]
    end
    subgraph Cancel["3. Cancelación por el propietario"]
        direction TB
        C0([Usuario autenticado:<br/>cancelar reserva propia]) --> C1{"¿PENDIENTE o APROBADA<br/>y faltan al menos 24 horas?"}
        C1 -->|Sí| C2[CANCELADA y notificar<br/>Liberar intervalo si estaba aprobado]
        C1 -->|No| C3[Denegar cancelación<br/>Conservar estado]
    end
    subgraph Attendance["4. Cierre y bloqueo"]
        direction TB
        T0([Admin autenticado:<br/>al terminar la hora]) --> T1{"¿APROBADA y<br/>aún sin cierre?"}
        T1 -->|No| T2[No registrar asistencia<br/>ni duplicar inasistencias]
        T1 -->|Sí| T3{¿El usuario asistió?}
        T3 -->|Sí| T4[COMPLETADA]
        T3 -->|No| T5[INASISTENCIA<br/>Sumar una al contador]
        T5 --> T6{¿Contador = 3?}
        T6 -->|No| T7[Conservar contador]
        T6 -->|Sí| T8[Bloquear por 30 días desde el registro<br/>Reiniciar contador a 0 y notificar]
    end
    %% Invisible links only arrange the four independent entry points.
    Request ~~~ Review
    Review ~~~ Cancel
    Cancel ~~~ Attendance
```

### Casos de uso - Después

```mermaid
---
config:
  layout: elk
---
usecase-beta
direction LR
actor User("Usuario")
actor Admin("Administrador")
systemBoundary Lab["Sistema de reservas de laboratorio"]
    Browse("Consultar disponibilidad")
    Request("Solicitar reserva de una hora")
    ValidateRequest("Validar usuario habilitado, inicio futuro y equipo libre")
    View("Consultar mis reservas")
    Cancel("Cancelar reserva propia")
    ValidateCancel("Validar pendiente o aprobada y plazo mínimo de 24 h")
    Approve("Aprobar reserva pendiente")
    ValidateApproval("Revalidar condiciones y guardar atómicamente")
    Reject("Rechazar reserva pendiente")
    Attendance("Registrar asistencia al terminar")
    Absence("Registrar falta de aprobada una sola vez")
    Block("Bloquear 30 días al acumular 3 faltas y reiniciar contador")
end
User -- Browse
User -- Request
User -- View
User -- Cancel
Admin -- Approve
Admin -- Reject
Admin -- Attendance
Request ..> : include ValidateRequest
Cancel ..> : include ValidateCancel
Approve ..> : include ValidateApproval
Absence ..> : extend Attendance
Block ..> : extend Absence
%% ValidateRequest also checks equipment enabled and conflicts with approved slots.
%% ValidateApproval repeats all request guards while the reservation is pending.
%% Absence extends Attendance only if the user did not attend.
```

### Diagrama de clases - Después

```mermaid
classDiagram
    direction TB
    class User {
        +int id
        +string name
        +int absenceCount
        +datetime blockedUntil
        +isBlocked(now) bool
    }
    class Administrator {
        +int id
        +string name
    }
    class Equipment {
        +int id
        +string name
        +bool enabled
    }
    class Reservation {
        +int id
        +datetime start
        +datetime end
        +ReservationStatus status
    }
    class ReservationStatus {
        <<enumeration>>
        PENDING
        APPROVED
        REJECTED
        CANCELLED
        COMPLETED
        NO_SHOW
    }
    class ReservationService {
        +request(user, equipment, start) Reservation
        +approve(admin, reservation, now)
        +reject(admin, reservation)
        +cancel(owner, reservation, now)
        +close(admin, reservation, attended, now)
    }
    User "1" --> "0..*" Reservation : solicita
    Equipment "1" --> "0..*" Reservation : recibe en distintos horarios
    Administrator "0..1" --> "0..*" Reservation : decide
    Reservation --> ReservationStatus : estado
    ReservationService ..> Reservation : valida y cambia estado
    note for Reservation "end = start + 1 h; inicio futuro.<br/>Intervalo [start, end); sin cruce de aprobadas por equipo.<br/>Cancelar propia PENDING o APPROVED<br/>si now <= start - 24 h."
    note for User "blockedUntil puede ser nulo.<br/>Bloqueado si now < blockedUntil.<br/>Tercera falta: bloquear 30 días desde now<br/>y poner absenceCount = 0."
    note for ReservationService "Sesión y rol verificados en cada operación.<br/>Aprobar: revalidar usuario, equipo, estado y horario;<br/>comprobar y guardar de forma atómica.<br/>Cerrar una vez: APPROVED y now >= end."
```

### Criterios aplicados

Tomé los intervalos como [inicio, fin), por lo que dos reservas consecutivas pueden compartir la hora de fin/inicio. Solo las aprobadas ocupan equipo. La asistencia se registra por el administrador al terminar la hora; una cancelada no genera falta. Las tres faltas se acumulan desde el último bloqueo y el contador se reinicia al aplicar la sanción; el historial se conserva. Los 30 días empiezan al registrar la tercera falta y el usuario queda habilitado exactamente al cumplirse el plazo. El bloqueo no cancela automáticamente reservas previamente aprobadas. Todas las operaciones comprueban sesión y rol; la cancelación también comprueba propiedad. Estos detalles son supuestos de esta simulación porque la consigna no los define.

La validación de sintaxis y las capturas se realizan en un visor local con Mermaid 12.2.0. No se presentan como evidencia de revisión en mermaid.live. Los diagramas modelan reglas; no se implementó un sistema de reservas ni se probaron transacciones reales.
