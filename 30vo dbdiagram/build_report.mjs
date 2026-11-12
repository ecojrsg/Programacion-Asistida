import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

// Use the desktop's bundled libraries; no project installation is needed.
const runtime = 'file:///C:/Program%20Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1111-570-0_26.1111.570.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules/';
const require = createRequire(new URL(runtime + 'pdf-lib/package.json'));
const { PDFDocument, StandardFonts, rgb, PDFName, PDFString } = require('pdf-lib');
const sharp = require('sharp');
const root = path.dirname(fileURLToPath(import.meta.url));
const links = JSON.parse(await fs.readFile(path.join(root, 'diagramas.json'), 'utf8'));
const complete = await fs.readFile(path.join(root, 'dbdiagram.dbml'), 'utf8');
const mvp = await fs.readFile(path.join(root, 'mvp_dbdiagram.io.dbml'), 'utf8');
const columns = source => source.split('\n').filter(line => /^  (?:\w+|"año") (?:integer|smallint|varchar|text|boolean|timestamp)\b/.test(line));
assert.equal(columns(complete).length, 17);
assert.equal(columns(mvp).length, 5);
assert.deepEqual(columns(mvp).map(line => line.trim().split(' ')[0]), ['id', 'titulo', 'autor', '"año"', 'disponible']);

const doc = await PDFDocument.create();
doc.setTitle('30. dbdiagram - Biblioteca y modelo MVP');
doc.setAuthor('Jonathan Serna');
doc.setSubject('Programación Asistida por Inteligencia Artificial');
const regular = await doc.embedFont(StandardFonts.Helvetica);
const bold = await doc.embedFont(StandardFonts.HelveticaBold);
const mono = await doc.embedFont(StandardFonts.Courier);
const gray = rgb(0.38, 0.43, 0.49);
const width = 612;
const height = 792;
function text(page, value, x, y, size = 11, font = regular, color = rgb(0, 0, 0)) {
  assert(y >= 40 && y < height, 'Text must stay inside page margins');
  page.drawText(value, { x, y, size, font, color });
}
function paragraph(page, value, x, y, maxWidth = 516, size = 11, font = regular) {
  let line = '';
  for (const word of value.split(/\s+/)) {
    const next = line ? `${line} ${word}` : word;
    if (font.widthOfTextAtSize(next, size) > maxWidth && line) {
      text(page, line, x, y, size, font);
      y -= size * 1.45;
      line = word;
    } else line = next;
  }
  if (line) text(page, line, x, y, size, font);
  return y - size * 1.45;
}
function center(page, value, y, size) {
  text(page, value, (width - regular.widthOfTextAtSize(value, size)) / 2, y, size);
}
function page() {
  const result = doc.addPage([width, height]);
  const n = doc.getPageCount();
  if (n > 1) result.drawText('Ejercicio 30 - dbdiagram y biblioteca', { x:48, y:22, size:8, font:regular, color:gray });
  result.drawText(String(n), { x:565, y:22, size:8, font:regular, color:gray });
  return result;
}
function link(page, label, url, y) {
  text(page, label, 48, y, 10, bold);
  const bottom = paragraph(page, url, 48, y - 16, 516, 8.3);
  const annotation = doc.context.register(doc.context.obj({ Type:'Annot', Subtype:'Link', Rect:[48,bottom,564,y], Border:[0,0,0], A:{Type:'Action',S:'URI',URI:PDFString.of(url)} }));
  page.node.set(PDFName.of('Annots'),doc.context.obj([annotation]));
}
const cover = page();
center(cover, '30. Ejercicio de dbdiagram', 612, 28);
center(cover, 'Biblioteca y modelo MVP', 564, 24);
center(cover, 'Jonathan Serna', 466, 13);
center(cover, 'Ingeniería en Software', 426, 13);
center(cover, 'Programación Asistida por Inteligencia Artificial', 386, 13);

const full = page();
text(full, '1. Descripción del ejercicio', 48, 736, 18, bold);
paragraph(full, 'El ejercicio consiste en diseñar una tabla de libros para una biblioteca usando DBML y visualizarla en dbdiagram.io. Se elaboraron dos versiones: un catálogo completo y un producto mínimo viable (MVP) con los cinco datos esenciales solicitados.', 48, 708);
text(full, '2. Resultado del modelo completo', 48, 623, 17, bold);
let y = paragraph(full, 'El diagrama dbdiagram contiene una tabla libros con 17 campos. Cada registro representa una edición y agrupa la cantidad de ejemplares que posee la biblioteca.', 48, 594, 280);
const groups = [
  ['Identificación', 'id_libro e isbn; el identificador es automático y el ISBN es único cuando se registra.'],
  ['Datos del libro', 'Título, subtítulo, autor principal, editorial, categoría e idioma.'],
  ['Edición y contenido', 'Año de publicación, número de edición, páginas y sinopsis.'],
  ['Control del catálogo', 'Ubicación, ejemplares totales y disponibles, fecha de registro y observaciones.'],
  ['Restricciones', 'Título no vacío, valores numéricos positivos y disponibilidad entre cero y el total. El ISBN admite 10 o 13 caracteres.'],
];
for (const [label, value] of groups) {
  text(full, label, 48, y - 10, 11, bold);
  y = paragraph(full, value, 48, y - 28, 280, 10.5) - 9;
}
const fullCrop = await sharp(path.join(root, 'capturas/dbdiagram.png')).extract({left:1045,top:323,width:325,height:590}).png().toBuffer();
const fullImage = await doc.embedPng(fullCrop);
full.drawImage(fullImage,{x:354,y:197,width:210,height:381.23});
text(full, 'Diagrama real en dbdiagram.io', 354, 180, 9, regular, gray);
paragraph(full, 'Resultado: el editor generó la tabla y mostró el indicador de guardado. Se conserva como diagrama privado. El modelo no incluye préstamos ni el seguimiento individual de cada ejemplar.', 48, 145, 516, 10.5);
link(full, 'Abrir el modelo completo (requiere la cuenta propietaria):', links.completo.url, 88);

const minimal = page();
text(minimal, '3. Resultado del MVP', 48, 736, 18, bold);
paragraph(minimal, 'El diagrama mvp_dbdiagram.io simplifica la biblioteca a una tabla libros con exactamente cinco campos. Permite identificar un libro, conocer su autor y año, y consultar si está disponible.', 48, 708);
const rows = [
  ['Campo', 'Tipo', 'Función'],
  ['id', 'integer', 'Clave primaria automática.'],
  ['titulo', 'varchar(255)', 'Nombre del libro.'],
  ['autor', 'varchar(200)', 'Nombre del autor.'],
  ['año', 'smallint', 'Año de publicación positivo.'],
  ['disponible', 'boolean', 'true: disponible; false: no disponible.'],
];
rows.forEach((row, index) => {
  const top = 638 - index * 29;
  if (index === 0) minimal.drawRectangle({x:48,y:top-23,width:516,height:29,color:rgb(0.91,0.93,0.95)});
  row.forEach((value, column) => text(minimal,value,[55,150,275][column],top-14,10,index===0?bold:regular));
  minimal.drawLine({start:{x:48,y:top-23},end:{x:564,y:top-23},thickness:0.6,color:rgb(0.75,0.8,0.85)});
});
text(minimal, 'Código esencial del MVP', 48, 425, 12, bold);
const code = ['Table libros {','  id integer [pk, increment]','  titulo varchar(255) [not null]','  autor varchar(200) [not null]','  "año" smallint [not null]','  disponible boolean [not null, default: true]','}'];
code.forEach((line,index) => text(minimal,line,48,402-index*15,8.2,mono));
const mvpCrop = await sharp(path.join(root,'capturas/mvp_dbdiagram.io.png')).extract({left:1086,top:515,width:244,height:210}).png().toBuffer();
const mvpImage = await doc.embedPng(mvpCrop);
minimal.drawImage(mvpImage,{x:365,y:294,width:199,height:171.27});
text(minimal,'Diagrama real del MVP',365,280,9,regular,gray);
paragraph(minimal, 'El archivo DBML también exige título y autor no vacíos y año positivo. disponible es obligatorio y comienza en true. Representa una disponibilidad general: no cuenta copias ni identifica a quién se prestó el libro.',48,251,516,10.5);
text(minimal,'4. Comparación y conclusión',48,181,13,bold);
paragraph(minimal,'El modelo completo ofrece más información bibliográfica y control de cantidades. El MVP conserva solo lo necesario para un catálogo básico. Ambos se visualizaron y guardaron en dbdiagram.io; no se implementó una base de datos ni una aplicación de préstamos.',48,159,516,10.5);
link(minimal,'Abrir el MVP (requiere la cuenta propietaria):',links.mvp.url,88);
assert.equal(doc.getPageCount(),3);
const output = path.join(root,'Ejercicio_30_dbdiagram.pdf');
await fs.writeFile(output,await doc.save());
await fs.copyFile(output,path.join(root,'../PDFs ejercicios/Ejercicio_30_dbdiagram.pdf'));
const reopened = await PDFDocument.load(await fs.readFile(output));
assert.equal(reopened.getPageCount(),3);
console.log(JSON.stringify({pages:3,completeColumns:17,mvpColumns:5,output},null,2));
