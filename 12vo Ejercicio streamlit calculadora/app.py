# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-09-01 10:34:56
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-09-01 11:27:14
import streamlit as st


def add(first_number, second_number):
    """Return the sum of two numbers."""
    return first_number + second_number


def subtract(first_number, second_number):
    """Return the difference between two numbers."""
    return first_number - second_number


def multiply(first_number, second_number):
    """Return the product of two numbers."""
    return first_number * second_number


def divide(first_number, second_number):
    """Return the quotient or None when division is invalid."""
    if second_number == 0:
        return None
    return first_number / second_number


def main():
    st.set_page_config(page_title="Calculadora", layout="centered")

    st.title("Calculadora")
    st.caption("Realiza operaciones básicas con dos números.")
    st.divider()

    first_column, second_column = st.columns(2)
    with first_column:
        first_number = st.number_input("Primer número", value=0.0, key="first_number")
    with second_column:
        second_number = st.number_input("Segundo número", value=0.0, key="second_number")

    st.subheader("Operación")
    add_column, subtract_column, multiply_column, divide_column = st.columns(4)

    # Store the selected operation and its result.
    operation = None

    # Each button is placed inside its corresponding column.
    add_clicked = add_column.button("+", use_container_width=True, help="Sumar")
    subtract_clicked = subtract_column.button("-", use_container_width=True, help="Restar")
    multiply_clicked = multiply_column.button("*", use_container_width=True, help="Multiplicar")
    divide_clicked = divide_column.button("/", use_container_width=True, help="Dividir")

    # Render every button before handling the selected operation.
    if add_clicked:
        operation = ("Suma", add(first_number, second_number))
    elif subtract_clicked:
        operation = ("Resta", subtract(first_number, second_number))
    elif multiply_clicked:
        operation = ("Multiplicación", multiply(first_number, second_number))
    elif divide_clicked:
        operation = ("División", divide(first_number, second_number))

    if operation:
        operation_name, result = operation
        # Division by zero has no valid numeric result.
        if result is None:
            st.error("No se puede dividir entre cero.")
        else:
            st.success(f"**{operation_name}:** {result:g}")


if __name__ == "__main__":
    main()
