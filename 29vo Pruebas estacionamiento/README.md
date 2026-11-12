# Exercise 29: Parking toll tests and coverage

Author: Jonathan Serna. Academic report date: November 12, 2026.

This exercise checks the supplied `calculate_toll` function against its
specification. The implementation and specification are byte-for-byte copies of
the supplied files. Their original attribution and dates remain unchanged.

The Spanish report uses the cover, Letter page size, Arial typography, margins,
numbered sections, and footer style of exercise 28:
[Academic report](../PDFs%20ejercicios/Ejercicio_29_Pruebas_estacionamiento.pdf).

## Files

- `Specification.md`: original requirements.
- `parking_lot.py`: original implementation, unchanged.
- `test_initial.py`: exactly three initial unit tests.
- `test_generated.py`: 31 additional specification-based tests from a separate
  AI agent that did not receive the implementation.
- `docs/ai-request.md`: exact generation request and follow-up.
- `evidence/initial/`: initial test log, exit code, and annotated coverage.
- `evidence/full/`: complete test log, exit code, and annotated coverage.
- `evidence/summary.json`: checked results and original-file SHA-256 values.
- `docs/report/build_report.py`: PDF generator using the already available
  ReportLab runtime; it is not needed to execute the tests.
- `docs/report/validation.json`: report and source validation results.

## Run the tests

The recorded runs used Python 3.12.14. No test dependencies need installation;
`unittest` and `trace` are part of the standard library. From this directory:

```powershell
python -B -m unittest -v test_initial
python -B -m unittest -v test_initial test_generated
```

The initial command passes all 3 tests and returns 0. The complete command runs
34 tests: 24 pass and 10 fail, with exit code 1 and no execution errors. These
failures expose specification violations in the supplied implementation. They
are not suppressed or marked as expected failures.

## Reproduce line coverage

These PowerShell commands keep the recorded evidence intact by using new output
directories. Each `python -B -m trace` invocation is a single command line.

```powershell
$stdlibPath = python -c "import sysconfig; print(sysconfig.get_path('stdlib'))"
python -B -m trace --count --missing --summary --ignore-dir $stdlibPath --coverdir evidence/reproduced-initial --module unittest -v test_initial
python -B -m trace --count --missing --summary --ignore-dir $stdlibPath --coverdir evidence/reproduced-full --module unittest -v test_initial test_generated
```

Read the `parking_lot` row and `parking_lot.cover`. Test-file coverage is not the
target metric. Numeric prefixes are execution counts; `>>>>>>` marks an
unexecuted executable line. The counts include module loading.

| Suite | Tests | Passed | Failed | Covered lines | Line coverage |
| --- | ---: | ---: | ---: | ---: | ---: |
| Initial | 3 | 3 | 0 | 13 / 19 | 68.42% |
| Complete | 34 | 24 | 10 | 19 / 19 | 100% |

`trace` displays the initial percentage as 68% because its summary uses whole
numbers. Branch coverage was not measured. A failing assertion still counts as
executing the production lines it reached. Full line coverage does not imply
that the implementation meets its specification.

The trace CLI catches `SystemExit`, so it can return 0 even when `unittest`
reports failures. Use the separate unittest command and its exit code to assess
success. The stored `test-exit-code.txt` files come from those separate runs.

## Findings and scope

Seven failures expose the $200 cap where the specification requires $150.
Three failures expose acceptance of `pension`: free stays return before vehicle
validation, and paid stays have an unsupported `pension` branch. Ordinary rates,
hour rounding, the valid free period, weekend surcharges, and rejection of
`truck` at 60 minutes pass the included cases.

The 15-minute rule is treated as a free-stay threshold, not a deduction from a
longer stay. Thus 61 minutes of auto parking costs $40. Invalid vehicles must
raise `ValueError` even during the free period because the specification gives
no exception. Inputs outside the published contract are not assigned new
requirements. No implementation fixes, dependencies, or unrelated exercises
were changed.

## References

- Supplied `Specification.md` and `parking_lot.py`.
- [Python 3.12 unittest](https://docs.python.org/3.12/library/unittest.html).
- [Python 3.12 trace](https://docs.python.org/3.12/library/trace.html).
