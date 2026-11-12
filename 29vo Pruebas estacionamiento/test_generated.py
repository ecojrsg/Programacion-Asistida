# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-11-12 10:32:58
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-11-12 10:32:58

"""Test parking tolls against the published specification."""

import unittest

from parking_lot import calculate_toll


class GeneratedTollTests(unittest.TestCase):
    """Verify duration boundaries, vehicle rates, surcharges, and caps."""

    def test_zero_minutes_are_free(self):
        """Charge nothing for a zero-minute stay."""
        self.assertEqual(calculate_toll(0), 0)

    def test_fourteen_minutes_are_free(self):
        """Charge nothing below the free-duration threshold."""
        self.assertEqual(calculate_toll(14), 0)

    def test_sixteen_minutes_cost_one_auto_hour(self):
        """Charge one auto hour immediately after the free period."""
        self.assertEqual(calculate_toll(16), 20)

    def test_sixty_minutes_cost_one_auto_hour(self):
        """Charge one auto hour at the first full-hour boundary."""
        self.assertEqual(calculate_toll(60), 20)

    def test_sixty_one_minutes_cost_two_auto_hours(self):
        """Charge two hours without subtracting the free threshold."""
        self.assertEqual(calculate_toll(61), 40)

    def test_one_hundred_twenty_minutes_cost_two_auto_hours(self):
        """Charge two auto hours at the second full-hour boundary."""
        self.assertEqual(calculate_toll(120), 40)

    def test_one_hundred_twenty_one_minutes_cost_three_auto_hours(self):
        """Round a fraction beyond two hours up to three auto hours."""
        self.assertEqual(calculate_toll(121), 60)

    def test_sixteen_moto_minutes_cost_ten(self):
        """Apply the published moto example."""
        self.assertEqual(calculate_toll(16, "moto"), 10)

    def test_sixty_one_moto_minutes_cost_twenty(self):
        """Round a moto stay beyond one hour up to two hours."""
        self.assertEqual(calculate_toll(61, "moto"), 20)

    def test_sixteen_auto_weekend_minutes_cost_thirty(self):
        """Increase the auto hourly rate by fifty percent."""
        self.assertEqual(calculate_toll(16, "auto", True), 30)

    def test_one_hundred_twenty_auto_weekend_minutes_cost_sixty(self):
        """Apply the published auto weekend example."""
        self.assertEqual(calculate_toll(120, "auto", True), 60)

    def test_sixteen_moto_weekend_minutes_cost_fifteen(self):
        """Increase the moto hourly rate by fifty percent."""
        self.assertEqual(calculate_toll(16, "moto", True), 15)

    def test_fifteen_moto_weekend_minutes_are_free(self):
        """Preserve the free period for motos on weekends."""
        self.assertEqual(calculate_toll(15, "moto", True), 0)

    def test_auto_before_cap(self):
        """Charge seven auto hours below the maximum toll."""
        self.assertEqual(calculate_toll(420, "auto"), 140)

    def test_auto_first_capped_minute(self):
        """Cap the first rounded auto charge above the maximum."""
        self.assertEqual(calculate_toll(421, "auto"), 150)

    def test_auto_after_capped_hour(self):
        """Keep a longer auto stay at the maximum toll."""
        self.assertEqual(calculate_toll(481, "auto"), 150)

    def test_moto_before_cap(self):
        """Charge fourteen moto hours below the maximum toll."""
        self.assertEqual(calculate_toll(840, "moto"), 140)

    def test_moto_at_cap(self):
        """Allow a moto charge equal to the maximum toll."""
        self.assertEqual(calculate_toll(900, "moto"), 150)

    def test_moto_above_cap(self):
        """Cap the moto charge after fifteen hours."""
        self.assertEqual(calculate_toll(901, "moto"), 150)

    def test_auto_weekend_before_cap(self):
        """Charge four weekend auto hours below the maximum."""
        self.assertEqual(calculate_toll(240, "auto", True), 120)

    def test_auto_weekend_at_cap(self):
        """Allow five weekend auto hours to reach the maximum."""
        self.assertEqual(calculate_toll(300, "auto", True), 150)

    def test_auto_weekend_above_cap(self):
        """Apply the maximum after the auto weekend surcharge."""
        self.assertEqual(calculate_toll(301, "auto", True), 150)

    def test_moto_weekend_before_cap(self):
        """Charge nine weekend moto hours below the maximum."""
        self.assertEqual(calculate_toll(540, "moto", True), 135)

    def test_moto_weekend_at_cap(self):
        """Allow ten weekend moto hours to reach the maximum."""
        self.assertEqual(calculate_toll(600, "moto", True), 150)

    def test_moto_weekend_above_cap(self):
        """Apply the maximum after the moto weekend surcharge."""
        self.assertEqual(calculate_toll(601, "moto", True), 150)

    def test_day_long_auto_stay_is_capped(self):
        """Apply one maximum toll to a full-day auto stay."""
        self.assertEqual(calculate_toll(1440, "auto"), 150)

    def test_week_long_moto_stay_is_capped(self):
        """Keep a multi-day moto stay under one maximum toll."""
        self.assertEqual(calculate_toll(10080, "moto"), 150)

    def test_pension_is_invalid_at_zero_minutes(self):
        """Reject pension even when the stay has zero duration."""
        with self.assertRaises(ValueError):
            calculate_toll(0, "pension")

    def test_pension_is_invalid_at_fifteen_minutes(self):
        """Reject pension at the free-duration boundary."""
        with self.assertRaises(ValueError):
            calculate_toll(15, "pension")

    def test_pension_is_invalid_for_paid_stays(self):
        """Reject pension when a valid vehicle would be charged."""
        with self.assertRaises(ValueError):
            calculate_toll(60, "pension")

    def test_truck_is_invalid(self):
        """Reject another vehicle outside the two supported types."""
        with self.assertRaises(ValueError):
            calculate_toll(60, "truck")
