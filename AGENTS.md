# Project Agent Instructions

## Python tasks

Before writing, modifying, reviewing, documenting, or refactoring Python, load
the `hackthon` skill at `.agents/skills/hackthon/SKILL.md`. If a skill
loader is unavailable, read that file directly and follow its instructions.

- Confirm the human author's name before writing Python source for each task.
- Determine the application's language before writing user-facing strings.
- Write identifiers, comments, docstrings, and technical documentation in
  English. Use the application's language for user-facing text.
- Prefer short, descriptive names and small functions with one responsibility.
  Reduce unnecessary lines without sacrificing readability or correctness.
- Consider maintained external libraries when they avoid reinventing the
  wheel. Propose new dependencies before adding or installing them.
- Follow PEP 8, PEP 257, and the skill's final validation checklist.

## Repository boundaries

Treat each exercise directory as a separate project. Read its requirements,
`pyproject.toml` if present, dependencies, and relevant tests before changing it.
Preserve existing authorship, creation dates, licenses, and assignment material.
Do not translate, rename, or refactor unrelated exercises, or edit dependencies
and generated files merely to apply these guidelines across the repository.
