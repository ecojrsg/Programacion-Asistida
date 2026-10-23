# Corrección: centrado y scroll según el espacio disponible

Fecha: 2026-10-22, America/Mexico_City.

## Petición y alcance

El usuario solicita corregir la adaptación al poner el juego en pantalla
completa: tamaño limitado, conjunto centrado y scroll únicamente cuando haga
falta. Se corrige el requisito de adaptación del diseño inicial aprobado;
no cambia la dirección visual, el flujo ni las reglas del juego.

La petición actual autoriza esta corrección. La revisión humana del resultado
permanece pendiente. No se registra como aprobación de una nueva propuesta de
diseño ni como la iteración con referencia visual del laboratorio.

## Diagnóstico anterior al cambio

La aplicación mantiene una altura de aproximadamente 1065 px porque el tablero
depende solo del ancho. Su borde superior permanece en 0 incluso cuando sobra
altura. A 1366 × 768 y 1440 × 900 hay scroll; a 2560 × 1440 queda mucho espacio
debajo en lugar de distribuirlo arriba y abajo. No hay un overflow:hidden que
eliminar ni una intervención necesaria en JavaScript.

## Plan de corrección

1. Centrar el contenedor con Flexbox y márgenes automáticos, usando como mínimo
   la altura dinámica del viewport. Conservar el crecimiento natural cuando
   el contenido no cabe.
2. Mantener el ancho máximo de 1056 px y adaptarlo también a la altura en
   escritorio, con un límite inferior que conserve legibles tablero y controles.
3. Reducir espacios verticales de escritorio de forma coherente; mantener los
   controles de 48 px y el diseño móvil existente.
4. Comprobar 1366 × 768, 1440 × 900, 1920 × 1080 y 2560 × 1440, además de móvil,
   reglas abiertas, mensajes de juego y ventanas bajas. Conservar capturas de
   antes y después, sin sobrescribir las de la fase inicial.

Cambios de producto limitados a CSS. No añadir dependencias, listeners de resize,
zoom global, fullscreen programático ni scroll bloqueado para ocultar contenido.
El resultado y las medidas se registrarán al terminar la verificación.

## Resultado y comprobaciones ejecutadas

Se cambió únicamente `styles.css`: centrado mediante Flexbox, ancho máximo
adaptado a la altura con `clamp()` y espacios de escritorio más compactos.
No se bloquearon los desbordamientos ni se cambiaron las reglas o JavaScript.

| Viewport en Chrome | Contenedor aproximado | Margen superior | Scroll vertical con reglas cerradas |
| --- | --- | --- | --- |
| 1366 × 768 | 804 × 743 px | 12 px | No. |
| 1440 × 900 | 936 × 856 px | 22 px | No. |
| 1920 × 1080 | 1056 × 976 px | 52 px | No. |
| 2560 × 1440 | 1056 × 976 px | 232 px | No. |
| 1024 × 600 | 800 × 734 px | 0 px | Sí, porque el contenido supera la altura. |

El centrado se comprobó calculando los puntos medios del contenedor y del
viewport. No hubo desbordamiento horizontal en los tamaños probados. En móvil
de 390 px se conserva el desplazamiento natural y el botón de 48 px.

En 1366 × 768, abrir las reglas elevó la altura de página a aproximadamente
924 px y activó el scroll. El borde superior quedó en 0, con todo el contenido
accesible. Al cerrarlas desapareció nuevamente la barra.

Se inició una partida, se lanzó un 3 y se comprobó el salto a 22. Al cambiar de
1366 × 768 a 1920 × 1080 se conservaron posición, turno y coordenadas de la ficha
(`13%`, `76.6%`). El juego siguió centrado y sin scroll en ambos tamaños.

### Capturas

- [Antes, 1366 × 768](../evidence/02-before-1366.jpg).
- [Después, 1366 × 768](../evidence/02-after-1366.jpg).
- [Después, 1920 × 1080](../evidence/02-after-1920.jpg).

Son capturas del navegador, sin modificar su contenido. Las capturas de la
versión inicial se conservan. No se añadieron pruebas unitarias ni se repitió
la batería de reglas porque la corrección afecta solamente CSS. Se verificaron
el diseño y una jugada de integración. No se probaron otros motores de navegador
ni dispositivos físicos. Revisión humana del resultado: **Pendiente**.

## Rectificación tras la captura del usuario

El usuario volvió a señalar que no estaba centrado. Las resoluciones de la tabla
se comprobaron mediante emulación, pero se dejó activa la de 1920 × 1080 al
terminar. El cierre anterior no comprobó que la página ocupara el área real de
la ventana de Chrome. No debe interpretarse esa tabla como una comprobación
de maximizado manual. El [diagnóstico posterior](03-browser-window.md) conserva
la captura del usuario, las medidas y la corrección de la sesión de pruebas.
