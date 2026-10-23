# Conversación: giro continuo y resultado sincronizado

Fecha: 2026-10-22, America/Mexico_City.
Transcripción manual de mensajes visibles; no es una exportación nativa.
Continúa la [primera revisión del dado](05-dice-motion.md).

## Usuario

Aun la animación no es muy fluida, derrepenete va rapido, luego parece que se detiene luego vuelve a girar un poco, hazla mas fluida y es muy raro que el resultado de abajo ya diga el numero que tocara antes del dado

## Asistente

Revisaré las pausas del giro y haré que el número aparezca cuando el dado termine de asentarse.

## Asistente

Las pausas vienen de aplicar una curva de velocidad distinta en cada tramo: el giro frena y vuelve a acelerar. Lo cambiaré por un giro continuo con desaceleración al final. Abajo mostraré «…» mientras gira y el número al asentarse, antes de mover la ficha.

## Asistente

La prueba confirma que el marcador sigue en «…» a los 500 ms y revela el número al asentarse el dado, alrededor de los 1.25 segundos. El giro también pasó la comprobación de continuidad entre fotogramas. Conservé tu partida para que puedas probar el cambio.

## Resultados visibles de herramientas

Las comprobaciones aprobaron 39 casos en escritorio y móvil, y 38 con movimiento
reducido. El resultado se reveló a los 1257 ms en una tirada que terminó a los
2202 ms. Se probaron efectos ausentes, error y límite de recuperación. Se
conservaron capturas del marcador oculto y del resultado con cara 6; un estado
de captura interrumpido por el límite de seguridad se descartó. La partida
del usuario se restauró después de las pruebas. El
[informe](../plans/06-continuous-roll.md) conserva las medidas y limitaciones.

## Asistente: cierre

Corregí ambos puntos: el dado gira de forma continua, sin pausas entre tramos, y el resultado muestra «…» hasta que se asienta. Después aparece el número y se mueve la ficha.

Probado en Chrome, con tu partida conservada. No probé otros navegadores.
