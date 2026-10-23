# Fase 1: juego inicial y evidencias del laboratorio

Fecha: 2026-10-22, America/Mexico_City.
Estado: aprobado para implementación por el usuario el 2026-10-22 mediante
«Hazlo implementalo». Esta aprobación corresponde al plan; no sustituye la
revisión posterior del código y las evidencias generadas.

## Objetivo y decisiones confirmadas

Crear una primera versión completa de serpientes y escaleras, llamativa y fluida,
con código que un estudiante pueda leer y explicar. El usuario confirmó dos
jugadores locales, un diorama colorido y efectos en archivos separados, aplicados
directamente al juego. No se añadirá una galería o escena independiente.

Esta fase comprende preparación documental, diseño, implementación inicial,
comprobaciones y capturas. La mejora con referencia visual y la selección de
tres escenarios pertenecen a las dos iteraciones posteriores. No se anticiparán
esas funciones ni se presentarán como mejoras ya realizadas.

La instrucción 3 original dice «Genera el diseño de la aplicación en modo Build».
Por indicación del estudiante, se considera un error y se utiliza Plan antes de
implementar. La revisión de este documento debe registrarse antes de escribir
código de la aplicación.

## Experiencia y reglas propuestas

- Tablero fijo de 10 por 10, numerado del 1 al 100 en recorrido serpenteante:
  1 abajo a la izquierda, 10 abajo a la derecha, 11 sobre 10 y 100 arriba a la
  izquierda. Dos fichas empiezan fuera del tablero, en la posición 0.
- Los jugadores se llaman «Jugador 1» y «Jugador 2». Juega primero el 1. No se
  requieren nombres, cuentas, selección de jugadores ni rival automático.
- «Comenzar partida» activa el primer turno. «Lanzar dado» produce una tirada
  de 1 a 6 y mueve únicamente la ficha del jugador activo. Sacar 6 no repite turno.
- Al caer en el inicio de una escalera se sube; al caer en una cabeza de serpiente
  se baja. Se aplica un solo salto por tirada. Pasar por una casilla especial
  sin caer en ella no activa su efecto.
- Para ganar hay que llegar exactamente a 100. Una tirada que sobrepase la meta
  deja la ficha en su lugar y consume el turno. Las fichas pueden compartir una
  casilla; se dibujan desplazadas entre sí para que ambas sean visibles.
- El turno termina después del movimiento y su posible salto. Mientras se anima
  una tirada se desactivan lanzamiento y reinicio para evitar acciones simultáneas.
- Al ganar, se anuncia al ganador y se bloquean nuevas tiradas. «Nueva partida»
  restaura posiciones, turno, dado y mensajes. Si hay una partida en curso, pide
  confirmación mediante el diálogo nativo del navegador antes de borrarla.
- Muestra siempre el jugador activo, ambas posiciones, el dado y el resultado
  de la última jugada. Las reglas breves estarán disponibles en un desplegable
  HTML nativo, sin introducir un sistema de ventanas.

Mapa inicial propuesto; es la única fuente tanto para reglas como para dibujos:

| Escaleras | Serpientes |
| --- | --- |
| 3 → 22 | 27 → 5 |
| 8 → 30 | 43 → 18 |
| 20 → 41 | 54 → 31 |
| 28 → 55 | 66 → 45 |
| 58 → 77 | 89 → 53 |
| 75 → 94 | 97 → 72 |

Ningún destino coincide con el inicio de otro salto. Esto evita cadenas y ciclos
sin agregar reglas o recorridos recursivos.

## Diseño y movimiento

La página se percibe como un juego de mesa de juguete, con una base sólida,
casillas ligeramente elevadas, fichas con volumen y un dado de seis caras.
El tablero es el protagonista desde la primera pantalla, acompañado del control
del turno. No habrá una cabecera promocional grande que desplace la partida.

- Escritorio: tablero a la izquierda, jugadores y dado a la derecha. En móvil:
  turno y posiciones, tablero y controles en una sola columna; el botón de
  lanzamiento queda próximo al tablero.
- Fondo crema, texto verde muy oscuro y acentos coral, turquesa y amarillo.
  Usa fuentes del sistema, superficies mates, bordes suaves y sombras cortas;
  las piezas se distinguen por número y marca además del color.
- Perspectiva leve en la base del tablero en pantallas amplias; se reduce en
  móvil para mantener legibles las 100 casillas. La inclinación se aplica al
  conjunto para que fichas, números y conexiones permanezcan alineados.
- Serpientes y escaleras mediante SVG nativo, con sombra y detalle suficiente
  para reconocer cabeza, cola, largueros y peldaños. Sus extremos se calculan
  a partir de los mismos números usados por las reglas.
- Dado: giro corto de unos 450 ms hasta la cara que corresponda al resultado
  real. Ficha: avance por casilla de unos 90 ms; salto especial de unos 400 ms.
  La secuencia completa dura menos de 1.5 segundos en condiciones normales.
- Respuesta de botones de unos 150 ms y una celebración breve al ganar. No se
  incorporan vídeo, sonido, partículas continuas ni animaciones permanentes.
- Con `prefers-reduced-motion`, muestra directamente los estados finales.
  No se mueve la partida por pasar el ratón ni por cambiar el tamaño de pantalla.

Anatomy aporta los criterios de volumen, piezas reconocibles, sombras y movimiento
suave, adaptados al requisito del usuario de mantener poco código. No se copiará
su motor geométrico ni se impondrá una cantidad artificial de piezas. HyperFrames
se evaluó como herramienta orientada a vídeo y no se incorporará a esta versión.
Se usarán CSS 3D, SVG y animaciones nativas; no hace falta una biblioteca externa
ni un paso de compilación para obtener este resultado.

## Organización e integración

El juego abrirá directamente desde `index.html`, sin instalaciones, servidor o
conexión de red. Los scripts serán clásicos con `defer`, sin imports ni `fetch`
que obliguen a servir el ejercicio por HTTP.

| Parte | Responsabilidad |
| --- | --- |
| HTML y CSS principal | Estructura semántica, distribución, tablero legible y controles. |
| `game.js` | Datos del tablero y funciones de reglas, sin DOM, animaciones ni azar interno. |
| `script.js` | Estado de partida, tirada aleatoria, eventos y actualización de interfaz. |
| `visuals/` | `effects.css` y `effects.js`: relieve, SVG y animaciones, sin decidir reglas. |
| `tests/rules.html` | Comprobación ejecutable en navegador mediante aserciones, sin framework. |

La lógica recibe la tirada como argumento para poder probar resultados concretos.
Las posiciones, jugador activo y fase de la partida constituyen el estado mínimo.
No se añadirá un motor, bus de eventos, jerarquía de clases o configuración futura.

La capa visual recibe el recorrido y el resultado ya calculados. No cambia turno,
posición ni ganador. La aplicación debe finalizar cada jugada aun cuando los
efectos estén desactivados o fallen; usa una integración pequeña con finalización
garantizada y duración acotada. La presentación básica debe seguir mostrando
posiciones, cambios especiales y mensajes sin depender de esa capa.

Los SVG son decorativos; la información necesaria para jugar está en HTML y en
mensajes accesibles. Los cambios de turno, saltos y victoria se anuncian una vez
por evento mediante una región `aria-live`, nunca por fotograma. Los botones usan
semántica nativa y foco visible. No se convierten las 100 casillas en 100 paradas
de tabulación porque no son controles.

## Orden de implementación y evidencias

1. Registrar la revisión del plan y sus correcciones reales. Mantener en pendiente
   cualquier apartado que el usuario no haya revisado.
2. Crear y revisar los tres archivos de buenas prácticas en las rutas indicadas
   por `AGENTS.md`. Conservar consigna, chat y decisiones sin inventar historial.
3. Implementar las reglas y la comprobación determinista. Después, montar el
   tablero HTML y los controles hasta completar una partida sin adornos.
4. Integrar el diorama y las transiciones desde `visuals/`, manteniendo la misma
   fuente de datos y comprobando que el juego funciona sin esos efectos.
5. Verificar escritorio, móvil, teclado y movimiento reducido; corregir los
   problemas observados y conservar capturas reales de esta versión inicial.
6. Crear el README del laboratorio con objetivo, decisiones, etapas, criterios,
   enlaces a cada Markdown y nota explícita Build → Plan. La URL del código solo
   se publica como enlace cuando exista una dirección real.
7. Guardar el texto final literal de la ejecución que escriba código en
   `docs/results/`, mantener el chat en `docs/conversations/` y actualizar la
   matriz de revisión. Pedir después la mejora con su imagen para la iteración 1.

Los planes, resultados y capturas usarán el prefijo de fase `01` para la ejecución
inicial y conservarán los archivos de planificación `00`. Las evidencias finales
deberán mostrar la partida inicial, un salto especial y la victoria, además de
la vista móvil. El PDF es condicional a no mostrar el trabajo terminado en clase;
no forma parte de esta implementación inicial.

## Comprobaciones y aceptación

- Reglas: inicio en 0, tiradas de los extremos 1 y 6, alternancia de dos jugadores,
  salto de escalera, salto de serpiente, no activar saltos al pasar, llegada exacta,
  exceso sobre 100, victoria y reinicio completo. La lógica no acepta tiradas
  fuera de 1–6 ni movimientos en una partida terminada.
- Datos: orígenes únicos, destinos dentro del tablero, escaleras ascendentes,
  serpientes descendentes y ausencia de cadenas o ciclos en este mapa.
- Integración: doble clic en lanzar produce una sola tirada; botones bloqueados
  durante la transición; el dado muestra la tirada utilizada y la ficha termina
  en la posición informada; dos fichas en la misma casilla siguen visibles.
- Resiliencia: partida jugable sin efectos, movimiento reducido sin esperas
  artificiales y reinicio cancelado sin pérdida de la partida en curso.
- Presentación: escritorio de 1440 px y móvil de 390 px, sin desbordamiento
  horizontal, números legibles y controles de al menos 44 px. Comprobar además
  que el tablero se adapta a 320 px sin recortes.
- Accesibilidad: iniciar, lanzar y reiniciar con teclado; foco visible, estado
  comprensible sin depender del color y anuncios de turno y ganador.
- Rendimiento: usar principalmente transformaciones y opacidad; sin bucle de
  animación en reposo. Confirmar ausencia de errores de consola y revisar las
  transiciones con limitación de CPU. No prometer FPS sin medirlos.
- Entregable: archivos de buenas prácticas consultados, enlaces locales válidos,
  planificación anterior al código, capturas auténticas y matriz de revisión que
  diferencie comprobación técnica de revisión humana.

Al redactar este plan todavía no había código ni pruebas ejecutadas. Los
resultados de implementación se conservarán por separado en `docs/results/`.
