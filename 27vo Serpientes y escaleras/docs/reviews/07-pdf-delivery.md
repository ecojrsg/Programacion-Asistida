# Comprobación de la entrega en PDF

Fecha: 2026-10-22, America/Mexico_City.

El usuario solicita el PDF y autoriza commit y push. No autoriza más cambios
del juego. Se guardó un manifiesto SHA256 de sus seis archivos de producto y
dos páginas de pruebas para comprobar que permanezcan idénticos.

## Fuentes y formato comprobados

- PDF 25 y 26 de `PDFs ejercicios`: carta, portada blanca, título centrado,
  datos del estudiante, materia, texto Helvetica y números de página.
- Nombre y matrícula copiados de esas portadas, no inventados.
- Consigna original y nueva copia adjunta a la solicitud del PDF.
- Registro nativo de esta conversación: exportados mensajes del usuario y del
  asistente, incluido el formulario y sus selecciones. Corte: petición del PDF
  inclusive. Se excluyen contexto interno y razonamiento privado.

El chat de desarrollo completo se conserva en
[UTF-8](../conversations/07-chat-crudo.txt) y
[JSONL](../conversations/07-chat-crudo.jsonl). Se conserva el texto, incluidos
errores ortográficos; los saltos tipográficos del PDF no cambian esos originales.
Los cierres redactados en archivos pero no enviados antes de una interrupción
no se agregan como si fueran mensajes realmente entregados.

## Estado de esta fase

El PDF quedó generado con 23 páginas y el formato de las referencias. Se
renderizaron y revisaron todas las páginas; una corrección de espacios al final
de los mensajes eliminó un encabezado de continuación innecesario. La última
versión se renderizó de nuevo: las páginas sin cambios conservaron sus imágenes
y se revisaron todas las páginas modificadas.

La aceptación «Perfecto» del usuario
se registra sobre el resultado observado del juego, no sobre cada Markdown.

## Resultados comprobados

- Ocho capturas, 56 enlaces y liga a cada uno de los 31 Markdown existentes.
- Numeración continua del 1 al 23, carta de 612 × 792 puntos y sin texto fuera
  de los márgenes comprobados. Portada con nombre, matrícula y materia de los
  documentos anteriores.
- Chat con 54 intervenciones: 12 del usuario y 42 del asistente, incluido el
  formulario. Corte: `2026-10-23T03:33:14.204Z`, solicitud del PDF inclusive.
- La extracción del chat del PDF coincide con el registro UTF-8 al ignorar
  únicamente los espacios y saltos tipográficos: 13401 caracteres no blancos
  en ambas fuentes. Se preservaron flechas y caracteres españoles.
- Los hashes SHA256 de los seis archivos de producto y las dos pruebas son
  idénticos a los guardados antes de preparar el PDF. No se modificó el juego.
- Código publicado en `20723eb8909e0b4dbe0e7852a2fa0c7021c3256a`; ruta de
  `index.html` verificada con gh. El árbol remoto contiene los documentos
  referenciados. El PDF y el cierre documental se publican en el commit de
  entrega posterior, conservando esa revisión fija para el código.
- El PDF declara los tres escenarios y la revisión humana completa pendientes.
  No se añadieron escenarios ni se inventó aprobación académica.

Los datos estructurados están en
[pdf-validation.json](../deliverable/pdf-validation.json). Las imágenes de
revisión son temporales y no forman parte del juego. La revisión del asistente
no equivale a la revisión humana; esa revisión del PDF y de los archivos queda
pendiente. No se repitieron pruebas del juego, pues esta fase solo documenta.

## Autorización de publicación pública

El primer intento de push fue rechazado por la revisión automática: el alcance
inicial mencionaba el código y el commit incluía también chat, capturas y datos
de portada. No se ejecutó ese intento. Se preguntó expresamente por publicar el
PDF, el chat completo, las capturas y todos los Markdown en un repositorio
público, indicando que el PDF incluye nombre y matrícula. El usuario respondió
«Sí, publicar todo el entregable». Esta respuesta autoriza la publicación de
ese contenido; no se interpreta como revisión académica de todos los archivos.
