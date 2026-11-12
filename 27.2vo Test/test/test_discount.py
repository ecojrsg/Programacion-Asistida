# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-10-26 16:04:48
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-10-26 16:16:08

"""Tests for the discount calculation."""

import pytest

from discount import apply_discount


def test_apply_discount_examples():
    """Check the two discount examples."""
    assert apply_discount(100, 10) == 90
    assert apply_discount(765.6, 3) == 742.63
    # assert apply_discount(50, 0) == 51


@pytest.mark.parametrize(
    ("price", "percentage", "expected"),
    [
        (100, 5, 95),
        (80, 25, 60),
        (50, 0, 50),
        (25, 100, 0),
    ],
)
def test_apply_discount_combinations(price, percentage, expected):
    """Check several price and discount combinations, including limits."""
    assert apply_discount(price, percentage) == expected


@pytest.mark.parametrize("percentage", [-1, 101])
def test_apply_discount_rejects_invalid_percentage(percentage):
    """Raise ValueError for discounts outside the valid range."""
    with pytest.raises(ValueError):
        apply_discount(100, percentage)
