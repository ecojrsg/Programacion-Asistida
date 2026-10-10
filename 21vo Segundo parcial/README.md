# FinanzApp

A local personal expense tracker developed step by step for university
coursework. Author: Jonathan Serna.

The interface is in Spanish. Code and technical documentation are in English.

## Requirements

- Python 3.14 or newer.
- [uv](https://docs.astral.sh/uv/getting-started/installation/).

## Install and run

Open a terminal in the `21vo Segundo parcial` directory and run:

```powershell
uv sync --locked
uv run streamlit run app.py
```

Open <http://localhost:8501> if the browser does not open automatically.
Stop the application with `Ctrl+C` in the terminal.

`uv` creates the local `.venv` environment and installs the versions recorded
in `uv.lock`. Streamlit is the only direct dependency.

## Use FinanzApp

1. Open **Agregar una etiqueta**, enter its name, and click **Agregar etiqueta**.
   Create the tags you need before using them in an expense.
2. In **Registrar un gasto**, select a date, one or more tags, and a positive
   amount. The description is optional. Click **Guardar gasto**.
3. In **Consultar gastos**, enter both filter dates and click **Aplicar filtro**.
   Both boundary days are included. Leave both dates empty to show all expenses.
4. To edit, select a displayed identifier under **ID del gasto**, change its
   fields or tags, and click **Guardar cambios**.
5. To delete, select the identifier, check the confirmation box, and click
   **Eliminar gasto**. Changing the selection resets deletion approval.

The table and chart refresh after every saved change. Invalid values produce
a message and do not change the stored data.

## Data and tags

The application creates `data/finanzapp.db` automatically. Closing the app
does not erase the database. Its location depends on the project directory,
not the terminal's current directory.

- `expenses`: dates, amounts, descriptions, and identifiers.
- `categories`: reusable tag names and identifiers.
- `expense_categories`: many-to-many links between expenses and tags.

An expense requires at least one tag. The same tag can belong to several
expenses, and one expense can have several tags. Deleting an expense removes
its links but keeps the tags available.

## Chart totals

The chart uses exactly the expenses returned by the table's date filter.
As confirmed by the user, an expense is split equally among its tags:
100.00 with two tags contributes 50.00 to each.

Amounts are stored and added as integer cents. Remaining cents go to the
first tags in identifier order. For example, 10.01 with three tags becomes
3.34, 3.34, and 3.33. The combined bar total equals the filtered table total.

## Check the application

```powershell
uv run python -m unittest discover -s tests -v
```

The suite uses temporary databases and Streamlit's built-in `AppTest`.
It does not change the application's database and needs no extra dependency.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Expense forms, filters, table, editing, deletion, and chart. |
| `models.py` | `Expense`, `Category`, validation, and exact tag totals. |
| `storage.py` | SQLite persistence and transactional tag links. |
| `tests/test_finanzapp.py` | Storage and interface checks. |
| `pyproject.toml` | Project metadata and dependencies. |
| `uv.lock` | Exact dependency versions. |
| `docs/plans/plan.md` | Design, implementation order, and checks. |
| `docs/plans/classes-original.md` | Original Mermaid class diagram. |
| `docs/plans/classes-corrected.md` | Corrected classes and join-table diagram. |
| `docs/plans/diagram-change.md` | Exact requested change and justification. |
| `docs/plans/checks.md` | Results of checks actually performed. |
| `docs/conversación/conversacion.md` | User and assistant conversation record. |

The original diagram remains preserved. The implementation follows the
corrected three-class design requested in the conversation.
