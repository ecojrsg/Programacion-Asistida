# Revisión humana y criterios del laboratorio

Fecha: 2026-10-22, America/Mexico_City.
Revisor identificado: usuario del chat; no se ha solicitado ni supuesto un nombre.

## Decisiones con evidencia humana

| Elemento | Evidencia | Alcance de la revisión |
| --- | --- | --- |
| Configuración de `AGENTS.md` | «Perfecto ahora iniciemos el plan de implementación de la primera fase.» | Aceptación de la configuración del agente; no demuestra revisión de código futuro. |
| Dos jugadores locales | Selección del formulario de planificación | Decisión confirmada. |
| Diorama colorido | Selección del formulario de planificación | Dirección visual confirmada. |
| Efectos en archivos separados | Selección del formulario de planificación | Integrados en el juego, sin bloque visual independiente. |
| Adaptación de la interfaz inicial | El usuario indicó que no se adapta al poner pantalla completa y solicitó centrado y scroll condicional. | Revisión humana parcial de la interfaz; generó la corrección 02. No implica aprobación de todos los archivos. |

«Sigue» solicita continuar la planificación. No se registra como aprobación de
un plan escrito que todavía no se había presentado al usuario.

Después de presentar el plan escrito, el usuario indicó «Hazlo implementalo».
Esta respuesta aprueba la implementación del plan el 2026-10-22; no se utiliza
como evidencia de revisión del código y los documentos que se generaron después.

## Documentos actuales

| Archivo | Revisión técnica del asistente | Revisión humana |
| --- | --- | --- |
| `AGENTS.md` | Consultado para preparar el plan. | Aceptación registrada arriba. |
| `PRODUCT.md` | Basado en requisitos y respuestas confirmadas. | Pendiente. |
| `docs/plans/00-first-phase.md` | Contrastado con consigna y decisiones confirmadas. | Aprobado: «Hazlo implementalo». |
| `docs/conversations/00-planning.md` | Orden, interlocutores y límites de la transcripción indicados. | Pendiente. |
| `docs/reviews/00-review-status.md` | Distingue decisiones confirmadas de documentos pendientes. | Pendiente. |
| `docs/evidence/00-assignment.png` | Copia sin cambios; hashes SHA256 iguales al original. | Pendiente como evidencia conservada. |

Una comprobación técnica no equivale a revisión humana. No cambiar `Pendiente`
sin una respuesta real que permita identificar qué se revisó y qué se corrigió.

## Matriz del laboratorio

| Criterio | Evidencia actual o prevista | Estado actual |
| --- | --- | --- |
| Un Markdown de buenas prácticas por tecnología | Tres archivos en `docs/best-practices/`, creados y consultados antes del código. | Hecho; revisión humana pendiente. |
| AGENTS que señale las buenas prácticas | `AGENTS.md` contiene las tres rutas existentes. | Hecho. |
| Planificación antes del código | `docs/plans/00-first-phase.md` y conversación. | Plan aprobado por el usuario antes de implementar. |
| Corrección de Build a Plan | Agente, plan y nota explícita en README. | Documentado; revisión humana del README pendiente. |
| Juego inicial completo | Código, pruebas y capturas de fase 1. | Implementado y verificado; revisión humana pendiente. |
| Refinamiento iterativo en prompts | Formato provisional en el agente; conservar prompts reales al ejecutarlos. | Iteraciones pendientes. |
| Mejora con imagen de referencia | Captura del usuario y corrección de distribución 04. La consigna no se usa como referencia del diseño. | Realizada como refinamiento; validación académica final pendiente. |
| Mejora adicional con tres escenarios | Será una iteración posterior a la mejora con imagen. | Pendiente. |
| Control humano de todo lo generado, incluidos los `.md` | Este registro y respuestas reales del estudiante. | Parcial; documentos nuevos pendientes. |
| Capturas auténticas del juego y las mejoras | Cuatro capturas de fase 1 en `docs/evidence/`; las mejoras son etapas futuras. | Versión inicial hecha; mejoras pendientes. |
| README orientado al entregable y enlaces a cada `.md` | `README.md` reúne las evidencias y el índice. | Hecho; revisión humana pendiente. |
| Liga al código | Revisión 20723eb publicada y comprobada con gh. | Hecho. |
| Todo el chat crudo con la IA | Exportación nativa de 54 intervenciones hasta la solicitud del PDF inclusive; fase PDF documentada aparte. | Exportado y cotejado; revisión humana pendiente. |
| PDF si no se demuestra terminado en clase | PDF de 23 páginas, capturas, ligas y chat. | Generado y revisado técnicamente; revisión humana pendiente. |

La consigna advierte que los puntos sin revisión afectan la calificación y
menciona «0.2». Esta matriz conserva los pendientes en lugar de declararlos
cumplidos anticipadamente.

## Archivos añadidos durante la implementación

La revisión humana de `index.html`, `styles.css`, `game.js`, `script.js`, ambos
archivos de `visuals/`, `tests/rules.html`, `README.md`, los tres documentos de
buenas prácticas, la conversación de fase 1, el informe de verificación, el
resultado de ejecución y las cuatro capturas permanece **Pendiente**. La revisión
técnica y sus resultados están en [01-verification.md](01-verification.md).

La corrección posterior de centrado, su conversación, resultado, documentación
de CSS y capturas siguen pendientes de revisión humana. Sus medidas están en
[02-layout-fix.md](../plans/02-layout-fix.md). Se registra como corrección de
adaptación; la iteración con imagen y los tres escenarios continúan pendientes.

El usuario revisó el resultado visual de la corrección 02 y señaló «nuevamente
no queda centrado, revisalo bien», adjuntando una captura. No se registra como
aprobación. El [diagnóstico 03](../plans/03-browser-window.md) encontró una
resolución de emulación que quedó activa en Chrome. Se ajustó la sesión de
pruebas sin cambiar la aplicación. La nueva captura, el diagnóstico, la
conversación y el resultado siguen pendientes de revisión humana.

El usuario confirmó el centrado horizontal, pidió retirar el centrado vertical
y señaló elementos tapados en una nueva captura. La [corrección 04](../plans/04-board-spacing.md)
separa la leyenda del tablero inclinado y alinea el contenido arriba. Esto
registra una revisión parcial de la distribución anterior, no una aprobación
de los archivos nuevos. El CSS modificado, las buenas prácticas actualizadas,
el plan, la conversación, el cierre, README y las tres evidencias de esta
corrección permanecen **Pendientes** de revisión humana posterior.

El usuario respondió «Super bien» tras el resultado de distribución 04 y pidió
mejorar la duración y naturalidad del dado. Se registra aceptación del resultado
visual de distribución, sin suponer revisión de todos sus archivos. El
[refinamiento 05](../plans/05-dice-motion.md) modifica el giro y su integración.
Su código, prueba de movimiento, documentos, README y capturas siguen
**Pendientes** de revisión humana. Las pruebas técnicas no sustituyen la
valoración del estudiante sobre la naturalidad del movimiento.

El usuario revisó el refinamiento 05 y señaló pausas y cambios de velocidad,
además de un resultado revelado antes del giro. Se registra como solicitud de
corrección, no como aprobación. La [corrección 06](../plans/06-continuous-roll.md)
utiliza un giro continuo y sincroniza el marcador al asentarse. Su código,
prueba ampliada, documentos, README y capturas siguen **Pendientes** de revisión
humana; la comprobación técnica no da por aceptada la fluidez percibida.

El usuario respondió «Perfecto» tras comprobar el giro y pidió el PDF sin más
cambios del juego. Se registra aceptación de ese resultado observado. Durante
la preparación autorizó expresamente «Sí, publicar todo el entregable» después
de indicar que el repositorio es público y el PDF incluye nombre y matrícula.
Esa autorización permite la publicación; no equivale a aprobar académicamente
todos los Markdown. El PDF, las exportaciones, los generadores y la documentación
de entrega continúan pendientes de revisión humana. Los tres escenarios siguen
sin implementar, como declara el informe.
