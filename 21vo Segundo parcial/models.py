# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-10-09 19:59:10
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-10-09 20:11:16

"""Represent expenses and their reusable category tags."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP


@dataclass
class Category:
    """Represent one reusable expense tag."""

    name: str
    id: int | None = None

    def validate(self) -> None:
        """Reject a blank tag name."""
        if not self.name.strip():
            raise ValueError("Escribe un nombre para la etiqueta.")


@dataclass
class Expense:
    """Represent an expense with one or more saved tags."""

    date: date | None
    categories: list[Category]
    amount_cents: int
    description: str = ""
    id: int | None = None

    def validate(self) -> None:
        """Require a date, saved tags, and a positive amount in cents."""
        if not isinstance(self.date, date):
            raise ValueError("Selecciona la fecha del gasto.")
        if not self.categories:
            raise ValueError("Selecciona al menos una etiqueta.")
        for category in self.categories:
            category.validate()
            if category.id is None:
                raise ValueError(
                    "Selecciona etiquetas que ya estén guardadas."
                )
        if not isinstance(self.amount_cents, int) or self.amount_cents <= 0:
            raise ValueError("El monto debe ser mayor que cero.")


def to_cents(amount: float) -> int:
    """Round a finite monetary input to integer cents."""
    value = Decimal(str(amount))
    if not value.is_finite():
        raise ValueError("Escribe un monto válido.")
    return int((value * 100).to_integral_value(rounding=ROUND_HALF_UP))


def category_totals(expenses: list[Expense]) -> dict[str, int]:
    """Split each expense into stable tag shares without losing cents."""
    totals = {}
    for expense in expenses:
        expense.validate()
        tags = sorted(expense.categories, key=lambda tag: tag.id)
        share, remainder = divmod(expense.amount_cents, len(tags))
        for index, tag in enumerate(tags):
            extra_cent = 1 if index < remainder else 0
            totals[tag.name] = totals.get(tag.name, 0) + share + extra_cent
    return totals
