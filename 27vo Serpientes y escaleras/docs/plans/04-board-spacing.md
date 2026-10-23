# Corrección: separación del tablero y alineación superior

Fecha: 2026-10-22, America/Mexico_City.

## Petición y autorización

El usuario adjunta una captura del juego y solicita revisar los elementos
tapados, como la escalera, y dejar de centrar verticalmente la página. Su
petición corrige expresamente la distribución anterior. Se mantiene el
centrado horizontal y la identidad visual existente; no se propone una nueva
dirección de diseño. La revisión humana del resultado sigue pendiente.

## Diagnóstico antes de modificar código

El tablero utiliza `rotateX(9deg) rotateZ(-1.5deg)` y una sombra para simular
relieve. Las transformaciones no reservan espacio en el flujo del documento.
En el navegador actual, el borde pintado del tablero termina en 1003.72 px,
pero la leyenda comienza en 1001.5 px: se superponen unos 2.22 px, además de
la sombra. La leyenda de la escalera queda parcialmente tapada.

El centrado vertical procede de `body { display: flex }` y de los márgenes
automáticos en ambos ejes de `.app`. El usuario indica que ya no lo necesita.

## Plan comunicado antes de implementar

1. Dejar `body` en flujo normal y utilizar `margin: 0 auto` en `.app`,
   conservando el ancho máximo y el margen interior superior existente.
2. Reservar espacio inferior para el tablero inclinado en `visuals/effects.css`.
   Mantener el espaciado móvil, donde el tablero no tiene inclinación.
3. Verificar la leyenda completa, la separación respecto a reglas y controles,
   el centrado horizontal y el inicio superior en escritorio ancho, escritorio
   compacto y móvil. Mantener scroll natural cuando el contenido no quepa.
4. Guardar la captura del usuario y nuevas capturas, registrar medidas reales
   y conservar la conversación y el cierre literal.

La sesión está en modo de ejecución y no dispone de un cambio de modo Plan
desde estas herramientas. Se guarda este plan antes de tocar el código de la
aplicación. La petición actual autoriza la corrección concreta; no se inventa
una aprobación posterior de este documento.

Archivos de producto afectados: `styles.css` y `visuals/effects.css`. No hace
falta cambiar HTML, JavaScript, reglas, dependencias ni añadir nuevos efectos.

## Resultado y comprobaciones

Se retiró Flexbox de `body` y se cambió el margen de `.app` a `0 auto`.
La posición vertical comienza ahora en 0, con los 12 px interiores superiores
de escritorio y 22 px de móvil que ya existían. El centrado horizontal se
conserva. En los efectos se reservan 40 px inferiores para el tablero inclinado;
en móvil se mantienen los 20 px y el tablero sin inclinación.

| Viewport en Chrome | Posición superior de `.app` | Separación entre tablero y leyenda | Scroll horizontal / vertical con reglas cerradas |
| --- | --- | --- | --- |
| Ventana actual: 3440 × 1305 | 0 px. | 22.25 px. | No / No. |
| 1074 × 1042, emulado | 0 px. | 22.25 px. | No / No. |
| 1366 × 768, emulado | 0 px. | 32.21 px. | No / No. |
| 390 × 844, móvil emulado | 0 px. | 20 px. | No / Sí, contenido de 1053 px. |
| 320 × 700, móvil emulado | 0 px. | 20 px. | No / Sí, contenido de 1064 px. |

El error de centrado horizontal fue 0 en todos esos casos. Los controles
mantuvieron 48 px de alto. Se inspeccionaron capturas de escritorio y móvil:
los iconos de la leyenda quedan completos, fuera del tablero y de su sombra.
En escritorio hay otros 16 px entre la leyenda y las reglas. A 320 px la
leyenda se distribuye en dos líneas sin desbordarse.

Abrir las reglas a 1366 × 768 elevó la altura de página a 928 px y habilitó
scroll; cerrarlas lo eliminó. `.app` siguió en 0. Se restauró la ventana real
de 3440 × 1305 al terminar y la herramienta no dejó emulación activa.

Se actualizaron las hojas de estilo de la pestaña sin recargar el documento.
La partida conservó su estado (`ready`, posiciones `[0, 0]`, cero tiradas).
No se registraron errores de consola. El análisis mecánico de distribución
de Impeccable devolvió `[]`, sin hallazgos, antes y después del cambio.

### Evidencias y límites

- [Captura del usuario](../evidence/04-user-spacing.png), copia sin cambios y
  con SHA256 igual al original.
- [Escritorio después, 1074 × 1042](../evidence/04-desktop-spacing.jpg).
- [Móvil después, 390 px](../evidence/04-mobile-spacing.jpg), página completa.

No se añadieron pruebas unitarias ni se repitieron las reglas, porque el cambio
es de CSS. Las pruebas móviles fueron emuladas; no se probaron dispositivos
físicos ni otros motores. El ajuste no altera los cruces dibujados entre
serpientes y escaleras dentro del tablero. La revisión humana posterior del
código, documentos y capturas permanece **Pendiente**.
