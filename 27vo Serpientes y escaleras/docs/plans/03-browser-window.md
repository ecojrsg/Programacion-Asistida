# Diagnóstico: ventana real y resolución de prueba

Fecha: 2026-10-22, America/Mexico_City.

## Alcance y actuación

El usuario informó «nuevamente no queda centrado, revisalo bien» y adjuntó una
[captura de la ventana](../evidence/03-user-window.png). La página terminaba
antes del borde derecho e inferior del navegador. Se revisó la configuración
de Chrome antes de modificar de nuevo la aplicación.

La actuación comunicada fue comparar ventana y viewport, retirar la emulación
y comprobar los márgenes. No se escribió código de la aplicación, por lo que
no se propuso ni implementó un nuevo diseño. Se conservaron las reglas y el
CSS aprobados para la adaptación inicial.

## Causa y resultado

La herramienta indicaba una emulación activa de 1920 × 1080. La ventana exterior
medía 3440 × 1392. Al retirar esa emulación, el área volvió inicialmente al
tamaño base de prueba de 1440 × 1000, todavía menor que la ventana. Por eso no
bastaba con que la herramienta informara que la emulación estaba desactivada.

Se ajustó la ventana de pruebas para que su viewport midiera 3424 × 1241 y se
retiró nuevamente la emulación explícita. La ventana exterior terminó en
3440 × 1392, coincidiendo con el área disponible de la pantalla. La diferencia
incluye el marco y los controles del navegador.

| Medición final | Resultado |
| --- | --- |
| Viewport | 3424 × 1241 px. |
| Contenedor `.app` | 1056 × 976 px. |
| Márgenes izquierdo y derecho | 1184 px cada uno. |
| Márgenes superior e inferior | 132.5 px cada uno. |
| Diferencia entre centros | 0 px en ambos ejes. |
| Desbordamiento horizontal o vertical | Ninguno, con reglas cerradas. |
| Estado de partida antes y después | `ready`, posiciones `[0, 0]`, cero tiradas. |
| Errores de consola | Ninguno registrado. |

No se recargó el juego ni se modificaron HTML, CSS o JavaScript. Se cerró una
pestaña vacía creada por una herramienta auxiliar. Un intento de abrir el archivo
en otra pestaña de Chrome fue bloqueado por la política de URLs de esa herramienta;
no se intentó sortear ese bloqueo. La comprobación y el ajuste continuaron
en la pestaña de pruebas que ya estaba abierta.

## Evidencia y límites

- [Captura proporcionada por el usuario](../evidence/03-user-window.png), copiada
  sin cambios; su SHA256 coincide con el original.
- [Viewport después del ajuste](../evidence/03-window-3424.jpg), captura real de
  Chrome sin editar, que muestra el contenedor centrado y el fondo completo.

La segunda captura muestra el contenido de la pestaña; no incluye el marco de
Windows ni la zona exterior del navegador. Se verificó el tamaño actual mediante
mediciones y captura. No se verificó un cambio de tamaño manual posterior ni
el maximizado con controles nativos. No se repitieron las pruebas de reglas,
ya que el juego no cambió. No se probaron otros navegadores.

La revisión humana posterior del resultado y de estos documentos permanece
**Pendiente**. Este diagnóstico corrige la verificación anterior y no se presenta
como una de las dos iteraciones de mejora exigidas por la consigna.
