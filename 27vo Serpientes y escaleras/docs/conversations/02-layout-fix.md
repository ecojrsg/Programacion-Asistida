# Conversación: centrado y adaptación de pantalla

Fecha: 2026-10-22, America/Mexico_City.
Transcripción manual de los mensajes visibles disponibles. Continúa la
[implementación inicial](01-implementation.md); no es una exportación nativa.

## Usuario

Bien hagamos unos cambios, cuandonpongo el juego en pantalla completa no se adapta de manera correcta, no quiero que cubra toda mi pantalla pero si que este centrado y que el scroll desaparezca si no es necesario.

## Asistente

Revisaré el tamaño y la distribución en pantalla completa para centrar el juego, mantener un ancho limitado y mostrar el scroll solo cuando el contenido lo necesite.

## Asistente

Encontré la causa: el contenido mide unos 1065 px de alto, pero solo se adapta al ancho y queda pegado arriba. Ajustaré el tamaño y los espacios según la altura disponible, y centraré el conjunto con márgenes automáticos. El scroll seguirá disponible al abrir las reglas o usar una ventana pequeña.

## Asistente

El ajuste ya pasó las comprobaciones de tamaño: en 1366×768, 1440×900, 1920×1080 y 2560×1440 queda centrado y sin scroll. En móvil y ventanas bajas conserva el desplazamiento cuando el contenido no cabe. Ahora compruebo el caso de las reglas abiertas y guardo el antes y después.

## Resultados visibles de herramientas

El contenedor pasó de mantener unos 1065 px de alto a ajustar su tamaño con la
altura disponible. Las cuatro resoluciones de escritorio indicadas terminaron
sin barras. Abrir las reglas en 1366 × 768 produjo scroll real (página de unos
924 px), y cerrarlas lo eliminó. Una jugada hasta 22 conservó estado y posición
al redimensionar. Se guardaron las tres capturas enlazadas en el
[plan e informe](../plans/02-layout-fix.md).

## Asistente: cierre

Corregido: ahora queda centrado, conserva un tamaño limitado y adapta el tablero a la altura disponible. El scroll aparece únicamente cuando hace falta.

Verificado en Chrome en tamaños de escritorio y móvil, incluidas las reglas abiertas.

Recarga la pestaña para verlo; esto reinicia la partida. No probé otros navegadores.
