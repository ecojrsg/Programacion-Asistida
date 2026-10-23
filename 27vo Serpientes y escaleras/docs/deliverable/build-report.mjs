import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { createRequire } from 'node:module';

const require = createRequire(path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json'));
const { PDFDocument, StandardFonts, rgb, PDFName, PDFString } = require('pdf-lib');
const [project, revision, destination] = process.argv.slice(2);
if (!project || !/^[a-f0-9]{40}$/.test(revision ?? '') || !destination) throw new Error('Usage: node build-report.mjs PROJECT COMMIT_SHA OUTPUT_PDF');
const pdf = await PDFDocument.create();
pdf.setTitle('27. Serpientes y escaleras - Laboratorio de refinamiento iterativo');
pdf.setAuthor('Jonathan Ricardo Serna Galina');
pdf.setSubject('Programación Asistida');
const regular = await pdf.embedFont(StandardFonts.Helvetica);
const bold = await pdf.embedFont(StandardFonts.HelveticaBold);
const mono = await pdf.embedFont(StandardFonts.Courier);
const symbol = await pdf.embedFont(StandardFonts.Symbol);
const root = 'https://github.com/ecojrsg/Programacion-Asistida';
const relativeProject = path.basename(project);
const route = p => p.split(/[\\/]/).map(encodeURIComponent).join('/');
const codeLink = p => `${root}/blob/${revision}/${route(relativeProject + '/' + p)}`;
const documentLink = p => `${root}/blob/main/${route(relativeProject + '/' + p)}`;
const codeFolder = `${root}/tree/${revision}/${route(relativeProject)}`;
const manifest = JSON.parse(await fs.readFile(path.join(project, 'docs/deliverable/chat-manifest.json'), 'utf8'));
const chat = (await fs.readFile(path.join(project, 'docs/conversations/07-chat-crudo.jsonl'), 'utf8')).trim().split('\n').map(JSON.parse);
const markdown = (await fs.readdir(project, { recursive: true })).filter(p => p.endsWith('.md')).map(p => p.replaceAll('\\', '/')).sort();
const validation = { revision, pages: 0, images: [], links: [], textBounds: [], unsupported: [] };
let page;
let y;
let continuation = '';
const ink = rgb(.08, .08, .08);
const blue = rgb(.07, .23, .48);
const gray = rgb(.35, .35, .35);

function fontFor(c, font) {
  try { font.encodeText(c); return font; } catch {
    try { symbol.encodeText(c); return symbol; } catch { validation.unsupported.push(c); throw new Error(`Unsupported character: ${c}`); }
  }
}
function width(text, font, size) {
  return [...text].reduce((sum, c) => sum + fontFor(c, font).widthOfTextAtSize(c, size), 0);
}
function draw(text, x, baseline, font = regular, size = 10.5, color = ink, url) {
  let start = x;
  let run = '';
  let active;
  const flush = () => {
    if (!run) return;
    page.drawText(run, { x: start, y: baseline, font: active, size, color });
    start += active.widthOfTextAtSize(run, size);
    run = '';
  };
  for (const c of text) { const f = fontFor(c, font); if (f !== active) { flush(); active = f; } run += c; }
  flush();
  validation.textBounds.push({ page: pdf.getPageCount(), x, y: baseline, right: start, size });
  if (url) {
    const link = pdf.context.obj({ Type: 'Annot', Subtype: 'Link', Rect: [x, baseline - 2, start, baseline + size + 1], Border: [0, 0, 0], A: { Type: 'Action', S: 'URI', URI: PDFString.of(url) } });
    page.node.addAnnot(pdf.context.register(link));
    validation.links.push({ text, url, page: pdf.getPageCount() });
  }
}
function newPage() {
  page = pdf.addPage([612, 792]);
  y = 735;
  draw(String(pdf.getPageCount()), 558, 18, regular, 6);
  if (continuation) { draw(continuation, 54, y, bold, 11); y -= 26; }
}
function ensure(height) { if (y - height < 48) newPage(); }
function wrap(line, font, size, maxWidth, literal = false) {
  if (!line) return [''];
  const out = [];
  let current = '';
  for (const c of line.replaceAll('\t', '    ')) {
    if (width(current + c, font, size) > maxWidth && current) {
      const at = !literal ? current.lastIndexOf(' ') : -1;
      if (at > 0) { out.push(current.slice(0, at)); current = current.slice(at + 1) + c; }
      else { out.push(current); current = c; }
    } else current += c;
  }
  if (current) out.push(current);
  return out;
}
function para(text, options = {}) {
  const { font = regular, size = 10.5, leading = size * 1.4, x = 54, maxWidth = 504, literal = false, gap = 9, color = ink, url } = options;
  const lines = text.split(/\r?\n/);
  while (lines.length > 1 && lines.at(-1) === '') lines.pop();
  for (const raw of lines) for (const line of wrap(raw, font, size, maxWidth, literal)) {
    ensure(leading);
    if (line) draw(line, x, y, font, size, color, url);
    y -= leading;
  }
  y -= gap;
}
function heading(text, size = 14) { ensure(60); para(text, { font: bold, size, gap: 10 }); }
function link(label, url, size = 10) { para(label, { size, color: blue, url, gap: 5 }); }
function centered(text, baseline, size, font = regular) { draw(text, (612 - width(text, font, size)) / 2, baseline, font, size); }
async function figure(file, caption, maxHeight = 520, maxWidth = 504, x) {
  const bytes = await fs.readFile(path.join(project, file));
  const image = file.endsWith('.png') ? await pdf.embedPng(bytes) : await pdf.embedJpg(bytes);
  const scale = Math.min(maxWidth / image.width, maxHeight / image.height);
  const w = image.width * scale;
  const h = image.height * scale;
  ensure(h + 46);
  page.drawImage(image, { x: x ?? (612 - w) / 2, y: y - h, width: w, height: h });
  validation.images.push({ file, page: pdf.getPageCount(), x: x ?? (612 - w) / 2, y: y - h, width: w, height: h });
  y -= h + 17;
  para(caption, { size: 9, color: gray, gap: 7 });
  link('Abrir imagen original en GitHub', documentLink(file), 9);
}

newPage();
centered('27. Serpientes y escaleras', 560, 22, bold);
centered('Jonathan Ricardo Serna Galina', 500, 12);
centered('20074902', 482, 12);
centered('Programación Asistida', 294, 12);

newPage();
heading('1. Objetivo y alcance del entregable');
para('Desarrollé un juego de serpientes y escaleras con HTML, CSS y JavaScript puros para practicar el refinamiento iterativo de prompts. El proceso conserva planificación, revisión del estudiante, resultados y capturas reales.');
para('El juego tiene dos jugadores locales, tablero de 100 casillas, turnos, dado, serpientes, escaleras, llegada exacta a la meta y reinicio. Las reglas están separadas de la interfaz y de los efectos visuales. No requiere instalación, servidor ni conexión para jugar.');
heading('Requisitos de la consigna', 12);
para('1. Crear un Markdown de buenas prácticas para HTML, CSS y JavaScript.\n2. Crear AGENTS.md y señalar esas rutas.\n3. Diseñar la aplicación. La imagen dice Build, no Plan; por indicación del estudiante se considera un error y se planifica antes de implementar.\n4. Implementar y aplicar una mejora usando una imagen como referencia.\n5. Añadir otra iteración que permita elegir entre tres escenarios.');
heading('Estado real de la entrega', 12);
para('Este PDF incluye el resumen del refinamiento, capturas del juego y de sus cambios, liga al código publicado, ligas a todos los Markdown y el chat de desarrollo sin resumir. El selector de tres escenarios NO está implementado. La revisión humana de todos los documentos sigue pendiente. Por petición expresa, durante esta entrega no se modificó el juego.');
para('La corrección con imagen de la distribución se documenta como refinamiento visual real. No se afirma que el docente haya validado que sustituye una iteración formal ni que el laboratorio esté completamente terminado.');

newPage();
heading('2. Cómo apliqué refinamiento iterativo');
para('La meta original se mantuvo: código sencillo, sin frameworks y efectos ligeros separados. El ciclo fue petición del estudiante, diagnóstico, plan, cambio acotado, comprobación y nueva revisión humana.');
para('El formato del ejemplo del docente no fue proporcionado. La organización Meta original, Refinamientos anteriores, Nuevo refinamiento y Criterios de aceptación se usa como guía provisional; no se presenta como un prompt enviado antes de existir. Los mensajes exactos están en el anexo.');
heading('Versión inicial y planificación', 12);
para('Se eligieron dos jugadores locales, diorama colorido y efectos en archivos separados. El estudiante aprobó la implementación con el mensaje literal:');
para('Hazlo implementalo', { font: mono, size: 10 });
heading('Refinamiento de distribución con imagen', 12);
para('Después de corregir tamaño y centrado, el estudiante adjuntó una captura donde la inclinación y sombra del tablero tapaban la leyenda. También indicó que no necesitaba centrado vertical. Se conservó el centrado horizontal, se alineó el contenido arriba y se reservó espacio para el relieve.');
para('Criterio: leyenda e iconos completos, sin superposición, y scroll solo cuando el contenido no cabe. El estudiante respondió «Super bien».');
heading('Refinamiento del dado y del marcador', 12);
para('El primer intento amplió el giro de 0.45 a 1.25 segundos, con rebote. La revisión humana detectó pausas y que el marcador anticipaba el número. El siguiente cambio sustituyó los tramos por un giro continuo y mostró «…» hasta que el dado se asentara. Después aparece el número y se mueve la ficha.');
para('Criterio: rotación sin paradas intermedias, cara final correcta y resultado revelado al asentarse. La solicitud de este PDF comienza con «Perfecto». Esa valoración no se interpreta como revisión de todos los Markdown.');

newPage();
heading('3. Evidencia de la versión inicial');
await figure('docs/evidence/01-desktop.jpg', 'Versión inicial real conservada antes de las correcciones de distribución y de animación.', 535);
para('La lógica aprobó 17 comprobaciones deterministas. Se verificaron una partida completa, turnos, victoria, reinicio y recuperación ante errores de la capa visual. Los límites de estas pruebas están registrados en el informe técnico.');
link('Informe de verificación de la primera fase', documentLink('docs/reviews/01-verification.md'));

newPage();
heading('4. Mejora de distribución con referencia');
await figure('docs/evidence/04-desktop-spacing.jpg', 'Después: leyenda separada del tablero, centrado horizontal y alineación superior. Captura de la etapa de distribución, anterior al cambio del dado.', 525);
para('La imagen que motivó esta corrección se conserva como adjunto del chat. La transformación 3D no reserva espacio en el flujo; por eso se añadió separación para impedir que el relieve tapara los iconos.');
link('Referencia del usuario: elementos tapados', documentLink('docs/evidence/04-user-spacing.png'));
link('Plan, medidas y revisión de distribución', documentLink('docs/plans/04-board-spacing.md'));

newPage();
heading('5. Adaptación a móvil');
await figure('docs/evidence/04-mobile-spacing.jpg', 'Interfaz móvil de la etapa de distribución. El tablero pierde inclinación y los controles se organizan debajo. Se mantiene el desplazamiento vertical necesario.', 535);
para('La revisión técnica incluyó anchos de 320 y 390 px sin desbordamiento horizontal. Son pruebas emuladas en Chrome; no se presentaron como comprobación en teléfonos físicos.');

newPage();
heading('6. Dado: resultado oculto y revelado');
const startY = y;
const files = ['docs/evidence/06-dice-rolling.jpg', 'docs/evidence/06-dice-result.jpg'];
for (let i = 0; i < files.length; i++) {
  const image = await pdf.embedJpg(await fs.readFile(path.join(project, files[i])));
  const w = 205;
  const h = image.height * w / image.width;
  const x = 76 + i * 255;
  page.drawImage(image, { x, y: startY - h, width: w, height: h });
  validation.images.push({ file: files[i], page: pdf.getPageCount(), x, y: startY - h, width: w, height: h });
}
y = startY - 415;
para('Izquierda: muestra pausada durante el giro con «…». Derecha: tirada completa sin pausa, cara 6, marcador 6 y ficha en 30.', { size: 9, color: gray });
para('La prueba del marcador registró «…» a los 500 ms y la primera aparición de «6» a los 1257 ms. La ficha terminó su recorrido a los 2202 ms. El giro conserva 1.25 segundos y una única curva de desaceleración.');
para('La prueba actual aprobó 39 comprobaciones en escritorio y móvil, y 38 con movimiento reducido; en ese modo no se ejecuta el muestreo del giro. Se verificaron resultado repetido, cancelación y recuperación ante fallos.');
link('Plan y comprobaciones del giro continuo', documentLink('docs/plans/06-continuous-roll.md'));
link('Prueba ejecutable de la animación', codeLink('tests/motion.html'));

newPage();
heading('7. Control humano y requisitos pendientes');
para('La consigna evalúa el control de todo lo generado, incluidos todos los .md; exige que se note la revisión humana e indica una afectación de 0.2 por puntos no revisados. Las pruebas técnicas del asistente no sustituyen esa revisión.');
const status = [
  ['Buenas prácticas y AGENTS', 'Creados y enlazados. La revisión completa de los documentos sigue pendiente.'],
  ['Planificación antes del código', 'Plan de fase 1 aprobado con «Hazlo implementalo». La interpretación Build a Plan pertenece al estudiante.'],
  ['Refinamiento con capturas', 'Cambios reales de distribución y dado documentados; se conservan mensajes, imágenes y resultados.'],
  ['Revisión del juego', 'El usuario señaló fallos, pidió correcciones y expresó «Super bien» y «Perfecto» sobre resultados observados.'],
  ['Tres escenarios', 'PENDIENTE. No existe selector de tres escenarios y no se implementó durante esta entrega.'],
  ['Revisión de todos los archivos', 'PENDIENTE. No hay evidencia de lectura y aprobación humana de cada Markdown y archivo.'],
  ['PDF y código publicado', 'El documento reúne las cinco piezas del entregable. La liga al código corresponde a una revisión fija del repositorio.'],
];
for (const [name, state] of status) { heading(name, 11); para(state); }
link('Matriz completa de revisión humana', documentLink('docs/reviews/00-review-status.md'));

newPage();
heading('8. Código publicado y reproducción');
para(`Repositorio: ecojrsg/Programacion-Asistida.\nRevisión de código: ${revision}.`);
link('Abrir carpeta del ejercicio en la revisión publicada', codeFolder);
for (const file of ['index.html', 'styles.css', 'game.js', 'script.js', 'visuals/effects.css', 'visuals/effects.js', 'tests/rules.html', 'tests/motion.html']) link(file, codeLink(file));
para('Para jugar, descargo esa revisión y abro index.html. Los enlaces de GitHub permiten revisar los archivos; no representan un sitio publicado con GitHub Pages. La partida vive en la pestaña y se reinicia al cerrar o recargar.');
para('La entrega en PDF no modifica HTML, CSS, JavaScript ni pruebas del juego. Los cambios de esta etapa corresponden a documentación, exportación del chat y el propio PDF.');
heading('Ligas al historial sin resumir', 12);
link('Chat completo de desarrollo en UTF-8', documentLink('docs/conversations/07-chat-crudo.txt'));
link('Chat estructurado, un mensaje por registro JSONL', documentLink('docs/conversations/07-chat-crudo.jsonl'));
para(`Corte del registro: ${manifest.cutoff}. Se incluyen ${manifest.entries} intervenciones: ${manifest.user} del usuario y ${manifest.assistant} del asistente, incluido el formulario y sus selecciones. El corte llega hasta la solicitud de este PDF, inclusive; la generación posterior aún estaba en curso.`);

newPage();
heading('9. Ligas a todos los Markdown');
para('Cada nombre es un enlace clicable a su archivo en main. La referencia fija del código está en la sección anterior. Las transcripciones por etapa se conservan junto al nuevo registro nativo.');
for (const file of markdown) link(file, documentLink(file), 9.5);

newPage();
heading('Anexo A. Chat crudo de desarrollo');
para('Se reproducen los textos del usuario y del asistente, sin resumir ni corregir su ortografía, en el orden del registro nativo. Los formularios y sus selecciones conservan su JSON. Se excluyen instrucciones de sistema, razonamiento privado, skills inyectadas como contexto y trazas de herramientas. Los saltos de línea adicionales solo permiten ajustar el texto a la página; el archivo UTF-8 conserva la fuente.');
para('La última intervención de este anexo es la petición de crear el PDF. Las imágenes adjuntas se conservan en los archivos de evidencia y se muestran o enlazan en el Anexo B. No se inventa un mensaje final de un turno que el usuario interrumpió.');
for (let i = 0; i < chat.length; i++) {
  const entry = chat[i];
  continuation = '';
  ensure(70);
  heading(`${String(i + 1).padStart(3, '0')}. ${entry.role} - ${entry.kind}`, 11);
  if (entry.timestamp) para(entry.timestamp, { size: 8.5, color: gray, gap: 5 });
  continuation = `${entry.role} - continuación de la intervención ${i + 1}`;
  para(entry.text, { font: mono, size: 9, leading: 12.6, literal: true, gap: 11 });
  if (entry.attachments?.length) para('Adjuntos: ' + entry.attachments.join(', '), { size: 8.5, color: gray });
}

continuation = '';
newPage();
heading('Anexo B. Imágenes aportadas en el chat');
await figure('docs/evidence/00-assignment.png', 'Consigna original: objetivo, instrucciones, criterios de evaluación y contenido del PDF.', 350);
link('Consigna adjunta otra vez a la solicitud del PDF', documentLink('docs/evidence/07-assignment-pdf.png'));
para('La solicitud inicial y la solicitud final adjuntaron la misma consigna visual. Se conservan ambos archivos originales; la imagen no sustituye una aprobación del docente sobre los requisitos pendientes.');

newPage();
heading('Anexo B. Referencia de centrado');
await figure('docs/evidence/03-user-window.png', 'Captura del usuario al señalar que el juego todavía no estaba centrado. La zona gris reveló una resolución de prueba del navegador que se había dejado activa.', 390);
link('Diagnóstico y rectificación de la prueba', documentLink('docs/plans/03-browser-window.md'));

newPage();
heading('Anexo B. Referencia de distribución');
await figure('docs/evidence/04-user-spacing.png', 'Captura del usuario: el relieve tapaba parte de la leyenda y pidió retirar el centrado vertical. La mejora aparece en la sección 4.', 535);

validation.pages = pdf.getPageCount();
const invalid = validation.textBounds.filter(b => b.x < 45 || b.right > 568 || b.y < 15 || b.y + b.size > 760);
if (invalid.length || validation.unsupported.length) throw new Error(`Invalid text bounds: ${JSON.stringify(invalid.slice(0, 4))}`);
await fs.mkdir(path.dirname(destination), { recursive: true });
await fs.writeFile(destination, await pdf.save());
delete validation.textBounds;
await fs.writeFile(path.join(project, 'docs/deliverable/pdf-validation.json'), JSON.stringify(validation, null, 2) + '\n');
console.log(JSON.stringify({ output: destination, pages: validation.pages, images: validation.images.length, links: validation.links.length, markdown: markdown.length }));
