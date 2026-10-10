# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-10-09 19:26:38
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-10-09 20:11:16

"""Display FinanzApp's expense forms and reusable tags."""

import logging
import sqlite3
from pathlib import Path

import streamlit as st

from models import Category, Expense, category_totals, to_cents
from storage import ExpenseStore


def notify(message: str) -> None:
    """Keep a success message visible after refreshing the page."""
    st.session_state["notice"] = message
    st.rerun()


def show_categories(store: ExpenseStore, categories: list[Category]) -> None:
    """Show the form for creating a reusable tag."""
    with st.expander("Agregar una etiqueta", expanded=not categories):
        with st.form("category_form"):
            name = st.text_input("Nombre de la etiqueta", key="category_name")
            submitted = st.form_submit_button(
                "Agregar etiqueta", key="add_category"
            )
        if submitted:
            try:
                category = store.add_category(name)
                notify(f"Etiqueta «{category.name}» guardada.")
            except ValueError as error:
                st.error(str(error))


def expense_form(
    categories: list[Category], expense: Expense | None = None
) -> Expense | None:
    """Read submitted fields for a new or existing expense."""
    key = f"expense_{expense.id}" if expense else "new_expense"
    category_by_id = {category.id: category for category in categories}
    names = {category.id: category.name for category in categories}
    with st.form(key):
        expense_date = st.date_input(
            "Fecha", value=expense.date if expense else None, key=f"{key}_date"
        )
        selected = st.multiselect(
            "Etiquetas",
            options=list(names),
            default=[tag.id for tag in expense.categories] if expense else [],
            format_func=names.get,
            key=f"{key}_tags",
        )
        amount = st.number_input(
            "Monto",
            min_value=0.0,
            value=expense.amount_cents / 100 if expense else 0.0,
            step=0.01,
            format="%.2f",
            key=f"{key}_amount",
        )
        description = st.text_input(
            "Descripción (opcional)",
            value=expense.description if expense else "",
            key=f"{key}_description",
        )
        submitted = st.form_submit_button(
            "Guardar cambios" if expense else "Guardar gasto",
            type="primary",
            key=f"{key}_save",
        )
    if not submitted:
        return None
    return Expense(
        expense_date,
        [category_by_id[category_id] for category_id in selected],
        to_cents(amount),
        description.strip(),
        expense.id if expense else None,
    )


def show_new_expense(
    store: ExpenseStore, categories: list[Category]
) -> None:
    """Validate and save the expense entry form."""
    st.subheader("Registrar un gasto")
    if not categories:
        st.info("Agrega una etiqueta antes de registrar tu primer gasto.")
    try:
        expense = expense_form(categories)
        if expense is not None:
            store.add(expense)
            notify("Gasto registrado.")
    except ValueError as error:
        st.error(str(error))


def show_expenses(store: ExpenseStore) -> list[Expense]:
    """Filter expenses and display each one as a single table row."""
    st.subheader("Consultar gastos")
    st.caption("Deja ambas fechas vacías para mostrar todos los gastos.")
    with st.form("date_filter"):
        left, right = st.columns(2)
        start_date = left.date_input(
            "Fecha inicial", value=None, key="start_date"
        )
        end_date = right.date_input("Fecha final", value=None, key="end_date")
        st.form_submit_button("Aplicar filtro", key="apply_filter")
    try:
        expenses = store.list_expenses(start_date, end_date)
    except ValueError as error:
        st.error(str(error))
        st.stop()

    if not expenses:
        st.info("No hay gastos para mostrar.")
        return []
    rows = [
        {
            "ID": expense.id,
            "Fecha": expense.date,
            "Etiquetas": ", ".join(tag.name for tag in expense.categories),
            "Monto": expense.amount_cents / 100,
            "Descripción": expense.description,
        }
        for expense in expenses
    ]
    st.dataframe(
        rows,
        hide_index=True,
        width="stretch",
        column_config={
            "Fecha": st.column_config.DateColumn(format="DD/MM/YYYY"),
            "Monto": st.column_config.NumberColumn(format="%.2f"),
        },
    )
    return expenses


def clear_delete_confirmation() -> None:
    """Require fresh deletion approval after selection or data changes."""
    st.session_state["confirm_delete"] = False


def show_editor(
    store: ExpenseStore, categories: list[Category], expenses: list[Expense]
) -> None:
    """Edit a displayed expense or delete it after explicit confirmation."""
    st.subheader("Editar o eliminar un gasto")
    expense_by_id = {expense.id: expense for expense in expenses}
    selected_id = st.selectbox(
        "ID del gasto",
        options=list(expense_by_id),
        index=None,
        placeholder="Selecciona un gasto de la tabla",
        key="selected_expense",
        on_change=clear_delete_confirmation,
    )
    if selected_id not in expense_by_id:
        return
    try:
        updated = expense_form(categories, expense_by_id[selected_id])
        if updated is not None:
            store.update(updated)
            notify("Gasto actualizado.")
    except ValueError as error:
        st.error(str(error))

    confirmed = st.checkbox(
        f"Confirmo que quiero eliminar el gasto #{selected_id}.",
        key="confirm_delete",
    )
    if st.button(
        "Eliminar gasto", disabled=not confirmed, key="delete_expense"
    ):
        try:
            store.delete(selected_id)
            notify("Gasto eliminado.")
        except ValueError as error:
            st.error(str(error))


def show_chart(expenses: list[Expense]) -> None:
    """Chart allocated tag totals from the exact displayed expense list."""
    st.subheader("Gasto por etiqueta")
    st.caption(
        "Si un gasto tiene varias etiquetas, su monto se reparte entre ellas. "
        "Los centavos sobrantes se asignan en el orden de creación de las "
        "etiquetas. El total de las barras coincide con el total de la tabla."
    )
    totals = category_totals(expenses)
    st.bar_chart(
        [
            {"Etiqueta": name, "Monto": cents / 100}
            for name, cents in totals.items()
        ],
        x="Etiqueta",
        y="Monto",
        y_label="Monto repartido",
        alt="Monto repartido por etiqueta de los gastos de la tabla.",
    )


def main() -> None:
    """Open the database and display the available expense controls."""
    st.set_page_config(page_title="FinanzApp")
    st.title("FinanzApp")
    st.write("Controla tus gastos personales.")
    if "notice" in st.session_state:
        st.success(st.session_state.pop("notice"))
        clear_delete_confirmation()

    store = ExpenseStore(Path(__file__).resolve().parent / "data/finanzapp.db")
    store.initialize()
    categories = store.list_categories()
    show_categories(store, categories)
    show_new_expense(store, categories)
    expenses = show_expenses(store)
    if expenses:
        show_editor(store, categories, expenses)
        show_chart(expenses)


if __name__ == "__main__":
    try:
        main()
    except sqlite3.Error:
        logging.exception("Could not access the expense database.")
        st.error("No se pudo acceder a la base de datos. Intenta de nuevo.")
