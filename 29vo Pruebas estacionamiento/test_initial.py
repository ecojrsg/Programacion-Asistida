# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-11-12 10:29:04
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-11-12 10:29:51

"""Check three initial requirements from the parking specification."""

import unittest

from parking_lot import calculate_toll


class InitialTollTests(unittest.TestCase):
    """Check validation, free parking, and a supplied billing example."""

    def test_negative_minutes_raise_value_error(self):
        """Reject a stay with negative minutes."""
        with self.assertRaises(ValueError):
            calculate_toll(-1)

    def test_first_fifteen_minutes_are_free(self):
        """Charge nothing at the end of the free period."""
        self.assertEqual(calculate_toll(15), 0)

    def test_ninety_minutes_cost_forty_for_auto(self):
        """Round ninety minutes up to two billable hours."""
        self.assertEqual(calculate_toll(90), 40)
