---
name: readme-academico
description: Create or update a project README with its description, folder structure, requirements, installation, execution, and troubleshooting. Use for documenting an exercise in Programacion-Asistida and applying its numbering and optional PDF delivery conventions.
---

# Academic Project README

Create concise, evidence-based project documentation. This skill documents the
selected project; it does not implement features or reorganize the repository.

## Read before writing

1. Resolve the target exercise and the user's requested deliverables. Treat each
   exercise as a separate project. Locate the repository root and read applicable
   `AGENTS.md` files before inspecting source or writing documentation.
2. Read [repository conventions](references/repository-conventions.md) for folder
   numbering, the repository index, README links, and optional PDF requirements.
3. Inspect the target's assignment, existing README, source entry points,
   manifests, configuration, relevant tests, and available evidence. Ignore
   environments, caches, generated files, and lockfile internals unrelated to
   the documented dependencies. Preserve existing attribution and assignment text.
4. Read [the README template](references/readme-template.md). Adapt it to the
   project rather than copying instructions or empty placeholders into the result.

## Write the README

Use the language requested by the user; otherwise follow the target project's
documentation policy. Keep identifiers, commands, keys, and paths unchanged.
Include these six sections, even for a project that only contains documents:

1. **Descripción del proyecto:** explain the goal and actual result, with a small
   example when it makes the behavior clearer. Distinguish implemented features
   from proposals and branch-only work.
2. **Estructura de las carpetas:** show a short tree of real files and explain the
   responsibilities that matter. Show hidden skill directories when relevant;
   omit `.venv`, `__pycache__`, `node_modules`, and generated clutter.
3. **Preparación de dependencias y requerimientos:** identify supported runtime
   versions from manifests and distinguish declared, locked, and verified
   installed versions. If there is no executable app, say which tool reads the
   documentation and that no project package installation is needed.
4. **Modo de instalación:** provide commands from the correct directory using
   the project's existing package manager. Do not add or install dependencies
   merely to document them. Keep credentials out of examples.
5. **Modo de ejecución:** provide the real entry point or a usable document/skill
   workflow. Describe an expected result. Separate commands executed during this
   task from instructions a reader can run later.
6. **Troubleshooting:** pair concrete symptoms with checks and remedies grounded
   in the project, such as the working directory, runtime, missing dependencies,
   tool permissions, or known service conflicts. Label untested remedies as
   suggestions. Avoid generic filler or destructive reset commands.

Add evidence, sources, or deliverable links only when they help assess the work.
Keep the six required sections easy to find. Preserve useful existing content
when updating a README and remove stale claims only after checking the project.

## Scope of changes

- Write the target README and the supporting documents the user requested.
- For a new exercise folder, allocate its number from actual sibling directories
  using the conventions reference. Never rename an existing exercise to fix its
  spelling or ordinal suffix.
- Update the root index only when requested or included in the authorized scope.
  Documenting one exercise does not authorize rewriting the repository README.
- Create a PDF only when requested or required by that exercise. A README task
  does not automatically require a PDF. Follow the PDF procedure in the reference
  and verify the rendered result before claiming completion.
- Do not change program behavior, dependencies, historical dates, or unrelated
  exercises to make documentation appear consistent. Report discrepancies.

## Validate and report

Check every relative link, tree entry, and command against the target. Verify the
six sections are present, remove unused placeholders, and ensure no secrets or
invented results remain. Review diffs for scope. Run existing safe checks when
they substantiate a claim; do not start services or external actions solely for
a README without appropriate task authorization. Report generated files and
meaningful limitations, including whether OpenCode actually loaded the skill.
