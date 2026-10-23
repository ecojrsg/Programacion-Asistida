import fs from 'node:fs/promises';
import path from 'node:path';

// Export only the human-visible development conversation, never model context.
const [source, project] = process.argv.slice(2);
if (!source || !project) throw new Error('Usage: node export-chat.mjs SESSION_JSONL PROJECT');
const rows = (await fs.readFile(source, 'utf8')).split('\n').filter(Boolean).map(JSON.parse);
const entries = [];
let formCall;
let cutoff;
for (const row of rows) {
  const p = row.payload;
  if (row.type !== 'response_item') continue;
  if (['function_call', 'custom_tool_call'].includes(p?.type) && String(p.name).endsWith('request_user_input')) {
    formCall = p.call_id;
    entries.push({ role: 'Asistente', kind: 'formulario', timestamp: row.timestamp, text: p.arguments ?? p.input });
    continue;
  }
  if (p?.call_id === formCall && ['function_call_output', 'custom_tool_call_output'].includes(p.type)) {
    entries.push({ role: 'Usuario', kind: 'selecciones del formulario', timestamp: row.timestamp, text: p.output });
    formCall = undefined;
    continue;
  }
  if (p?.type !== 'message' || !['user', 'assistant'].includes(p.role)) continue;
  if (p.role === 'assistant' && !['commentary', 'final_answer'].includes(p.phase)) continue;
  let text = p.content.filter(c => typeof c.text === 'string').map(c => c.text).join('\n');
  if (!text || /^(# AGENTS\.md instructions|<external_codex_apps|<skill>)/.test(text)) continue;
  const attachments = [...text.matchAll(/^## ([^\n]+\.png):/gm)].map(m => m[1]);
  if (text.includes('## My request:')) text = text.slice(text.indexOf('## My request:') + '## My request:'.length).replace(/^\r?\n/, '');
  entries.push({ role: p.role === 'user' ? 'Usuario' : 'Asistente', kind: p.phase ?? 'mensaje', timestamp: row.timestamp, text, ...(attachments.length ? { attachments } : {}) });
  if (p.role === 'user' && text.includes('ya no modifiques el juego') && text.includes('archivo pdf')) {
    cutoff = row.timestamp;
    break;
  }
}
if (!cutoff || entries[0]?.role !== 'Usuario') throw new Error('Development transcript boundaries not found.');
const target = path.join(project, 'docs/conversations');
await fs.mkdir(target, { recursive: true });
await fs.writeFile(path.join(target, '07-chat-crudo.jsonl'), entries.map(e => JSON.stringify(e)).join('\n') + '\n');
const note = 'CHAT DE DESARROLLO - EJERCICIO 27\nExportación del registro nativo. Corte: solicitud del PDF inclusive.\nMensajes del usuario y asistente sin resumir; incluye formulario y selecciones.\nNo incluye instrucciones internas, razonamiento privado ni trazas de herramientas.\nLos adjuntos se conservan en docs/evidence.\n\n';
await fs.writeFile(path.join(target, '07-chat-crudo.txt'), note + entries.map((e, i) => `${String(i + 1).padStart(3, '0')}. ${e.role} | ${e.kind} | ${e.timestamp ?? ''}\n${e.text}${e.attachments?.length ? '\nAdjuntos: ' + e.attachments.join(', ') : ''}\n`).join('\n'));
await fs.writeFile(path.join(project, 'docs/deliverable/chat-manifest.json'), JSON.stringify({ cutoff, entries: entries.length, user: entries.filter(e => e.role === 'Usuario').length, assistant: entries.filter(e => e.role === 'Asistente').length, forms: entries.filter(e => e.kind === 'formulario').length, scope: 'Visible development conversation through the PDF request, inclusive; no internal context or reasoning.' }, null, 2) + '\n');
console.log(JSON.stringify({ entries: entries.length, cutoff, files: ['07-chat-crudo.txt', '07-chat-crudo.jsonl'] }));
