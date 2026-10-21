# Programacion-Asistida: documentation conventions

These conventions come from the repository inspected on 2026-10-21. Recheck the
current files when using the skill later; the repository can change.

## Exercise folders and numbering

- Inspect direct child directories at the repository root. Read their leading
  exercise numbers, ignoring unrelated directories such as `PDFs ejercicios`.
- For an ordinary new exercise, use the next number after the highest existing
  exercise. Respect a number explicitly assigned by the user or the assignment.
  If that number already exists, inspect it before deciding whether to reuse it.
- Existing names vary: `1er Ejercicio áreas`, `10mo Ejercicio uv_example`, and
  `23vo Skill Chamaleon`. Preserve them exactly when linking or documenting.
- Recent folders follow `Nvo Descriptive topic`, such as `25vo Knowledge Priming`.
  This assignment uses `26vo Skills OpenCode`; do not reserve 26 for future work.
- Do not renumber siblings or infer the next exercise from the root README alone:
  at inspection time its index ended at 17 while folders reached 25.
- Keep each exercise's source, documents, and assets inside its own folder.
  The shared `PDFs ejercicios` folder is an established delivery destination.

## Exercise README

- Use a title such as `# 26. Tarea de skills de OpenCode`.
- Write a brief goal, actual contents, requirements, and usable steps. Use the
  six sections in the template to satisfy this assignment.
- Use relative Markdown links. Encode spaces as `%20` or put link targets with
  spaces between angle brackets. Resolve links from the README's own directory.
- A compact tree should describe actual files and include meaningful hidden
  directories such as `.opencode/skills`.
- Commands must state their working directory. Quote folder names with spaces.
- Distinguish a requirement from a locked version and an observed installation.
  Do not copy another exercise's runtime or dependencies without inspection.
- Keep attribution and licenses. Use clear, brief explanations with concrete
  examples. State unresolved checks where they affect use of the deliverable.

## Root README: repository registry

The root `README.md` is a registry of exercises organized by work day. It is
different from the README explaining one project. When an index update is in
scope, add or update only the relevant entry with this observed structure:

```markdown
### N. Exercise title

- **Tema:** Main topic.
- **Descripción:** Actual purpose or behavior.
- **Ubicación:** [Exercise folder](actual-relative-path/)
- **Estado:** Verified status.
- **Documentación:** [README](actual-relative-path/README.md)
- **PDF:** [Report](PDFs%20ejercicios/actual-existing-report.pdf)
```

Replace all example fields. Use Spanish labels for this registry. Add a PDF
link only if that file exists. Use an established work date or one confirmed
for the activity; do not invent a date or mark unperformed work as completed.

## PDF names and destination

- If a PDF is requested, use `PDFs ejercicios/Ejercicio_NN_Topic.pdf`, with a
  two-digit number below 100. Example: `Ejercicio_23_Skill_Camaleon.pdf`.
- For a presentation, an observed name is
  `Ejercicio_24_MCP_OpenCode_Presentacion.pdf`.
- Keep historical filenames unchanged. Avoid overwriting an existing delivery
  unless replacement was requested; otherwise create a clearly versioned file.

## PDF preparation and review

1. Inspect an existing PDF, such as `Ejercicio_22_Mermaid.pdf`, before matching
   its format. Read a real cover and content page rather than guessing.
2. For a written report, preserve its US Letter portrait page size, white
   background, centered cover, simple sans-serif font, numbered sections,
   readable margins, and page numbering. The cover identifies the exercise,
   student, student number, and `Programación Asistida`.
3. Copy identity fields only from a verified reference or the user's current
   instructions. Do not invent identity, dates, test results, or evidence.
4. Keep the report focused on the assignment: goal, approach, relevant examples,
   criteria, checks, and limitations. A report need not include every source file.
5. Use available document/PDF tooling, such as the environment's PDF skill or
   installed libraries. Do not assume a global export script exists: this
   repository does not establish one. Avoid new dependencies when available
   tools can produce the requested file. If Python source is needed, follow the
   repository's author-confirmation and `hackthon` requirements first.
6. For a requested slide deck, adapt the identification and visual hierarchy to
   a landscape layout. Use supplied or properly sourced images when required,
   preserving legibility. Keep conceptual illustrations separate from evidence.
7. Export to PDF, reopen it, check page count, and render every page for visual
   review. Fix clipping, overlap, illegible examples, and missing images.
8. Save only the final delivery in `PDFs ejercicios`; keep necessary source
   assets in the exercise and temporary builds out of the delivery folder.
9. Add working relative links from the exercise README to the final PDF.

## Evidence used to establish these conventions

- Root `README.md`: dated registry and entry labels.
- Root `AGENTS.md`: separate exercise boundaries and Python requirements.
- `14vo Ejercicio CoT BookingCalendar/README.md`: commands, contract, evidence.
- `23vo Skill Chamaleon/README.md`: local skill, example, verification limits.
- `24vo MCP's/README.md`: multiple deliverables and observed versus pending work.
- `PDFs ejercicios/Ejercicio_22_Mermaid.pdf`: written-report cover and layout.
- `PDFs ejercicios/Ejercicio_23_Skill_Camaleon.pdf`: numbered report and examples.
- `PDFs ejercicios/Ejercicio_24_MCP_OpenCode_Presentacion.pdf`: illustrated slides.
