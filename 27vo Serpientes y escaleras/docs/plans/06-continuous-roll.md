# Corrección: giro continuo y resultado sincronizado

Fecha: 2026-10-22, America/Mexico_City.

## Petición y diagnóstico previo

El usuario señala aceleraciones, pausas y nuevos giros dentro del lanzamiento,
y observa que el resultado numérico se muestra antes de que termine el dado.
La mejora anterior no satisfizo su valoración de fluidez. Se corrige ese
comportamiento conservando duración, cara final, reglas y distribución.

La rotación anterior tiene un easing distinto en cada keyframe. Cada tramo
puede terminar con velocidad casi nula y el siguiente volver a acelerar.
Además, `playTurn()` escribe el resultado antes de llamar a la capa visual.

## Plan comunicado antes de implementar

1. Simplificar el giro a una única interpolación de 1250 ms y una curva de
   desaceleración continua; eliminar los cambios de velocidad por tramos.
2. Mostrar «…» durante el giro. Añadir un callback opcional de dado asentado
   a `Visuals.play()` para que el controlador revele el resultado antes de la
   animación de la ficha. La capa visual no escribe el marcador.
3. Mantener el resultado en el cierre del turno como respaldo ante efectos
   ausentes, fallidos o agotados; conservar movimiento reducido y cancelación.
4. Extender la prueba existente para verificar ocultación, revelación única
   y ausencia de revelación después de cancelar. Revisar continuidad de giro,
   integración, repetición de resultados y movimiento reducido.
5. Conservar estado de la partida al actualizar la pestaña y documentar los
   resultados reales y la revisión humana pendiente.

Archivos de producto: `visuals/effects.js` y `script.js`. Prueba afectada:
`tests/motion.html`. No se necesita modificar CSS, instalar librerías ni
añadir un sistema de eventos.

La petición actual autoriza esta corrección concreta. La sesión sigue en
modo de ejecución sin herramienta para cambiar a Plan; se guarda el plan
antes de escribir código. No se inventa una aprobación posterior del documento.

## Resultado y verificación

La rotación usa ahora dos keyframes y una sola curva
`cubic-bezier(0.25, 0.4, 0.55, 1)` durante los 1250 ms completos. Se eliminaron
las elevaciones, rebotes y easings por tramo que interrumpían el ritmo. Se
mantiene una lista de transformaciones compatible entre tiradas para interpolar
las vueltas completas sin saltos de pose.

`Visuals.play()` recibe un callback opcional `onRolled`. Lo invoca una sola vez
después de comprobar la cancelación y fijar la pose final, antes de mover la
ficha. El controlador muestra «…» mientras gira y escribe el número al recibir
ese aviso. El cierre del turno conserva una asignación de respaldo para efectos
ausentes, errores o tiempo agotado. Movimiento reducido revela el número de
inmediato, con la cara correcta y sin giro.

### Pruebas ejecutadas

- [tests/motion.html](../../tests/motion.html) amplía la comprobación existente:
  **39 comprobaciones aprobadas** en escritorio, 39 en móvil emulado de 390 px
  y 38 con movimiento reducido. En este último caso se omite el muestreo de
  continuidad porque no existe giro.
- La nueva comprobación de continuidad muestrea la rotación real cada 20 ms
  hasta 1100 ms. Exige avance angular y cambios de velocidad inferiores al 20%
  entre muestras consecutivas; detecta pausas y reinicios en el tramo interior.
  No evalúa los últimos 150 ms, donde detenerse es el resultado esperado.
- Se comprobaron las seis caras, resultado repetido, ocultación durante el giro,
  revelación única con la cara correcta, reposo sin salto y cancelación sin
  revelar el resultado de un giro interrumpido.
- En una tirada completa de seis pasos y escalera, el marcador mostraba «…»
  al inicio y a los 500 ms. Un observador del DOM registró la primera aparición
  de «6» a los **1257 ms**. A los 1300 ms, el marcador ya era «6» y la ficha
  seguía moviéndose; la jugada terminó en 30 a los **2202 ms**. La segunda
  acción simultánea no añadió un turno.
- Sin capa visual y con un error provocado, el resultado final se mostró y
  los controles se habilitaron. Un efecto detenido se recuperó a los **3004 ms**
  y mostró el resultado. Con movimiento reducido también coincidieron cara,
  número y posición final.
- En 1366 × 768 se conservó la ausencia de scroll. Durante el giro, el dado
  mantuvo al menos 13.73 px respecto al bloque superior y 8.81 px respecto al
  marcador. No se modificó CSS ni la distribución.

Se ejecutó la función de comprobación de la página de pruebas en el dado real
de la pestaña existente. No se abrió el HTML de pruebas como pestaña nueva.
Se verificaron la sintaxis de JavaScript y los enlaces locales del entregable.

### Capturas y conservación de partida

- [Durante el giro, marcador oculto](../evidence/06-dice-rolling.jpg): muestra
  real pausada a 600 ms, con «…» y controles bloqueados.
- [Tirada completa, resultado revelado](../evidence/06-dice-result.jpg): cara 6,
  número 6 y ficha en 30 después de una tirada ejecutada sin pausa.

Al pausar para la primera captura se alcanzó el límite de recuperación. Por
ello un intento de finalizar después esa animación ya cancelada no encontró
una animación activa. Se descartó ese estado como evidencia del asentamiento
y se capturó una tirada completa adicional sin pausa, con la cara comprobada.

Antes de actualizar la pestaña se guardó la partida: posiciones `[32, 38]`,
ocho tiradas y turno de Jugador 1. Algunas emulaciones móviles recargan la
página; después de terminar todas las pruebas se restauraron esa partida,
su número anterior, mensaje, pose, reglas y desplazamiento. No se dejó emulación
activa. La captura de ejemplo utiliza una partida de prueba distinta.

No se añadieron dependencias ni se modificaron las reglas. Las imágenes estáticas
no prueban fluidez perceptiva. La continuidad se comprobó mediante muestreo y
se ejecutaron tiradas completas, pero la valoración del usuario sigue pendiente.
No se probaron otros navegadores ni móviles físicos. Código, prueba, documentos
y capturas permanecen pendientes de revisión humana posterior.
