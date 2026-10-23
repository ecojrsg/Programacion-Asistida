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

Preparación terminada. La publicación de la revisión del código, generación,
renderizado y validación final del PDF se registrarán aquí tras ejecutarse.
El documento debe señalar que los tres escenarios y la revisión humana de
todos los archivos siguen pendientes. La aceptación «Perfecto» del usuario
se registra sobre el resultado observado del juego, no sobre cada Markdown.

## Autorización de publicación pública

El primer intento de push fue rechazado por la revisión automática: el alcance
inicial mencionaba el código y el commit incluía también chat, capturas y datos
de portada. No se ejecutó ese intento. Se preguntó expresamente por publicar el
PDF, el chat completo, las capturas y todos los Markdown en un repositorio
público, indicando que el PDF incluye nombre y matrícula. El usuario respondió
«Sí, publicar todo el entregable». Esta respuesta autoriza la publicación de
ese contenido; no se interpreta como revisión académica de todos los archivos.
