# Skill camaleón: cartas del medievo

La skill adapta texto para personas al tono de una carta medieval: solemne,
cercano y reflexivo. La referencia a la carta de Ezio para su hermana orienta
el ambiente; los mensajes son originales.

## Entrega

- `.agents/skills/medieval-chameleon/SKILL.md`: instrucciones de la skill.
- `demo.before.mjs`: demostración original conservada para comparar.
- `demo.mjs`: resultado de aplicar la skill a comentarios y mensajes.

La demostración usa JavaScript y no necesita paquetes externos. La skill puede
trabajar con otros lenguajes respetando las instrucciones de cada proyecto.

## Cómo usarla

Abre esta carpeta como proyecto o menciona directamente el archivo de la skill
en el chat del agente. Por ejemplo:

> Usa la skill de `.agents/skills/medieval-chameleon/SKILL.md` para dar un tono
> de carta medieval a los comentarios y mensajes de `demo.mjs`. Conserva el
> idioma de cada texto y verifica que el código permanezca intacto. Trabaja
> únicamente dentro de este ejercicio.

Si el agente la muestra entre las skills disponibles, también puedes invocarla
con `$medieval-chameleon`. No se ha instalado fuera de este ejercicio.

## Ver la demostración

Desde esta carpeta, con Node.js disponible:

```sh
node demo.before.mjs
node demo.mjs
git diff --no-index -- demo.before.mjs demo.mjs
```

El último comando devuelve el código de salida 1 cuando hay diferencias; en
este caso permite revisar las cuatro sustituciones de texto esperadas.

Salida original:

```text
Proceso iniciado.
Total: 25
```

Salida medieval:

```text
Doy comienzo a esta jornada.
Que conste en esta crónica el total: 25
```

El comentario conserva el inglés de su versión original y adopta el mismo tono.
El mensaje de error también fue adaptado, aunque no aparece en la ejecución
normal del ejemplo.

## Verificación realizada

Se verificaron con Node.js el nombre, los dos campos del encabezado YAML y la
ausencia de marcadores pendientes en la skill. El validador oficial
`quick_validate.py` no pudo ejecutarse por falta de `PyYAML`; no se instalaron
dependencias para suplirlo.

Se comprobó la sintaxis de ambos archivos con `node --check`. Se compararon
ambos contenidos revirtiendo en memoria las cuatro sustituciones permitidas:
todo el contenido restante resultó idéntico, incluida la expresión `${total}`.

También se ejecutaron ambas versiones en un entorno aislado de Node.js y se
simularon en memoria las ramas de éxito y error. Se conservaron el total `25`,
los datos exportados, la ruta `./records/journey.json`, los valores de estado
y la cantidad de mensajes de cada tipo. Solo cambió el texto previsto.

Si una ejecución futura modifica código, la skill indica deshacer sus propios
cambios con `/undo` cuando esté disponible, o restaurarlos desde el original
retenido. Después se debe mejorar la skill antes de repetir la transformación;
no se debe corregir el programa para ocultar el fallo.
