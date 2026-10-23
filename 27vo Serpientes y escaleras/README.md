# Laboratorio de refinamiento iterativo

Ejercicio 27: serpientes y escaleras con HTML, CSS y JavaScript puros.
Este README organiza el entregable y sus evidencias. La primera versión está
implementada y verificada técnicamente. El PDF reúne los refinamientos y las
evidencias; siguen pendientes los tres escenarios y la revisión humana completa.

## Consigna y decisión sobre el modo Plan

La [imagen original](docs/evidence/00-assignment.png) solicita buenas prácticas
por tecnología, un agente que las consulte, diseño, implementación, una mejora
con imagen de referencia y otra mejora para elegir entre tres escenarios.

**La instrucción 3 de la consigna dice Build, no Plan. Por indicación del
estudiante se considera un error y se utiliza el modo Plan para diseñar y
planificar todo antes de implementar.** Esta interpretación pertenece al
estudiante; no modifica ni se atribuye al texto original del docente.

El usuario aprobó el [plan de fase 1](docs/plans/00-first-phase.md) con el mensaje
«Hazlo implementalo», registrado antes de escribir el código.

## Etapas y evidencias

| Etapa | Resultado | Evidencia |
| --- | --- | --- |
| Preparación | Agente y tres documentos de buenas prácticas, consultados antes del código. | [AGENTS](AGENTS.md) y documentos del índice. |
| Planificación | Dos jugadores locales, diorama colorido, reglas y efectos separados. Plan aprobado. | [Plan](docs/plans/00-first-phase.md), [conversación](docs/conversations/00-planning.md). |
| Versión inicial | Juego completo: inicio, turnos, dado, saltos, meta exacta y reinicio. | [Juego](index.html), [verificación](docs/reviews/01-verification.md), capturas. |
| Corrección de adaptación | Centrado horizontal y vertical, tamaño limitado y scroll cuando el contenido lo requiere. | [Diagnóstico, plan y verificación](docs/plans/02-layout-fix.md). |
| Rectificación de la comprobación | Se retiró una resolución de prueba que quedó activa en Chrome y se ajustó la ventana actual. Sin cambios en la aplicación. | [Diagnóstico y límites](docs/plans/03-browser-window.md), [captura](docs/evidence/03-window-3424.jpg). |
| Ajuste de distribución | A petición del usuario, centrado solo horizontal y contenido alineado arriba; leyenda separada del tablero para mostrar los iconos completos. | [Plan y verificación](docs/plans/04-board-spacing.md), [captura](docs/evidence/04-desktop-spacing.jpg). |
| Refinamiento del dado | Lanzamiento de 1.25 s con elevación, rebote y asentamiento; sincronización con la ficha y movimiento reducido. | [Plan y pruebas](docs/plans/05-dice-motion.md), [comprobación ejecutable](tests/motion.html). |
| Corrección del dado | Giro continuo de 1.25 s; el marcador muestra «…» y revela el número al asentarse, antes de mover la ficha. Sustituye el movimiento por tramos anterior. | [Plan, pruebas y capturas](docs/plans/06-continuous-roll.md). |
| Entrega en PDF | Documento de 23 páginas, ocho capturas, 54 intervenciones de chat y ligas a los 31 Markdown. | [PDF](../PDFs%20ejercicios/Ejercicio_27_Serpientes_y_Escaleras.pdf), [comprobación](docs/reviews/07-pdf-delivery.md). |
| Mejora con referencia visual | Corrección de distribución realizada con una captura del usuario; validación académica final pendiente. | [Referencia](docs/evidence/04-user-spacing.png), [plan y resultado](docs/plans/04-board-spacing.md). |
| Iteración 2 | Pendiente: agregar selección entre tres escenarios y comprobarlos. | Debe conservar la mejora de la iteración anterior. |

Se usó este flujo: petición → preguntas y elecciones del estudiante → plan escrito
→ aprobación humana → implementación → pruebas → resultado y pendientes.
Se distinguen las correcciones técnicas, la mejora con referencia visual y la
iteración de tres escenarios que todavía falta. El PDF no inventa validación
del docente ni afirma que el laboratorio esté completamente terminado.

Para los refinamientos posteriores se conservarán los prompts reales con
**Meta original**, **Refinamientos anteriores**, **Nuevo refinamiento** y
**Criterios de aceptación**. Ese formato es provisional hasta recibir el ejemplo
exacto del docente. No se inventaron prompts anteriores a la implementación.

## Evidencias de la primera versión

- [Escritorio: partida inicial](docs/evidence/01-desktop.jpg).
- [Móvil: interfaz a 390 px](docs/evidence/01-mobile.jpg).
- [Escalera y fichas compartiendo casilla](docs/evidence/01-ladder-shared.jpg).
- [Victoria real después de 13 tiradas](docs/evidence/01-victory.jpg).

Se aprobaron **17 comprobaciones deterministas** de las reglas y se verificaron
partida completa, doble clic, reinicio, teclado, diseño a 320 y 390 px,
movimiento reducido y recuperación ante errores visuales en Chrome. El informe
detalla los resultados reales y sus límites; no sustituye revisión humana.

## Índice de todos los Markdown

| Documento | Propósito |
| --- | --- |
| [README.md](README.md) | Guía del entregable del laboratorio. |
| [AGENTS.md](AGENTS.md) | Instrucciones del agente y rutas de buenas prácticas. |
| [PRODUCT.md](PRODUCT.md) | Contexto confirmado de producto y restricciones técnicas. |
| [Buenas prácticas de HTML](docs/best-practices/html.md) | Semántica, controles y accesibilidad. |
| [Buenas prácticas de CSS](docs/best-practices/css.md) | Distribución, legibilidad y movimiento. |
| [Buenas prácticas de JavaScript](docs/best-practices/javascript.md) | Reglas, estado, validación y efectos opcionales. |
| [Conversación de planificación](docs/conversations/00-planning.md) | Interlocutores, mensajes y decisiones iniciales. |
| [Conversación de implementación](docs/conversations/01-implementation.md) | Petición de implementación, avances y cierre. |
| [Plan de fase 1](docs/plans/00-first-phase.md) | Reglas, diseño, alcance y aceptación aprobados. |
| [Registro de revisión humana](docs/reviews/00-review-status.md) | Criterios evaluados y pendientes reales. |
| [Verificación técnica](docs/reviews/01-verification.md) | Inventario, pruebas, capturas y limitaciones. |
| [Resultado de fase 1](docs/results/01-first-phase.md) | Texto final literal de esta ejecución. |
| [Plan y verificación de adaptación](docs/plans/02-layout-fix.md) | Diagnóstico, corrección de pantalla y capturas antes/después. |
| [Conversación de adaptación](docs/conversations/02-layout-fix.md) | Solicitud y avances de la corrección. |
| [Resultado de adaptación](docs/results/02-layout-fix.md) | Texto final literal de la corrección. |
| [Diagnóstico de ventana](docs/plans/03-browser-window.md) | Emulación, medidas actuales, captura y límites de la comprobación. |
| [Conversación de ventana](docs/conversations/03-browser-window.md) | Nueva observación del usuario, diagnóstico y cierre. |
| [Resultado de ventana](docs/results/03-browser-window.md) | Texto final literal del ajuste de Chrome. |
| [Plan de distribución](docs/plans/04-board-spacing.md) | Diagnóstico del solapamiento, corrección, medidas y capturas. |
| [Conversación de distribución](docs/conversations/04-board-spacing.md) | Petición del usuario, avances y cierre. |
| [Resultado de distribución](docs/results/04-board-spacing.md) | Texto final literal de la corrección de CSS. |
| [Plan y pruebas del dado](docs/plans/05-dice-motion.md) | Movimiento, integración, comprobaciones y capturas. |
| [Conversación del dado](docs/conversations/05-dice-motion.md) | Petición de mejora, avances y cierre. |
| [Resultado del dado](docs/results/05-dice-motion.md) | Texto final literal del refinamiento. |
| [Corrección del giro y marcador](docs/plans/06-continuous-roll.md) | Diagnóstico de las pausas, sincronización y verificación. |
| [Conversación de giro continuo](docs/conversations/06-continuous-roll.md) | Observaciones del usuario y respuesta de corrección. |
| [Resultado de giro continuo](docs/results/06-continuous-roll.md) | Texto final literal de esta corrección. |
| [Plan de entrega en PDF](docs/plans/07-pdf-delivery.md) | Alcance, formato de referencia y verificaciones previstas. |
| [Conversación de entrega](docs/conversations/07-pdf-delivery.md) | Solicitud del PDF y avances. |
| [Comprobación de la entrega](docs/reviews/07-pdf-delivery.md) | Fuentes del documento y estado de las verificaciones. |
| [Resultado de entrega](docs/results/07-pdf-delivery.md) | Cierre de esta fase. |

Las conversaciones por etapa son transcripciones manuales. Para el PDF se
recuperó el registro nativo y se exportó el chat de desarrollo sin resumir en
[UTF-8](docs/conversations/07-chat-crudo.txt) y
[JSONL](docs/conversations/07-chat-crudo.jsonl), con formulario y selecciones.
El corte llega hasta la solicitud del PDF inclusive. Se excluyen contexto
interno, razonamiento privado y trazas de herramientas. La fase de preparación
del PDF se documenta aparte y la revisión humana de esta exportación sigue
pendiente. Los anexos de skills inyectados como contexto no son mensajes humanos.

## Código y ejecución breve

Abre [index.html](index.html) con doble clic en un navegador. No requiere
instalaciones, servidor o conexión de red. Comienza la partida y usa «Lanzar dado».
El progreso vive en esa pestaña: recargar o cerrar la página comienza de nuevo.

Las [reglas](game.js) reciben una tirada y devuelven el siguiente estado; los
[controles](script.js) administran la interfaz. El [diseño base](styles.css) y los
[efectos CSS](visuals/effects.css) / [efectos JavaScript](visuals/effects.js) se
mantienen separados. Se emplea volumen con CSS 3D y SVG nativo, inspirado en el
acabado de Anatomy. No se añadió una dependencia de vídeo ni una biblioteca.

Abre [tests/rules.html](tests/rules.html) para repetir las 17 comprobaciones de
reglas en el navegador.

Abre [tests/motion.html](tests/motion.html) para comprobar las seis caras,
tiradas repetidas, continuidad del giro, cancelación y revelación del resultado.
Su función actual aprobó 39 comprobaciones con movimiento normal y 38 con
movimiento reducido. Los métodos y las pruebas de integración están en el
[informe actualizado](docs/plans/06-continuous-roll.md).

Repositorio configurado en `origin`:
[ecojrsg/Programacion-Asistida](https://github.com/ecojrsg/Programacion-Asistida).
La entrega publicó el código en la revisión
[20723eb](https://github.com/ecojrsg/Programacion-Asistida/tree/20723eb8909e0b4dbe0e7852a2fa0c7021c3256a/27vo%20Serpientes%20y%20escaleras).
La ruta y la revisión se verificaron con gh. El PDF usa esa referencia fija
para el código y enlaces a main para los documentos. El usuario autorizó
expresamente publicar también PDF, chat, capturas y Markdown en el repositorio
público, con su nombre y matrícula en la portada.

## Revisión humana y entrega

La revisión del agente y del plan tiene evidencia en el chat. El código, los
documentos nuevos y las capturas todavía deben revisarse por el estudiante y
anotarse en la [matriz](docs/reviews/00-review-status.md). La consigna incluye
todos los `.md` y advierte una afectación a la calificación, mencionando «0.2»,
si hay puntos sin revisar. No se marcaron como revisados automáticamente.

Si el juego no se muestra terminado en clase, la consigna pide un **PDF** con:

- Resumen del refinamiento aplicado a los prompts.
- Capturas del juego y de las mejoras de cada iteración.
- Liga al código entregado y ligas a cada `.md`.
- Todo el chat crudo con la IA.

El [PDF del ejercicio](../PDFs%20ejercicios/Ejercicio_27_Serpientes_y_Escaleras.pdf)
ya está generado. Se revisaron sus 23 páginas y 56 enlaces; el chat de desarrollo
se cotejó con su exportación nativa. Los ocho archivos del juego y sus pruebas
conservan sus hashes SHA256 anteriores a esta fase. El PDF señala expresamente
que los tres escenarios y la revisión humana de todos los documentos están
pendientes. La conversación de esta preparación queda registrada aparte del
chat de desarrollo, cuyo corte llega hasta la solicitud del PDF inclusive.
