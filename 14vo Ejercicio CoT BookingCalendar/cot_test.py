#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Developer: Miguel Jara Maldonado.
Creation Date: 2026-08-27.
Description: Unit Tests for the Chain of Thought Booking Calendar code.
"""

from booking_calendar import BookingCalendar


def run_tests():
    calendar = BookingCalendar()

    assert calendar.book(9, 11, "a") is True, "Booking method is incorrect."
    assert calendar.book(10, 12, "b") is True, "Adjacent blocks must be allowed."
    assert calendar.book(11, 12, "b") is False, "Overlap must be rejected."

    calendar.book(14, 14, "d") is True, "Zero-length bookings must be rejected."
    calendar.book(14, 12, "d") is True, "Impossible bookings must be rejected."

    assert (
        calendar.cancel(9, 11, "f") is False
    ), "Unexisting bookings should not be cancelled."
    assert calendar.cancel(9, 11, "a") is True, "Existing bookings can be cancelled."

    calendar.book(8, 10, "Sala 1")
    calendar.book(10, 12, "Sala 1")
    calendar.book(14, 16, "Sala 1")
    calendar.book(16, 17, "Sala 2")
    calendar.get_available_slots()
    print("All tests passed.")


run_tests()

if __name__ == "__main__":
    run_tests()
