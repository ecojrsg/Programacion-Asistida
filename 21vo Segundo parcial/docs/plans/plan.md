# FinanzApp implementation plan

## Goal and agreed choices

Build a local personal expense tracker for university coursework. Keep code
small, readable, and easy to explain in class. Explain each stage and verify
it before moving to the next one.

- Author: Jonathan Serna, confirmed for this task.
- Interface language: Spanish, confirmed by the user.
- Identifiers, comments, docstrings, and technical documentation: English.
- Python: 3.14, using the installed Python 3.14.5.
- Project management: uv.
- Only direct dependency: Streamlit, requested by the user.
- Persistence: SQLite through Python's standard `sqlite3` module.
- Automated checks: Python's standard `unittest` module.
- Interface: one Streamlit page using its built-in widgets and bar chart.

## Implementation boundary

Step 1 and the original diagram were completed and checked before the
requested pause. The user has now requested reusable category tags and a
many-to-many relationship. The original is preserved, and the corrected
diagram and exact request are recorded separately. Steps 3–9 are now
implemented; the final verification record is in `checks.md`.

The user also confirmed equal allocation across tags for the chart. Keep
integer cents and distribute remainders in tag-identifier order so that the
combined bar total remains equal to the filtered table total.

## Small file structure

Create files only when their stage needs them:

```text
app.py
models.py
storage.py
pyproject.toml
uv.lock
README.md
.gitignore
tests/
    test_finanzapp.py
data/
    finanzapp.db
docs/
    plans/
        plan.md
        classes-original.md
        classes-corrected.md
        diagram-change.md
        checks.md
    conversación/
        conversacion.md
```

The corrected design has three classes:

- `Expense`: hold one expense, its selected tags, and validate its values.
- `Category`: represent a reusable tag and validate its name.
- `ExpenseStore`: handle expenses, tags, and their SQLite links.

The `expense_categories` join table has no Python class; it only stores
identifier pairs. The original two-class proposal remains unchanged in
`classes-original.md`.

Use simple functions in `app.py` for the interface. A function that totals
expenses by category can live in `models.py`; it does not need a class.

## Step 1: Prepare the project

Initialize a standalone, unpackaged project in the exercise directory:

```powershell
uv init --bare --name finanzapp --python 3.14 --vcs none --no-workspace
uv add streamlit
```

Create the initial Streamlit page, a local `.gitignore`, and execution
instructions. Keep the dependency lockfile. Use these commands to install
and run the project:

```powershell
uv sync --locked
uv run streamlit run app.py
```

Check the dependency import, server health, and the initial page in a browser.

## Step 2: Define the system structure

Save the Mermaid class diagram and responsibilities in
`classes-original.md`. Verify Mermaid syntax and check that the two classes
cover the requested expense fields and storage operations.

The requested change is documented in `diagram-change.md`. Validate the
corrected class and relationship diagrams in `classes-corrected.md` before
implementing the models.

## Step 3: Store expenses

Create `data/finanzapp.db` automatically at a location based on `app.py`'s
directory. Use `expenses` for identifiers, dates, amounts, and descriptions;
`categories` for reusable tag names; and `expense_categories` for links.

- Store dates as ISO text: `YYYY-MM-DD`.
- Store amounts as integer cents; display monetary units with two decimals.
- Create the table only if it does not exist.
- Use SQL parameters for values.
- Enable foreign keys on each connection and prevent duplicate tag links.
- Keep an expense and its links in one transaction.
- Commit successful writes and close each connection.

Check initial table creation and repeated initialization. Reopening the
database must preserve previously saved rows.

## Step 4: Register an expense

Create a tag-name form and an expense form for date, selected tags, amount,
and description. Require a selected date, at least one existing tag, and a
positive amount. Reject empty or duplicate tag names. The description may
be empty.

Use one validation method for registration and editing. Show confirmation
only after a successful save.

Check a valid entry with multiple tags and reject a missing date, missing
tags, zero, and negative amounts. Invalid submissions must not add rows.

## Step 5: List and filter expenses

Display all expense fields, including the identifier, in a table. Two empty
filter dates mean all expenses. Applying a range requires both dates and
`start_date <= end_date`; include both boundary days.

Show a clear message for an invalid range or no results.

Check an unrestricted list, boundary dates, a single-day range, a missing
range endpoint, reversed dates, and an empty result.

## Step 6: Edit and delete an expense

Select an identifier from the displayed expenses and load its values into
an editing form. Reuse registration validation. Link deletion confirmation
to the selected identifier.

After a successful update or deletion, read the expenses again while
preserving the date filter. Keep the success message visible after refresh.

Check valid edits, rejected edits, canceled deletion, confirmed deletion,
and an edit that moves a row outside the active range. Changing the selected
identifier must not carry over deletion approval from another expense.

## Step 7: Display the chart

Calculate category totals from the exact expense list used by the filtered
table. Split each amount equally among its tags using integer cents; assign
remaining cents by ascending tag identifier. Convert only for presentation.
Render a bar chart with `st.bar_chart`, explain the allocation rule beside
it, and handle an empty list with a message.

Check each category total and the combined total against the visible rows,
including after editing and deleting an expense.

## Step 8: Verify the application

Use a small `unittest` suite with temporary databases, plus browser checks
of the forms. Cover validation, persistence, inclusive date filtering,
editing, deletion, and agreement between table and chart totals.

Use two Food expenses of 12.30 and 7.70 and one Transport expense of 5.25.
Expect category totals of 20.00 and 5.25. Add an out-of-range expense and
confirm that it is excluded from both the table and chart.

Run the test suite with:

```powershell
uv run python -m unittest discover -s tests -v
```

Record actual check results in `checks.md`. Do not describe planned checks
as passed.

## Step 9: Complete the documentation

Update this plan and the README to match the implemented application. Keep
simple instructions for installation, execution, database location, use of
the forms and filters, and test execution.

## Conversation record

Maintain `docs/conversación/conversacion.md` in place. Preserve user and
assistant message text in order without summarizing or correcting it,
including intermediate updates and question-form exchanges.

The current OpenCode session can be exported to verify the record. Its
session identifier is `ses_edc9c3930ffedWS2lV5Oc62rt9`. Record visible
conversation content, not private reasoning or tool execution details.
State any missing history honestly rather than inventing it.

In OpenCode's terminal interface, `/export` exports the conversation to
Markdown. The CLI can also export the session as JSON:

```powershell
opencode export ses_edc9c3930ffedWS2lV5Oc62rt9
```

## References checked

- [uv projects](https://docs.astral.sh/uv/guides/projects/).
- [Streamlit installation and supported Python versions](https://docs.streamlit.io/get-started/installation/command-line).
- [Streamlit forms](https://docs.streamlit.io/develop/concepts/architecture/forms).
- [Streamlit bar chart](https://docs.streamlit.io/develop/api-reference/charts/st.bar_chart).
- [OpenCode conversation export](https://opencode.ai/docs/tui/#export).

## Final status

- The three-class implementation follows `classes-corrected.md`.
- The original proposal remains in `classes-original.md` without edits.
- All 15 automated checks passed, including isolated Streamlit form checks.
- Python compilation passed after the final line-length cleanup.
- A real browser expense with two tags showed 10.01 in the table and
  allocated bars of 5.01 and 5.00. Temporary demonstration rows were removed.
- Installation, use, persistence, tag allocation, and test commands are
  documented in the README.
- Conversation messages continue in the same conversation file.
