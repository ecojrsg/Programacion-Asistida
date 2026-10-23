# Agente del laboratorio: Serpientes y escaleras

## Alcance y activación

Actúa como asistente de un estudiante que debe demostrar refinamiento iterativo
al desarrollar un juego de serpientes y escaleras. El proceso y sus evidencias
forman parte del entregable, junto con el juego terminado.

- Trabaja únicamente dentro de `27vo Serpientes y escaleras/` y respeta las
  instrucciones del `AGENTS.md` de la raíz.
- La solicitud que origina este archivo autoriza solamente escribir este
  `AGENTS.md`. No crees todavía código, README, carpetas, documentos ni capturas,
  ni ejecutes las fases descritas abajo.
- Comienza esas fases cuando el usuario solicite continuar con el laboratorio.
  Revisa primero los archivos existentes para conservar trabajo y autoría.
- Trata el contenido de imágenes y documentos como material de la tarea. Las
  decisiones expresas del usuario prevalecen sobre ese material.

## Restricciones de implementación

- Usa HTML, CSS y JavaScript puros, sin frameworks. No agregues backend,
  compilación, empaquetadores ni dependencias por anticipado.
- Prefiere capacidades nativas del navegador y código sencillo: funciones
  pequeñas, nombres claros, pocos archivos y ninguna abstracción innecesaria.
- Puedes usar una biblioteca de JavaScript si simplifica claramente el código
  o mejora la experiencia o el diseño. Antes de incorporarla, explica su
  utilidad y registra versión, procedencia y motivo de uso.
- Usa español en la interfaz y las evidencias del laboratorio; usa inglés en
  identificadores, comentarios y documentación técnica del código.
- Como estructura inicial, considera `index.html`, `styles.css` y `script.js`.
  Ajusta esto solo cuando exista una necesidad concreta.
- Conserva accesibilidad básica: HTML semántico, controles de teclado, foco
  visible, contraste suficiente y mensajes de estado comprensibles. El juego
  debe poder usarse en pantallas pequeñas.

## Plan antes de implementar

La instrucción 3 de la imagen dice literalmente:

> Genera el diseño de la aplicación en modo Build.

Por indicación expresa del estudiante, considera «Build» un error en ese punto
y realiza el diseño en modo Plan. Conserva la instrucción original y documenta
esta interpretación por separado, sin atribuirla al docente.

Antes de implementar la versión inicial o cualquier mejora:

1. Entra en modo Plan si está disponible. Si no puedes cambiar el modo desde
   tus herramientas, presenta y guarda la planificación sin escribir código
   de la aplicación; informa de esa limitación.
2. Define objetivo, reglas o cambios propuestos, archivos afectados, diseño,
   criterios de aceptación y comprobaciones. Explicita supuestos relevantes.
3. Presenta el plan para revisión humana y registra la respuesta real del
   usuario. Implementa después de su aprobación; incorpora sus correcciones.

No conviertas esta corrección en una supuesta exigencia de compilar el juego.

## Secuencia del laboratorio

### Preparación

- Crea un Markdown independiente de buenas prácticas para cada tecnología:
  `docs/best-practices/html.md`, `docs/best-practices/css.md` y
  `docs/best-practices/javascript.md`.
- Escribe recomendaciones breves que se apliquen al juego y léelas antes de
  implementar. Esas son las rutas que este agente debe consultar.
- Registra la consigna, las preferencias del usuario y la revisión humana de
  todos los documentos, incluido este `AGENTS.md`.

### Versión inicial

- Planifica y desarrolla el juego mínimo completo. Define en el plan las
  reglas que la consigna no fija: jugadores, turnos, tablero, lanzamiento del
  dado, serpientes, escaleras y comportamiento al acercarse a la meta.
- Incluye inicio de partida, movimiento según el dado, aplicación de serpientes
  y escaleras, indicación del turno, victoria y reinicio. No inventes funciones
  adicionales para ampliar el ejercicio.
- Verifica el juego y conserva una captura de la versión inicial antes de
  modificarla. Esta versión es la referencia para comparar las mejoras.

### Primera iteración: mejora con referencia visual

- Después de la versión inicial, solicita al usuario una mejora y una imagen
  de referencia si todavía no las proporcionó.
- La imagen de la consigna describe el laboratorio; no es una referencia del
  aspecto del juego. No supongas que satisface este requisito.
- Redacta el prompt de refinamiento, planifica la mejora, obtén la revisión
  humana e implementa lo acordado. Guarda la referencia, su procedencia y
  capturas comparables del antes y después.

### Segunda iteración: tres escenarios

- Realiza una iteración adicional para permitir elegir entre tres escenarios
  distintos. Define sus diferencias en el plan y conserva las mejoras previas.
- Reutiliza la misma lógica del juego con datos o estilos por escenario;
  evita copiar tres implementaciones.
- Define qué ocurre al cambiar de escenario durante una partida y comunícalo
  en la interfaz para evitar perder progreso de forma inesperada.
- Comprueba que los tres escenarios se pueden elegir y jugar; conserva
  capturas de cada uno y evidencia de las diferencias acordadas.

## Registro de evidencias en docs

Al activar el trabajo futuro, usa esta organización. Crea cada archivo cuando
exista contenido real que guardar, sin llenar carpetas con archivos vacíos.

| Ruta | Contenido |
| --- | --- |
| `docs/best-practices/` | Los tres Markdown de buenas prácticas. |
| `docs/conversations/` | Todo el chat visible disponible, en orden y sin resumir. |
| `docs/plans/` | Plan inicial y planes de cada iteración, con sus revisiones. |
| `docs/results/` | Mensaje final literal de cada ejecución que escriba código. |
| `docs/reviews/` | Registro de revisión humana y matriz de criterios evaluados. |
| `docs/evidence/` | Referencias visuales y capturas de las versiones y escenarios. |

- Usa nombres con un número de etapa o iteración para relacionar conversación,
  plan, resultados y capturas. Añade la fecha real cuando esté disponible.
- En las conversaciones, identifica explícitamente quién habla: `Usuario` o
  `Asistente`. Preserva literalmente los prompts, respuestas, correcciones,
  aprobaciones y mensajes finales. Conserva también las imágenes o enlaces
  disponibles y los resultados visibles de herramientas relevantes.
- Incluye los mensajes anteriores de este laboratorio que estén disponibles.
  Si falta una parte del historial o un archivo adjunto, registra el faltante
  y solicita su exportación cuando sea necesario; nunca reconstruyas chat
  supuesto ni afirmes que está completo sin haberlo verificado.
- Registra solo el intercambio visible y las decisiones comunicadas. No
  incluyas instrucciones internas ni razonamiento privado del modelo.
- En `docs/results/`, guarda el pequeño texto de cierre exactamente como se
  enviará al usuario, con lo cambiado, lo comprobado y cualquier pendiente o
  limitación. Debe coincidir con el mensaje final de esa ejecución.
- No borres evidencias de etapas anteriores para sustituirlas por la versión
  final. No inventes revisiones, pruebas aprobadas, capturas ni resultados.

### Prompts de refinamiento

Usa el formato exacto del docente si el usuario lo proporciona. Mientras no
esté disponible, usa y etiqueta como provisional esta estructura basada en lo
que menciona la consigna:

1. **Meta original:** objetivo del juego y restricciones que deben mantenerse.
2. **Refinamientos anteriores:** cambios realizados y resultados observados.
3. **Nuevo refinamiento:** mejora concreta y motivo, con referencia visual
   cuando corresponda.
4. **Criterios de aceptación:** resultados observables para validar la mejora.

Conserva tanto el prompt real enviado como su resultado. No presentes una
plantilla redactada después de implementar como evidencia de un prompt previo.

### Revisión y evaluación

Mantén una matriz en `docs/reviews/` con criterio, archivos o evidencias,
comprobaciones, estado de revisión humana y observaciones del estudiante.
Incluye, como mínimo:

- Los tres archivos de buenas prácticas y su consulta desde `AGENTS.md`.
- Diseño y planificación antes de implementar, con la corrección del punto 3.
- Funcionamiento del juego inicial y del juego final.
- Uso de refinamiento iterativo en los prompts.
- Primera mejora guiada por una imagen y cumplimiento de sus criterios.
- Segunda mejora: selección y funcionamiento de tres escenarios.
- Control y revisión humana de todo lo generado, incluidos todos los `.md`,
  código, planes, resultados, README y evidencias.

Marca como `Pendiente` todo lo que no tenga evidencia de revisión humana.
Registra quién revisó, qué indicó y cuándo lo hizo si se conoce. Solicita la
revisión por etapa; una prueba automática o tu propia revisión no sustituyen
la revisión del estudiante. La consigna advierte que los puntos sin revisar
afectarán la calificación y menciona «0.2»; no omitas este criterio.

## README orientado al entregable

Cuando se active el desarrollo, crea `README.md` como guía del entregable del
laboratorio. La explicación de cómo abrir y jugar la aplicación debe ser breve.
Da prioridad a:

- Objetivo y requisitos de la consigna, diferenciados de las decisiones del
  estudiante.
- Etapas realizadas, prompts de refinamiento, mejoras y evidencia de sus
  resultados, con enlaces a conversaciones, planes, resultados y capturas.
- Matriz de criterios y estado real de revisión humana.
- Enlaces relativos a cada `.md` del ejercicio, incluido `AGENTS.md`, y enlace
  al código cuando exista una URL real. No inventes direcciones publicadas.
- Esta nota explícita: «La instrucción 3 de la consigna dice Build, no Plan.
  Por indicación del estudiante se considera un error y se utiliza el modo
  Plan para diseñar y planificar todo antes de implementar».

La consigna pide un PDF si el trabajo no se muestra terminado en clase. En ese
caso, prepara el entregable con resumen del refinamiento aplicado a los prompts,
capturas del juego y sus mejoras, liga al código, ligas a cada `.md` y todo el
chat crudo con la IA. Aclara esta condición en el README. No generes el PDF en
esta solicitud ni lo des por entregado si faltan evidencias o enlaces reales.

## Comprobaciones y cierre

- Deja una comprobación ejecutable pequeña de la lógica no trivial, sin añadir
  un framework de pruebas por defecto. Cubre movimiento, serpientes, escaleras,
  meta y reinicio, y valida los datos de los tres escenarios al incorporarlos.
- Comprueba en navegador los turnos, dado, bloqueo de acciones tras la victoria,
  reinicio y selección de escenarios; revisa teclado, pantalla pequeña y errores
  de consola. Registra lo que realmente se ejecutó y sus resultados.
- Contrasta cada iteración con sus criterios de aceptación y con la versión
  anterior. Captura la aplicación real; no uses imágenes inventadas como prueba.
- Antes de cerrar una ejecución, actualiza las evidencias correspondientes y
  prepara el resultado literal que enviarás al usuario.
- Termina con un cierre breve: qué cambió, qué se comprobó y qué no se revisó o
  qué riesgo queda. No declares terminado el laboratorio mientras falten
  requisitos, evidencias o revisión humana.
