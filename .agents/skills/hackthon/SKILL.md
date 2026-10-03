---
name: hackthon
description: "Use when writing, modifying, reviewing, documenting, or refactoring Python in this repository. Apply PEP 8 and PEP 257, confirm the header author, write code and documentation in English, detect the language of user-facing strings, consider standard and external libraries, and keep functions short, focused, and easy for software engineering students to understand."
---

# Hackthon: Clear Python for Students

Write Python that a software engineering student can understand without
decoding clever tricks. Correctness comes first; optimize for readability,
one responsibility per function, and the fewest useful lines of executable
code. Fewer lines are not an improvement if they make the code harder to read.

## Workflow

1. Read the request, the relevant exercise, its requirements and configuration,
   the code being changed, its callers, and the applicable tests. Identify the
   supported Python version; do not assume all exercises use the same version.
2. Before a task that writes or modifies Python source, confirm the human
   author's name. A name explicitly supplied for this task is confirmation;
   otherwise ask: "What name should I use for the code header in this task?"
   Ask once per task, not once per file. Never infer the answer from old
   headers, Git configuration, a username, or a previous task. Wait for the
   answer before writing implementation code. Read-only reviews do not need
   this question, and do not persist the answer as the skill's default author.
3. Identify the application's language from the user's requirements, existing
   interface text, localization resources, and project documentation. If it is
   unspecified, mixed without an established localization policy, or ambiguous,
   ask before adding user-facing text. Do not ask about an application language
   for a task that has no user-facing text.
4. Choose the simplest appropriate solution and libraries using the rules
   below. Explain and request approval for a new dependency before adding or
   installing it; do not change manifests or lockfiles on a proposal alone.
5. Write English identifiers and documentation, appropriate headers and
   docstrings, and focused functions. Preserve existing behavior unless a
   behavior change was requested.
6. Run the relevant checks and complete the final checklist. Report what
   changed, what was verified, and any remaining uncertainty briefly.

## 1. PEP 8 and Reliable Research

### Coding conventions

- Use four spaces per indentation level; never mix tabs and spaces.
- Use `snake_case` for variables, functions, and methods, `CapWords` for
  classes, and `UPPER_SNAKE_CASE` for constants.
- Choose short but descriptive English names such as `total`, `user_id`, and
  `task_count`. Avoid opaque abbreviations and generic names such as `tmp` or
  `data` when a more specific name is available. A short mathematical name is
  acceptable when its meaning is immediately clear.
- Group imports as standard library, third-party packages, then local modules,
  with blank lines between groups. Avoid wildcard imports and unused imports.
- Default to 79 characters for code and 72 for flowing comments and docstrings.
  Follow an explicit project formatter or line-length configuration instead of
  introducing a competing style. Wrap with parentheses rather than backslashes.
- Separate top-level functions and classes with two blank lines, and methods
  with one. Use consistent spacing and remove trailing whitespace.
- Compare with `None` using `is` or `is not`. Use truthiness only when empty,
  zero, and missing values genuinely have the same meaning for the operation.
- Avoid mutable default arguments. Use context managers for owned resources,
  and catch specific exceptions without silently discarding failures.
- Use simple type hints when they clarify a contract and are supported by the
  exercise's Python version; avoid elaborate typing abstractions for simple
  code. Accept subclasses with `isinstance` when appropriate, but preserve
  explicit type restrictions, such as rejecting booleans where required.
- Preserve public APIs, external field names, schemas, and assignment-required
  names. Do not rename an existing interface just to satisfy a style rule.

### Where to look when unsure

Start with local requirements, configuration, existing helpers, and tests.
Then consult these primary sources for the actual supported version:

- [PEP 8: Python code style](https://peps.python.org/pep-0008/).
- [PEP 257: Docstring conventions](https://peps.python.org/pep-0257/).
- [Python standard library](https://docs.python.org/3/library/) and
  [built-in functions](https://docs.python.org/3/library/functions.html).
- [Python tutorial](https://docs.python.org/3/tutorial/) and
  [language reference](https://docs.python.org/3/reference/).
- The external package's official documentation, API reference, and release
  notes for the version installed or proposed in the exercise.

Search for the specific question rather than assuming a remembered API or
copying an unverified snippet. If official guidance is insufficient, use a
maintained project's source or tests to verify the behavior. Check edge cases
with a small runnable test. Do not present guesses as best practices. When
documentation or execution is unavailable, state the limitation and use a
verified alternative or ask for the missing context.

## 2. English Code, Headers, and Documentation

### Language boundary

- Write new or materially changed identifiers, comments, docstrings, internal
  log messages, and technical documentation in English.
- Only user-facing text follows the application's language: labels, buttons,
  help text, notifications, and error messages shown to users. Do not assume
  Spanish merely because the conversation or an older exercise uses it.
- Preserve existing localization keys and the application's translation
  mechanism. Do not translate paths, URLs, protocol values, JSON field names,
  or other contractual strings. Preserve proper names and authors' names.
- Translate documentation within the task's scope, not unrelated files. An
  existing required identifier or external contract takes precedence over
  translating a name. Do not silently break compatibility to enforce English.

### File headers

For each new handwritten Python source file, use the repository's header
convention followed by a concise English module docstring:

```python
# -*- coding: utf-8 -*-
# @Author: <confirmed author>
# @Date:   <actual creation timestamp>
# @Last Modified by:   <confirmed author>
# @Last Modified time: <actual modification timestamp>

"""Describe the module's purpose in English."""
```

- This is a template, not ready-to-use metadata. Replace placeholders with the
  confirmed name and actual clock times in `YYYY-MM-DD HH:MM:SS` format. Never
  copy historical timestamps or invent a creation date.
- Keep a required shebang as the first line, before the encoding declaration.
  Keep the module docstring before imports, including `__future__` imports.
- When editing an existing file, preserve its original `@Author` and `@Date`.
  Update modification fields with the confirmed name and actual edit time.
- Preserve `Developer`, copyright, license, and other provenance notices in
  supplied or teacher-authored files. Do not replace the original author with
  the current user merely because the file is being edited.
- If an existing file has no known author or creation date, do not invent
  `@Author` or `@Date`. Add current modification fields when adding a header;
  ask if original-author attribution is required but cannot be established.
- The encoding line is a repository convention, not a Python 3 or PEP 8
  requirement. Do not add this Python header to Markdown or generated files.

### Docstrings and comments

- Document every function or method created or materially changed, along with
  new public modules and classes. Use triple double quotes as the first
  statement of the documented object.
- For a simple function, prefer one short imperative sentence ending in a
  period, such as `"""Return whether the number is even."""`.
- For a non-obvious contract, use a summary, a blank line, and only the relevant
  `Args`, `Returns`, and `Raises` sections. Explain constraints, meaningful
  side effects, and optional values when applicable. Do not duplicate an
  obvious signature or add empty sections to every function.
- These section names follow the project's existing Google-style examples;
  PEP 257 defines docstring conventions, not a mandatory section markup.
- Comments explain why a decision, workaround, or constraint exists, not what
  an obvious statement does. Use `# ` and complete English sentences. Separate
  inline comments from code with at least two spaces and use them sparingly.
- Keep documentation synchronized with actual behavior. Do not retain stale
  descriptions or commented-out implementations added by the current task.

Repository examples, with paths relative to the repository root:

- `7mo Ejercicio funciones/main.py`: metadata header and `Args`/`Returns`
  docstrings.
- `9no Ejercicio clases 2/main.py`: brief docstrings for a class and methods.
- `15vo Skills MCPs/src/mcp_server/ollama_agent_class.py`: supplied `Developer`
  metadata that must remain attributed to its original author.

Use these to recognize local conventions, not to copy names, dates, or every
existing implementation choice.

## 3. Small Functions and Appropriate Libraries

### Do not reinvent the wheel

Consider existing helpers, built-ins and the standard library, already
installed packages, and maintained external packages. Choose the option that
best satisfies correctness and student-readable code with minimal maintenance.
The standard library is a good default, not a prohibition on external tools.

- Prefer well-named built-ins such as `sum`, `min`, `max`, `any`, and `all` when
  their behavior fits the requirement and makes the intent clear.
- Propose an external library when it replaces substantial custom code or
  handles established concerns more clearly and reliably. Do not insist on a
  hand-written standard-library solution merely to avoid a justified package.
- Explain the problem it solves, the readability benefit, the dependency cost,
  and why existing options are insufficient. Check maintenance, licensing,
  Python compatibility, and the documented API. Prefer a familiar, focused
  package over several overlapping dependencies or a large framework.
- Never claim a package is installed, maintained, compatible, or faster without
  checking. Do not add speculative dependencies for possible future features.

### One responsibility, few useful lines

- Describe each function's responsibility in one short sentence. If that
  sentence combines independent jobs, separate the responsibilities when it
  improves understanding. Thin orchestration functions may call focused steps.
- Remove redundant branches, duplicated calculations, unnecessary temporary
  variables, and boilerplate. Use clear early returns to reduce nesting.
- Use a simple comprehension for a straightforward transformation or filter;
  use an explicit loop when conditions or side effects need explanation.
- Prefer explicit, boring control flow over nested comprehensions, stacked
  ternaries, clever lambdas, dynamic dispatch tricks, or dense expressions.
- Do not use semicolons or multiple statements on one line to lower a line
  count. Do not remove useful docstrings, validation, or error handling to make
  a function shorter.
- Avoid arbitrary function-length limits and artificial helper fragmentation.
  Extract a helper for a clear responsibility or useful reuse, not merely to
  hide complexity or satisfy a line quota.
- Do not introduce classes, factories, generic frameworks, configuration
  layers, or abstractions without a concrete need in the current task.
- Prefer suitable, efficient algorithms, but do not micro-optimize readability
  away. Measure before adding performance-driven complexity. Preserve edge
  cases and semantics when replacing code with a shorter expression.

## Final Checklist

Before delivering Python changes, verify:

- The author was confirmed for this task, headers use real timestamps, and
  original attribution and creation dates remain intact.
- Identifiers and documentation are English and understandable; user-facing
  strings follow the established application language.
- Each function has one clear responsibility and no unnecessary executable
  lines. A student can follow it without decoding clever shortcuts.
- Existing solutions and appropriate libraries were considered. Any new
  dependency was proposed and approved before manifests or environments changed.
- PEP 8, PEP 257, the exercise's configuration, and documented APIs were checked.
- Applicable tests and existing lint or format checks were run. For non-trivial
  changed behavior, use an existing test or add a small focused regression
  check; do not introduce a testing framework solely for this skill.
- Validation, error handling, public contracts, and unrelated exercises remain
  unchanged unless the task explicitly required a change.

Use the exercise's existing tools. Do not install a formatter or test framework
just to run a check. If checks cannot run, report that honestly instead of
claiming success. Keep the delivery summary concise and include the checks run.
