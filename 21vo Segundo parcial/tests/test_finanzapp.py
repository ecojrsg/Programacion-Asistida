# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-10-09 19:59:10
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-10-09 20:11:16

"""Check expense behavior using disposable SQLite databases."""

import sqlite3
import unittest
from contextlib import closing
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from models import Category, Expense, category_totals, to_cents
from storage import ExpenseStore


class FinanzAppTests(unittest.TestCase):
    """Check persistence and the interface without changing user data."""

    def setUp(self) -> None:
        """Create an isolated database for each check."""
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "finanzapp.db"
        self.store = ExpenseStore(self.path)
        self.store.initialize()

    def start_app(self) -> AppTest:
        """Run the interface against this test's temporary database."""
        replacement = patch("storage.ExpenseStore", return_value=self.store)
        replacement.start()
        self.addCleanup(replacement.stop)
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        return AppTest.from_file(str(app_path), default_timeout=30).run()

    def test_initialize_preserves_rows_and_links(self) -> None:
        """Keep saved expenses and tags after repeated initialization."""
        with closing(sqlite3.connect(self.path)) as connection, connection:
            connection.execute("INSERT INTO categories (name) VALUES ('Food')")
            connection.execute(
                "INSERT INTO expenses (date, amount_cents) VALUES (?, ?)",
                ("2026-10-01", 1230),
            )
            connection.execute(
                "INSERT INTO expense_categories VALUES (1, 1)"
            )

        self.store.initialize()
        with closing(sqlite3.connect(self.path)) as connection:
            tables = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
            self.assertEqual(
                {row[0] for row in tables},
                {"expenses", "categories", "expense_categories"},
            )
            self.assertEqual(
                connection.execute(
                    "SELECT amount_cents FROM expenses"
                ).fetchall(),
                [(1230,)],
            )
            self.assertEqual(
                connection.execute(
                    "SELECT * FROM expense_categories"
                ).fetchall(),
                [(1, 1)],
            )

    def test_multiple_tags_survive_reopening(self) -> None:
        """Keep shared tags without duplicating expense rows."""
        food = self.store.add_category("Food")
        campus = self.store.add_category("Campus")
        self.store.add(Expense(date(2026, 10, 1), [food, campus], 1230))
        self.store.add(Expense(date(2026, 10, 2), [food], 770))

        reopened = ExpenseStore(self.path)
        expenses = reopened.list_expenses()
        self.assertEqual(len(expenses), 2)
        self.assertEqual(sum(item.amount_cents for item in expenses), 2000)
        self.assertEqual(expenses[1].categories, [food, campus])
        self.assertEqual(len(reopened.list_categories()), 2)

    def test_category_names_are_required_and_unique(self) -> None:
        """Trim tag names and reject blank or duplicate names."""
        self.assertEqual(self.store.add_category("  Food  ").name, "Food")
        for name in ("", "   ", "Food", "food"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.store.add_category(name)
        self.assertEqual(len(self.store.list_categories()), 1)

    def test_invalid_expenses_are_not_saved(self) -> None:
        """Reject missing required values and nonpositive amounts."""
        food = self.store.add_category("Food")
        for expense in (
            Expense(None, [food], 100),
            Expense(date(2026, 10, 1), [], 100),
            Expense(date(2026, 10, 1), [food], 0),
            Expense(date(2026, 10, 1), [food], -1),
        ):
            with self.subTest(expense=expense), self.assertRaises(ValueError):
                self.store.add(expense)
        self.assertEqual(self.store.list_expenses(), [])

    def test_invalid_links_roll_back_the_expense(self) -> None:
        """Roll back expense insertion for missing or repeated tag links."""
        food = self.store.add_category("Food")
        for tags in ([Category("Missing", 999)], [food, food]):
            with self.subTest(tags=tags):
                with self.assertRaises(sqlite3.IntegrityError):
                    self.store.add(Expense(date(2026, 10, 1), tags, 100))
                with closing(sqlite3.connect(self.path)) as connection:
                    count = connection.execute(
                        "SELECT count(*) FROM expenses"
                    ).fetchone()[0]
                self.assertEqual(count, 0)

    def test_entry_form_validates_and_saves_multiple_tags(self) -> None:
        """Create tags and submit a valid expense after correcting errors."""
        app = self.start_app()
        for name in ("Alimentación", "Universidad"):
            app.text_input("category_name").set_value(name)
            app.button("add_category").click().run()
            self.assertFalse(app.exception)
            self.assertTrue(app.success)

        app.button("new_expense_save").click().run()
        self.assertIn("fecha", app.error[0].value)
        app.date_input("new_expense_date").set_value(date(2026, 10, 1))
        app.button("new_expense_save").click().run()
        self.assertIn("etiqueta", app.error[0].value)

        ids = [tag.id for tag in self.store.list_categories()]
        app.multiselect("new_expense_tags").set_value(ids)
        app.button("new_expense_save").click().run()
        self.assertIn("monto", app.error[0].value)

        app.number_input("new_expense_amount").set_value(10.01)
        app.text_input("new_expense_description").set_value("Lunch")
        app.button("new_expense_save").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.success[0].value, "Gasto registrado.")
        app.run()
        expenses = self.store.list_expenses()
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].amount_cents, 1001)
        self.assertEqual(len(expenses[0].categories), 2)

    def test_date_filter_inclusive_and_invalid_ranges(self) -> None:
        """Include range boundaries and reject missing or reversed dates."""
        food = self.store.add_category("Food")
        for day in (1, 2, 3):
            self.store.add(Expense(date(2026, 10, day), [food], 100))
        filtered = self.store.list_expenses(
            date(2026, 10, 1), date(2026, 10, 2)
        )
        self.assertEqual([item.date.day for item in filtered], [2, 1])
        self.assertEqual(
            len(
                self.store.list_expenses(date(2026, 10, 2), date(2026, 10, 2))
            ),
            1,
        )
        self.assertEqual(
            self.store.list_expenses(date(2026, 11, 1), date(2026, 11, 2)), []
        )
        for start, end in (
            (date(2026, 10, 1), None),
            (None, date(2026, 10, 1)),
            (date(2026, 10, 3), date(2026, 10, 1)),
        ):
            with self.subTest(start=start, end=end):
                with self.assertRaises(ValueError):
                    self.store.list_expenses(start, end)

    def test_filter_form_handles_empty_and_invalid_ranges(self) -> None:
        """Apply date filters to the displayed rows and show range errors."""
        food = self.store.add_category("Food")
        expense_id = self.store.add(Expense(date(2026, 10, 1), [food], 1230))
        self.store.add(Expense(date(2026, 9, 30), [food], 9000))
        app = self.start_app()
        self.assertEqual(len(app.dataframe[0].value), 2)

        app.date_input("start_date").set_value(date(2026, 10, 1))
        app.button("apply_filter").click().run()
        self.assertIn("Completa", app.error[0].value)
        self.assertFalse(app.dataframe)
        app.date_input("end_date").set_value(date(2026, 9, 30))
        app.button("apply_filter").click().run()
        self.assertIn("posterior", app.error[0].value)

        app.date_input("end_date").set_value(date(2026, 10, 1))
        app.button("apply_filter").click().run()
        self.assertEqual(app.dataframe[0].value["ID"].tolist(), [expense_id])
        app.date_input("start_date").set_value(date(2026, 11, 1))
        app.date_input("end_date").set_value(date(2026, 11, 2))
        app.button("apply_filter").click().run()
        self.assertFalse(app.exception)
        self.assertFalse(app.dataframe)
        self.assertIn("No hay gastos", app.info[0].value)

    def test_edit_replaces_tags_and_rolls_back_failed_changes(self) -> None:
        """Update links together with fields and preserve both on failure."""
        food = self.store.add_category("Food")
        campus = self.store.add_category("Campus")
        expense = Expense(date(2026, 10, 1), [food], 1230)
        self.store.add(expense)
        expense.categories = [campus]
        expense.amount_cents = 770
        self.store.update(expense)
        saved = self.store.list_expenses()[0]
        self.assertEqual(saved.categories, [campus])
        self.assertEqual(saved.amount_cents, 770)

        expense.amount_cents = 9999
        expense.categories = [Category("Missing", 999)]
        with self.assertRaises(sqlite3.IntegrityError):
            self.store.update(expense)
        self.assertEqual(self.store.list_expenses()[0], saved)
        expense.categories = [food]
        expense.amount_cents = 0
        with self.assertRaises(ValueError):
            self.store.update(expense)
        self.assertEqual(self.store.list_expenses()[0], saved)

    def test_delete_removes_links_but_keeps_tags(self) -> None:
        """Cascade an expense's links without removing its reusable tags."""
        food = self.store.add_category("Food")
        campus = self.store.add_category("Campus")
        expense_id = self.store.add(
            Expense(date(2026, 10, 1), [food, campus], 1000)
        )
        self.store.delete(expense_id)
        self.assertEqual(self.store.list_expenses(), [])
        self.assertEqual(len(self.store.list_categories()), 2)
        with closing(sqlite3.connect(self.path)) as connection:
            self.assertEqual(
                connection.execute(
                    "SELECT count(*) FROM expense_categories"
                ).fetchone()[0],
                0,
            )
        with self.assertRaises(ValueError):
            self.store.delete(expense_id)

    def test_edit_and_delete_forms_require_confirmation(self) -> None:
        """Recheck editing fields and reset approval on selection changes."""
        food = self.store.add_category("Food")
        campus = self.store.add_category("Campus")
        first = self.store.add(
            Expense(date(2026, 10, 1), [food, campus], 1001)
        )
        second = self.store.add(Expense(date(2026, 10, 2), [food], 2000))
        app = self.start_app()
        app.selectbox("selected_expense").set_value(first).run()
        self.assertTrue(app.button("delete_expense").disabled)
        app.multiselect(f"expense_{first}_tags").set_value([])
        app.button(f"expense_{first}_save").click().run()
        self.assertIn("etiqueta", app.error[0].value)
        self.assertEqual(len(self.store.list_expenses()[1].categories), 2)

        app.multiselect(f"expense_{first}_tags").set_value([food.id])
        app.number_input(f"expense_{first}_amount").set_value(12.50)
        app.button(f"expense_{first}_save").click().run()
        self.assertEqual(app.success[0].value, "Gasto actualizado.")
        table = app.dataframe[0].value.set_index("ID")
        self.assertEqual(table.loc[first, "Monto"], 12.50)
        self.assertEqual(table.loc[first, "Etiquetas"], "Food")

        app.checkbox("confirm_delete").check().run()
        app.selectbox("selected_expense").set_value(second).run()
        self.assertFalse(app.checkbox("confirm_delete").value)
        self.assertTrue(app.button("delete_expense").disabled)
        app.selectbox("selected_expense").set_value(first).run()
        self.assertFalse(app.checkbox("confirm_delete").value)
        app.checkbox("confirm_delete").check().run()
        app.button("delete_expense").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.success[0].value, "Gasto eliminado.")
        self.assertEqual(app.dataframe[0].value["ID"].tolist(), [second])

    def test_edit_outside_the_filter_preserves_the_interval(self) -> None:
        """Keep date filters when an edit moves a row outside the interval."""
        food = self.store.add_category("Food")
        first = self.store.add(Expense(date(2026, 10, 1), [food], 100))
        second = self.store.add(Expense(date(2026, 10, 2), [food], 200))
        app = self.start_app()
        app.date_input("start_date").set_value(date(2026, 10, 1))
        app.date_input("end_date").set_value(date(2026, 10, 31))
        app.button("apply_filter").click().run()
        app.selectbox("selected_expense").set_value(first).run()
        app.date_input(f"expense_{first}_date").set_value(date(2026, 11, 1))
        app.button(f"expense_{first}_save").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.dataframe[0].value["ID"].tolist(), [second])
        self.assertEqual(app.date_input("start_date").value, date(2026, 10, 1))
        self.assertEqual(app.date_input("end_date").value, date(2026, 10, 31))

    def test_chart_allocation_preserves_cents_and_tag_order(self) -> None:
        """Allocate remainders in tag order, even for a one-cent expense."""
        tags = [Category("A", 1), Category("B", 2), Category("C", 3)]
        expense = Expense(date(2026, 10, 1), list(reversed(tags)), 1001)
        self.assertEqual(
            category_totals([expense]), {"A": 334, "B": 334, "C": 333}
        )
        expense.categories = tags
        self.assertEqual(
            category_totals([expense]), {"A": 334, "B": 334, "C": 333}
        )
        expense.amount_cents = 1
        self.assertEqual(category_totals([expense]), {"A": 1, "B": 0, "C": 0})
        self.assertEqual(category_totals([]), {})
        self.assertEqual(to_cents(10.005), 1001)
        with self.assertRaises(ValueError):
            to_cents(float("nan"))

    def test_chart_totals_match_the_filtered_table(self) -> None:
        """Exclude outside dates from the requested monetary example."""
        food = self.store.add_category("Food")
        transport = self.store.add_category("Transport")
        self.store.add(Expense(date(2026, 10, 1), [food], 1230))
        self.store.add(Expense(date(2026, 10, 3), [food], 770))
        self.store.add(Expense(date(2026, 10, 5), [transport], 525))
        self.store.add(Expense(date(2026, 9, 30), [food], 9900))
        expenses = self.store.list_expenses(
            date(2026, 10, 1), date(2026, 10, 5)
        )
        totals = category_totals(expenses)
        self.assertEqual(totals, {"Food": 2000, "Transport": 525})
        self.assertEqual(
            sum(totals.values()), sum(e.amount_cents for e in expenses)
        )

    def test_chart_data_tracks_filter_edit_and_delete(self) -> None:
        """Refresh chart data after filtering, editing, and deletion."""
        food = self.store.add_category("Food")
        campus = self.store.add_category("Campus")
        transport = self.store.add_category("Transport")
        first = self.store.add(
            Expense(date(2026, 10, 1), [food, campus], 1231)
        )
        self.store.add(Expense(date(2026, 10, 3), [food], 770))
        self.store.add(Expense(date(2026, 10, 5), [transport], 525))
        self.store.add(Expense(date(2026, 9, 30), [food], 9900))

        with patch("streamlit.bar_chart") as chart:
            app = self.start_app()
            app.date_input("start_date").set_value(date(2026, 10, 1))
            app.date_input("end_date").set_value(date(2026, 10, 5))
            app.button("apply_filter").click().run()
            rows = chart.call_args.args[0]
            self.assertEqual(
                {row["Etiqueta"]: row["Monto"] for row in rows},
                {"Food": 13.86, "Campus": 6.15, "Transport": 5.25},
            )
            self.assertAlmostEqual(
                sum(row["Monto"] for row in rows),
                app.dataframe[0].value["Monto"].sum(),
            )

            app.selectbox("selected_expense").set_value(first).run()
            app.multiselect(f"expense_{first}_tags").set_value([transport.id])
            app.number_input(f"expense_{first}_amount").set_value(13.00)
            app.button(f"expense_{first}_save").click().run()
            rows = chart.call_args.args[0]
            self.assertEqual(
                {row["Etiqueta"]: row["Monto"] for row in rows},
                {"Food": 7.70, "Transport": 18.25},
            )
            app.checkbox("confirm_delete").check().run()
            app.button("delete_expense").click().run()
            rows = chart.call_args.args[0]
            self.assertEqual(
                {row["Etiqueta"]: row["Monto"] for row in rows},
                {"Food": 7.70, "Transport": 5.25},
            )
            self.assertAlmostEqual(
                sum(row["Monto"] for row in rows),
                app.dataframe[0].value["Monto"].sum(),
            )
            self.assertFalse(app.exception)


if __name__ == "__main__":
    unittest.main()
