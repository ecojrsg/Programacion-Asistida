---
name: medieval-chameleon
description: Rewrite human-readable comments, console messages, logs, and prose in a medieval epistolary tone while preserving executable code and machine-readable strings. Use for the chameleon exercise or requests to give existing text the voice of a medieval letter.
---

# Medieval Chameleon

Transform existing human-readable text into an original medieval letter: solemn,
intimate, reflective, and clear. Evoke a chronicler writing to a trusted relative.
Use the referenced Ezio letter as a mood reference, without quoting or reproducing
its wording. Preserve the source language unless the user explicitly requests a
translation. In Spanish, prefer restrained expressions such as “os”, “vuestra”,
“que conste en esta crónica”, and “al término de esta jornada”. Avoid parody,
excessive archaisms, invented plot details, and turning short messages into letters.

## Scope and permitted edits

- Resolve the exact file or directory requested by the user. Stay inside that
  exercise; never install this skill globally or edit neighboring projects.
- Read applicable project instructions and inspect the target before editing.
  Preserve authorship, dates, licenses, assignment statements, and existing work.
- Edit only ordinary explanatory comments, natural-language documentation, and
  human-facing literal text in messages, prompts, logs, or errors.
- Keep the original meaning, facts, severity, and instructions understandable.
  A failure must remain a failure; a success must remain a success.
- Leave identifiers, imports, types, operators, control flow, calculations, data
  structures, calls, arguments, and formatting outside allowed text untouched.
- Preserve placeholders and interpolated expressions byte for byte, including
  `${...}`, `{name}`, `%s`, format specifications, escapes, and newlines.
- Preserve machine-readable strings: keys, paths, URLs, queries, commands,
  selectors, enum/status values, regular expressions, protocol messages, and
  strings involved in comparisons or parsing. A string literal is not
  automatically prose. Leave ambiguous strings unchanged and report them.
- Preserve shebangs, encoding declarations, compiler/linter/type directives,
  annotations interpreted by tools, and executable examples in documentation.
  Never reformat, fix, rename, or refactor code as part of this transformation.

## Execute and verify

1. Read and retain the original target and its current diff before editing.
   Identify the exact comment spans and human-facing literal segments to change.
2. Apply only those textual substitutions. Do not use a file-wide replacement
   that could alter machine strings or executable expressions.
3. Compare the result against the original. Every changed byte must belong to
   an approved text span; compare all remaining content exactly. When a parser
   is already available, also compare syntax trees after masking only approved
   text values and comments. An unchanged syntax tree alone is insufficient:
   verify machine strings and interpolation expressions separately.
4. Run available syntax checks and relevant existing tests. For a safe, local
   example, compare executions: data and behavior must remain the same, with
   only the intended human-readable output different. Do not execute a program
   with unknown side effects merely to check its wording.
5. If any executable content changes, undo the skill's own edits immediately
   using `/undo` when available. Otherwise restore only the skill's edits from
   the retained original, preserving pre-existing user changes. Improve these
   instructions before retrying; never repair the program's code to make the
   transformation pass. If verification is unavailable, report that limitation
   and do not claim code preservation was verified.
6. Report the files changed, the checks performed, and any text left unchanged.

## Examples

- `Proceso iniciado.` → `Doy comienzo a esta jornada.`
- `No se pudo abrir el archivo.` → `No me fue posible abrir el archivo.`
- `Total: ${total}` → `Que conste en esta crónica el total: ${total}`
- `status === "ready"` → unchanged: this is executable logic and a status value.

Keep changes concise and proportional to the original message. If the text
already has the requested voice, leave it unchanged.
