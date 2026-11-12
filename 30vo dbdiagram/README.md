# 30. dbdiagram - Biblioteca

Jonathan Serna | Ingeniería en Software | Programación Asistida por Inteligencia Artificial

## Entrega

- [Reporte PDF](Ejercicio_30_dbdiagram.pdf): portada, explicación del ejercicio, resultado completo y resultado del MVP. Se conserva una copia idéntica en `../PDFs ejercicios/Ejercicio_30_dbdiagram.pdf`.
- [Modelo completo](dbdiagram.dbml): tabla `libros` con 17 campos, índices y restricciones. Conserva la propuesta de la conversación.
- [Modelo MVP](mvp_dbdiagram.io.dbml): tabla `libros` con exactamente `id`, `titulo`, `autor`, `año` y `disponible`.
- [Enlaces y validación](diagramas.json).
- `capturas/`: evidencia real del editor de dbdiagram.io para ambas versiones.

## Diagramas guardados

- [dbdiagram](https://dbdiagram.io/d/dbdiagram-6af5ff55dec310ec25f387c8).
- [mvp_dbdiagram.io](https://dbdiagram.io/d/mvp_dbdiagram-io-6af5ffad4fa75117f6758022).

Ambos se guardaron como privados en la cuenta del usuario. Para abrir los enlaces es necesario iniciar sesión con esa cuenta. Los archivos DBML también pueden pegarse en un diagrama nuevo.

## Interpretación y límites

En el modelo completo una fila representa una edición. Los ejemplares disponibles no pueden ser negativos ni superar el total. El ISBN es opcional y único cuando existe; su restricción comprueba la longitud, no el dígito de control.

En el MVP `disponible` es un booleano obligatorio, con valor inicial `true`; no representa una cantidad de copias. El título y autor no pueden estar vacíos y el año debe ser positivo. Ambos diseños usan un solo autor por registro y no incluyen préstamos ni lectores.

## Verificación

Se comprobó la visualización de ambos diagramas y su indicador de guardado en dbdiagram.io. El generador del PDF comprueba 17 campos en el completo, los cinco nombres exactos en el MVP y las tres páginas del reporte. El PDF se renderizó para revisar visualmente sus páginas. No se ejecutó SQL ni se construyó una aplicación de biblioteca.

`build_report.mjs` reproduce el PDF con las bibliotecas incluidas en el runtime de escritorio de Codex usado para esta entrega; sus rutas son específicas de ese entorno. No requiere instalar dependencias en este ejercicio.

Referencia de sintaxis: [documentación oficial de DBML](https://dbml.dbdiagram.io/docs/).
