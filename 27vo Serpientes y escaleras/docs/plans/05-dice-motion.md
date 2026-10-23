# Refinamiento: lanzamiento del dado

Fecha: 2026-10-22, America/Mexico_City.

## Petición y alcance

El usuario considera que la animación del dado dura muy poco y se siente poco
natural. Solicita revisarla después de aceptar la distribución anterior con
«Super bien». Se mantiene el juego con HTML, CSS y JavaScript puros y los
efectos en archivos independientes.

El cambio se limita al lanzamiento: no cambia probabilidades, reglas, diseño
del tablero ni distribución general. La petición actual autoriza esta mejora
concreta; la revisión humana del resultado y los documentos queda pendiente.

## Diagnóstico anterior a la implementación

`Visuals.play()` gira el dado durante 450 ms entre solo dos transformaciones,
sin elevación ni rebote. Ambos ejes hacen el mismo giro. El controlador
interrumpe toda la presentación después de 1600 ms, un límite que cortaría el
movimiento de las fichas si solo se prolongara el giro.

## Plan comunicado antes de escribir código

1. Ampliar el giro a 1250 ms y utilizar keyframes nativos para elevación,
   caída, rebote pequeño y asentamiento. Dar ritmos distintos a los ejes,
   manteniendo la cara final correcta y continua con la siguiente tirada.
2. Conservar los efectos en `visuals/effects.js`. Reservar en
   `visuals/effects.css` espacio local para que el dado no toque jugadores ni
   resultado mientras gira; mantener el diseño móvil. En escritorio bajo,
   reducir ligeramente el dado y la reserva para conservar el ajuste sin scroll.
3. Ampliar a 3000 ms el límite de recuperación de `script.js`: el máximo
   previsto es 1250 ms de dado + 940 ms de ficha = 2190 ms. Conservar el bloqueo
   de acciones concurrentes y la recuperación ante fallo de los efectos.
4. Respetar movimiento reducido y cancelación. Comprobar seis resultados,
   tiradas consecutivas, una escalera con seis pasos, doble clic, cancelación,
   errores y movimiento reducido; revisar el espacio en escritorio y móvil.
5. Guardar las evidencias, la conversación, este plan y el cierre literal.

Se consultaron las pautas de HyperFrames y su adaptador WAAPI para el movimiento
nativo. Este entregable sigue siendo un juego interactivo; no se crea una
composición de vídeo ni se instala un runtime. No se utilizará un motor físico.

La sesión sigue en modo de ejecución; no hay una herramienta disponible para
cambiarla a modo Plan. Este plan se guarda antes de modificar código. No se
registra una aprobación posterior del documento que todavía no ocurrió.

## Implementación y verificación

La animación tiene seis keyframes y dura 1250 ms: lanzamiento con elevación de
12 px, caída, rebote de 4 px y asentamiento. El giro pierde energía al final;
los ejes recorren dos y tres vueltas respectivamente. La cara final coincide
con el resultado y con la siguiente tirada. Las fichas conservan su animación.

El helper existente admite ahora elegir el easing, manteniendo el anterior
para las fichas. Se comprueba la generación antes de escribir la pose final:
un giro cancelado ya no puede sobrescribir el reinicio. El límite de
recuperación del controlador pasó de 1600 a 3000 ms.

Se reservan 144 px para el dado en escritorio y 120 en móvil. La primera
verificación encontró que esa reserva añadía scroll en 1366 × 768. Se corrigió
con una reserva de 116 px y escala visual de 0.9 solo en escritorio de hasta
800 px de alto. El juego volvió a caber sin barras, con 767.16 px de contenido.

### Comprobaciones ejecutadas en Chrome

- Se creó [tests/motion.html](../../tests/motion.html), una comprobación sin
  dependencias. Se ejecutó su función `checkMotion()` sobre el dado real de la
  pestaña abierta: **23 comprobaciones aprobadas** en modo normal, otras 23
  con movimiento reducido y otras 23 en escritorio compacto. La función es la
  misma que utiliza la página de pruebas; no se abrió esta última como pestaña.
- Cubre las seis caras, un resultado repetido, duración perceptible o ausencia
  de giro según preferencias, reposo sin salto visual, reinicio durante un giro
  y ausencia de animaciones del dado pendientes.
- Una tirada real de seis pasos desde 2 hasta la escalera de 8 a 30 terminó en
  **2199 ms**. Durante la presentación ambos botones estaban bloqueados. Una
  segunda acción simultánea no añadió un turno. La ficha terminó en 30.
- Un efecto deliberadamente detenido se recuperó en **3008 ms**, completó el
  turno y habilitó los controles. Un error visual provocado también completó
  el turno, con posición 1 y modo de respaldo; generó el aviso esperado.
- Con movimiento reducido, una tirada terminó sin giro ni animaciones del
  dado y conservó resultado, turno y controles disponibles.
- No hubo mensajes de error en consola. Las pruebas restauraron estado,
  contenido y pose de la pestaña inicial; no se dejó emulación activa.

### Espacio durante el giro

Se muestrearon las seis caras cada 25 ms del giro: 300 estados por tamaño,
usando los límites de las caras reales transformadas. La separación mínima
respecto al bloque anterior y al resultado fue positiva en todos los casos.

| Viewport | Separación mínima arriba | Separación mínima abajo | Scroll horizontal |
| --- | --- | --- | --- |
| Ventana de escritorio durante la prueba: 1718 × 1304 | 11.47 px. | 18.99 px. | No. |
| Escritorio compacto emulado: 1366 × 768 | 4.72 px. | 10.99 px. | No. |
| Móvil emulado: 390 × 844 | 25.81 px. | 23.94 px. | No. |

El escritorio compacto no tiene scroll vertical con reglas cerradas. En móvil
se conserva el desplazamiento necesario para el contenido. No se cambiaron
el centrado horizontal, la alineación superior ni la separación de la leyenda.

### Evidencias y límites

- [Dado en vuelo, a 437.5 ms](../evidence/05-dice-airborne.jpg).
- [Dado asentado con resultado 6](../evidence/05-dice-settled.jpg).

Son capturas reales del panel con la animación aislada pausada y finalizada
para comparar poses. No representan una tirada completa: el estado y el
marcador se conservaron en la salida. Las capturas estáticas no demuestran
fluidez; la secuencia completa sí se ejecutó en la prueba de integración.

No se añadió un motor físico ni una biblioteca: el movimiento es una simulación
visual ligera con Web Animations API. No se repitió la batería de reglas porque
estas no cambiaron. No se probaron otros navegadores ni móviles físicos. La
naturalidad percibida y la revisión humana del código y evidencias quedan
pendientes de la respuesta real del estudiante.
