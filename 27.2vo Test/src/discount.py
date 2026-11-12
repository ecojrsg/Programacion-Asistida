# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-10-26 15:59:48
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-10-26 16:04:48
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Developer: .
Creation Date: 2026-10-26.
Description: Applies a discount to a given price based on a percentage.
"""


def apply_discount(price: float, percentage: float) -> float:
    """Return the price after applying a valid discount percentage."""
    if not 0 <= percentage <= 100:
        raise ValueError("Percentage must be between 0 and 100")
    return round(price * (1 - percentage / 100), 2)


def main():
    print(apply_discount(765.6, 3))


if __name__ == "__main__":
    main()