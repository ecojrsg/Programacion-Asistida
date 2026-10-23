# Verificación técnica de la fase 1

Fecha: 2026-10-22, America/Mexico_City.
La revisión técnica del asistente no sustituye la revisión humana del estudiante.

## Inventario previo a las pruebas

| Afirmación o control | Comprobación y evidencia prevista |
| --- | --- |
| Abrir sin instalar dependencias | Cargar el archivo local con sus CSS y scripts. |
| Comenzar y alternar turnos | Botón y teclado; inicio en salida, cambio de jugador. |
| Movimiento, escaleras y serpientes | Aserciones deterministas y una partida real. |
| Ganar exactamente y bloquear después | Casos de meta y exceso; captura del ganador. |
| Reiniciar y cancelar reinicio | Diálogo nativo, conservación y restablecimiento de estado. |
| Protección frente a doble clic | Dos activaciones rápidas producen una sola tirada. |
| Efectos separados y opcionales | Desactivar o hacer fallar efectos; comprobar la regla final. |
| Dado y ficha coherentes con el estado | Resultado numérico, cara del dado y posición al terminar. |
| Casilla compartida | Dos fichas distinguibles al coincidir. |
| Diseño adaptable y accesible | Capturas de escritorio y móvil; 320 px, foco y movimiento reducido. |
| Movimiento ligero | Sin animaciones en reposo; probar con CPU limitada. |
| Laboratorio documentado | Revisar enlaces, evidencias y texto final literal. |

Casos exploratorios: intentar jugar tras ganar; reiniciar durante una animación;
provocar un fallo de la capa visual; sobrepasar la meta.

## Resultados

Entorno: Chrome 155 en Windows, archivos locales `file://`, sin instalar
dependencias. La comprobación de sintaxis de los tres archivos JavaScript
terminó sin errores con `node --check`.

| Comprobación ejecutada | Resultado observado |
| --- | --- |
| Página `tests/rules.html` | 17 comprobaciones aprobadas, incluidos todos los saltos del mapa. |
| Inicio con Enter y lanzamiento con Espacio | Jugador 1 comenzó en 0 y una tirada de 3 terminó en 22; foco visible. |
| Dos clics consecutivos y reinicio durante movimiento | Una sola tirada; ambos botones bloqueados durante la transición. |
| Cancelar reinicio mediante confirmación nativa | Se conservaron posiciones y turno. |
| Aceptar reinicio mediante confirmación nativa | Regresó a salida, cero tiradas y dado sin resultado. |
| Dos jugadores en 22 | Ambas fichas visibles y distinguibles, con números y formas diferentes. |
| Partida completa | Jugador 1 ganó en 100 después de 13 tiradas; Jugador 2 terminó en 5 tras una serpiente. |
| Acción después de ganar | Lanzamiento deshabilitado; no cambió el número de tiradas; reinicio disponible. |
| Fallo provocado en `Visuals.play` | Se completó el salto a 22, se desactivó la decoración y siguió disponible el juego básico. |
| Sin efectos y con su CSS desactivado | Tablero básico jugable; salto, turno, posiciones y mensajes correctos. |
| Efecto que nunca responde | La espera terminó aproximadamente a los 1620 ms; el turno se completó y los controles se habilitaron. |
| Movimiento reducido a 320 px | Salto correcto en unos 7 ms de la prueba, sin animaciones activas. |
| Diseño final a 320 px | Sin desbordamiento horizontal; números y etiquetas de jugadores de 11 px; botón de 48 px. |
| Móvil de 390 × 844 | Jugadores encima del tablero y controles debajo; captura real de página completa. |
| Escritorio de 1440 × 1000 | Tablero y controles dentro del primer viewport: bordes inferiores aproximadamente 888 y 772 px. |
| CPU limitada a 4 veces más lenta | Tirada animada de 6 correcta, unos 1327 ms incluidos 200 ms de espera para inspeccionar reposo. |
| Reposo después de animar | Cero animaciones activas; no se usa un bucle permanente. |
| Consola en partidas normales | Sin errores ni advertencias; el fallo visual provocado produjo únicamente su advertencia esperada. |

Se controló temporalmente `Math.random` en las pestañas de prueba para obtener
tiradas repetibles; no se alteraron posiciones o ganadores directamente ni se
añadieron controles de depuración al producto. La secuencia de la partida fue
`3, 3, 6, 1, 3, 1, 6, 1, 5, 1, 6, 1, 6`, activando el botón de lanzamiento en
cada turno. La partida se repitió con movimiento reducido para las capturas
finales. Después se recargó la pestaña para restaurar el azar normal.

Durante una prueba del reinicio con teclado, el diálogo detuvo temporalmente la
herramienta de automatización. Se cerró esa pestaña de prueba y se continuó con
una sesión aislada. La aceptación y cancelación del reinicio se comprobaron con
el diálogo nativo desde la evaluación del navegador; no se atribuye este bloqueo
de la herramienta a un fallo de las reglas.

## Inspección visual y contraste

Se revisaron las capturas de escritorio y móvil. Se redujo el tablero de
escritorio para conservar visibles las piezas de salida, se colocaron los
jugadores antes del tablero en móvil y se separaron las fichas coincidentes.
El detector de Impeccable señaló textos pequeños: se ampliaron etiquetas,
leyendas y números en móvil, y se retiró una etiqueta de meta redundante.

Los pares principales de texto y fondo de la paleta dan contrastes calculados
de 10.40:1 (texto principal), 5.28:1 (secundario), 4.92:1 (etiqueta de jugador
activo), 5.12:1 (ficha coral) y 6.59:1 (ficha verde). El texto sobre el borde
de madera se oscureció hasta 5.60:1 respecto al tono más oscuro de la base.

El detector también señaló el fondo crema y una sombra como patrones genéricos.
Se conservaron: el diorama claro es una decisión aprobada, y la sombra tiene
desplazamiento vertical para representar la base física. No se afirma que el
detector haya terminado sin advertencias.

## Capturas auténticas

- [Inicio en escritorio](../evidence/01-desktop.jpg).
- [Vista móvil](../evidence/01-mobile.jpg).
- [Escalera y dos fichas en la casilla 22](../evidence/01-ladder-shared.jpg).
- [Victoria tras 13 tiradas](../evidence/01-victory.jpg).

Son capturas del juego ejecutándose en Chrome; no se generaron ilustraciones
para simular resultados. Fueron guardadas sin editar su contenido.

## Límites de la verificación

No se probaron otros navegadores, lectores de pantalla reales ni dispositivos
físicos. La emulación de CPU no es una medición de FPS ni garantiza el rendimiento
en cualquier equipo. La revisión humana del estudiante, la exportación completa
del chat, la publicación del código y las dos iteraciones posteriores siguen
pendientes. No se generó el PDF condicional.
