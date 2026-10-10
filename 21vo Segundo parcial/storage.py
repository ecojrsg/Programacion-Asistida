# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-10-09 19:59:10
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-10-09 20:11:16

"""Keep expenses, tags, and their links in SQLite."""

import sqlite3
from contextlib import closing
from datetime import date
from pathlib import Path

from models import Category, Expense


class ExpenseStore:
    """Read and change expenses and tags in a local database."""

    def __init__(self, path: str | Path) -> None:
        """Keep the database path for subsequent operations."""
        self.path = Path(path)

    def _connect(self) -> sqlite3.Connection:
        """Open a connection with named columns and foreign keys enabled."""
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        """Create the database tables without removing existing rows."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection, connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    date TEXT NOT NULL,
                    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
                    description TEXT NOT NULL DEFAULT ''
                );
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL COLLATE NOCASE UNIQUE
                        CHECK (length(trim(name)) > 0)
                );
                CREATE TABLE IF NOT EXISTS expense_categories (
                    expense_id INTEGER NOT NULL REFERENCES expenses(id)
                        ON DELETE CASCADE,
                    category_id INTEGER NOT NULL REFERENCES categories(id),
                    PRIMARY KEY (expense_id, category_id)
                );
                """
            )

    def add_category(self, name: str) -> Category:
        """Save a nonempty tag and reject duplicate names."""
        category = Category(name.strip())
        category.validate()
        try:
            with closing(self._connect()) as connection, connection:
                cursor = connection.execute(
                    "INSERT INTO categories (name) VALUES (?)",
                    (category.name,),
                )
                category.id = cursor.lastrowid
        except sqlite3.IntegrityError as error:
            raise ValueError(
                "Ya existe una etiqueta con ese nombre."
            ) from error
        return category

    def list_categories(self) -> list[Category]:
        """Return the saved tags in name order."""
        with closing(self._connect()) as connection:
            rows = connection.execute(
                "SELECT id, name FROM categories ORDER BY name"
            ).fetchall()
        return [Category(row["name"], row["id"]) for row in rows]

    def _save_tags(
        self,
        connection: sqlite3.Connection,
        expense_id: int,
        categories: list[Category],
    ) -> None:
        """Insert an expense's tag links in the current transaction."""
        connection.executemany(
            "INSERT INTO expense_categories VALUES (?, ?)",
            [(expense_id, category.id) for category in categories],
        )

    def add(self, expense: Expense) -> int:
        """Save a valid expense and its tags together."""
        expense.validate()
        with closing(self._connect()) as connection, connection:
            cursor = connection.execute(
                """INSERT INTO expenses (date, amount_cents, description)
                   VALUES (?, ?, ?)""",
                (
                    expense.date.isoformat(),
                    expense.amount_cents,
                    expense.description,
                ),
            )
            expense_id = cursor.lastrowid
            self._save_tags(connection, expense_id, expense.categories)
        expense.id = expense_id
        return expense_id

    def list_expenses(
        self, start_date: date | None = None, end_date: date | None = None
    ) -> list[Expense]:
        """Return tagged expenses inside an optional inclusive date range."""
        if (start_date is None) != (end_date is None):
            raise ValueError("Completa la fecha inicial y la fecha final.")
        if start_date is not None and start_date > end_date:
            raise ValueError(
                "La fecha inicial no puede ser posterior a la final."
            )
        start = start_date.isoformat() if start_date else None
        end = end_date.isoformat() if end_date else None
        with closing(self._connect()) as connection:
            rows = connection.execute(
                """SELECT e.id, e.date, e.amount_cents, e.description,
                          c.id AS category_id, c.name
                   FROM expenses AS e
                   JOIN expense_categories AS link ON link.expense_id = e.id
                   JOIN categories AS c ON c.id = link.category_id
                   WHERE (? IS NULL OR e.date BETWEEN ? AND ?)
                   ORDER BY e.date DESC, e.id DESC, c.id""",
                (start, start, end),
            ).fetchall()

        expenses = {}
        for row in rows:
            if row["id"] not in expenses:
                expenses[row["id"]] = Expense(
                    date=date.fromisoformat(row["date"]),
                    categories=[],
                    amount_cents=row["amount_cents"],
                    description=row["description"],
                    id=row["id"],
                )
            expenses[row["id"]].categories.append(
                Category(row["name"], row["category_id"])
            )
        return list(expenses.values())

    def update(self, expense: Expense) -> None:
        """Replace a valid expense and its tag links in one transaction."""
        expense.validate()
        with closing(self._connect()) as connection, connection:
            cursor = connection.execute(
                """UPDATE expenses
                   SET date = ?, amount_cents = ?, description = ?
                   WHERE id = ?""",
                (
                    expense.date.isoformat(),
                    expense.amount_cents,
                    expense.description,
                    expense.id,
                ),
            )
            if cursor.rowcount != 1:
                raise ValueError("El gasto seleccionado ya no existe.")
            connection.execute(
                "DELETE FROM expense_categories WHERE expense_id = ?",
                (expense.id,),
            )
            self._save_tags(connection, expense.id, expense.categories)

    def delete(self, expense_id: int) -> None:
        """Delete one expense and its links while preserving reusable tags."""
        with closing(self._connect()) as connection, connection:
            cursor = connection.execute(
                "DELETE FROM expenses WHERE id = ?", (expense_id,)
            )
            if cursor.rowcount != 1:
                raise ValueError("El gasto seleccionado ya no existe.")
