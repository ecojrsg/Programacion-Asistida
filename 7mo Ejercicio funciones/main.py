# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-08-28 18:34:57
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-08-28 18:36:22


def main() -> None:
    """Request a number and display whether it is even or odd."""
    number = int(input("Ingrese un número: "))
    if is_pair(number):
        print(f"El número {number} es par.")
    else:
        print(f"El número {number} es impar.")


def is_pair(num: int) -> bool:
    """Determine whether a number is even.

    Args:
        num: Number to check.

    Returns:
        True if the number is even; False otherwise.
    """
    return num % 2 == 0


if __name__ == "__main__":
    main()
