# Verification record

## Step 1: Project setup

- `uv init --bare --name finanzapp --python 3.14 --vcs none --no-workspace`:
  completed in the exercise directory.
- `uv add streamlit`: installed Streamlit 1.65.0 using Python 3.14.5 and
  generated `uv.lock` and the local `.venv` environment.
- `uv sync --locked`: passed; all 37 installed dependencies matched the lock.
- `uv run --locked python -c "import streamlit; print('Streamlit', streamlit.__version__)"`:
  passed; reported Streamlit 1.65.0.
- Started the application with `uv run --locked streamlit run app.py` using
  headless browser options for the check.
- `GET http://localhost:8501/_stcore/health`: returned `ok`.
- Browser check at `http://localhost:8501`: displayed `FinanzApp` and
  `Controla tus gastos personales.`. No browser console warnings or errors
  were reported.

## Step 2: Original class design

- Original Mermaid source saved in `classes-original.md`.
- Mermaid 11 browser validation with `mermaid.parse`: passed and returned
  `diagramType: classDiagram`.
- `mermaid.render`: produced an SVG. The browser accessibility snapshot
  contained both classes, all five expense fields, the validation method,
  the storage methods, and their dependency relationship.
- Requirement review: the five required expense fields are represented;
  the storage class covers creation, registration, date-filtered queries,
  editing, and deletion. The interface and category totals use functions.
- The user requested reusable category tags and a many-to-many relationship.
- The original file is preserved; the correction and exact request are in
  `classes-corrected.md` and `diagram-change.md`.
- Mermaid 11 parsed and rendered both corrected diagrams successfully:
  `classDiagram` and `er`.
- The user confirmed equal allocation of each expense across its tags.

## Conversation record

- Exported the current OpenCode session as JSON and checked its visible
  message history against `docs/conversación/conversacion.md`.
- Included both question-form exchanges, the planning response, the user's
  implementation request, the status question, and intermediate replies.
- Further messages, including this stage's final reply, are appended to
  that same file.

## Step 3: SQLite

- Created `expenses`, `categories`, and `expense_categories`.
- Ran the initial `unittest` check: 1 test passed. Reinitialization kept
  the seeded amount and its tag link.
- Initialized the application's database at `data/finanzapp.db`.

## Step 4: Tags and expense registration

- Ran the expanded suite: 6 tests passed, including Streamlit `AppTest`.
- Created tags, rejected blank and duplicate names, and saved an expense
  with two tags through the form.
- Missing date, missing tags, zero, and negative amounts were rejected.
- Foreign-key failures and repeated links rolled back the entire insertion.
- Reopening SQLite preserved expenses and shared tags without duplicate rows.
- A page rerun did not insert the submitted expense a second time.

## Step 5: Table and date filters

- Ran both date-filter checks: passed after increasing the AppTest startup
  timeout from 10 to 30 seconds. The first UI test had exceeded the 10-second
  limit; the rerun completed successfully.
- Verified inclusive boundary days, a single-day range, missing endpoints,
  reversed dates, and empty results.
- AppTest verified that applying a filter updates the displayed rows and
  that invalid or empty ranges do not leave an old table visible.

## Step 6: Editing and deletion

- All 4 targeted checks passed.
- Valid edits replaced tag links and refreshed table amounts and tags.
- Invalid fields and invalid tag links preserved the original expense and
  links; failed updates rolled back in full.
- Deletion required checkbox approval, which reset when selection changed.
- Deleted expense links were removed while category tags remained reusable.
- Moving an expense outside the current filter removed it from the table
  without clearing the selected date interval.

## Step 7: Chart

- All 3 targeted checks passed.
- Confirmed equal allocation and stable remainder-cent distribution,
  including a one-cent expense with three tags.
- The filtered example produced Food 20.00 and Transport 5.25, excluding
  the outside-range expense.
- AppTest captured the actual data passed to `st.bar_chart` after filtering,
  editing, and deletion; each category and the combined total matched the table.

## Step 8: Combined checks

- Full suite: all 15 tests passed.
- `uv run --locked python -m compileall -q app.py models.py storage.py tests`:
  passed.
- UI detector: reported no findings for `app.py`. This is a mechanical
  result, not a substitute for the browser check.
- Compiled the source again after the final line-length cleanup: passed.
- Python source lines were checked against the 79-character limit.
- Real browser check: created two tags and saved a 10.01 expense through the
  form. The table displayed one row with both tags; the chart's accessible
  bar values were 5.01 and 5.00, preserving the exact total.
- Reopening SQLite during cleanup retrieved the saved expense, its 1001
  cents, and both tag links.
- Reviewed the desktop capture's registration, filter, and table controls.
  The optional mobile capture was not obtained because the browser automation
  connection timed out. No mobile visual pass is claimed.
- Server health still returned `ok` after the automation timeout.
- Removed only the temporary expense and its unused test tags. The database
  returned to its original empty state: 0 expenses and 0 tags.

## Step 9: Documentation

- README reviewed against the implemented forms, database tables, allocation
  rule, and uv execution commands.
- Original and corrected diagrams, the exact requested change, its rationale,
  and this verification record are in `docs/plans`.
- The session was exported again to check the conversation's ordering and
  full user/assistant message text, including the allocation question.
