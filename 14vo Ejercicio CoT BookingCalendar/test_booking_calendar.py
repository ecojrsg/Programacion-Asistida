"""Pruebas adicionales que complementan el archivo del docente."""

import contextlib
import io
import unittest

from booking_calendar import BookingCalendar


class BookingCalendarTests(unittest.TestCase):
    def setUp(self):
        self.calendar = BookingCalendar()

    def slots(self, room=None):
        with contextlib.redirect_stdout(io.StringIO()):
            return self.calendar.get_available_slots(room)

    def test_overlap_variants(self):
        for start, end in [(9, 11), (8, 10), (10, 12), (8, 12)]:
            with self.subTest(start=start, end=end):
                calendar = BookingCalendar()
                self.assertTrue(calendar.book(9, 11, "A"))
                self.assertFalse(calendar.book(start, end, "A"))

    def test_adjacency(self):
        self.assertTrue(self.calendar.book(9, 11, "A"))
        self.assertTrue(self.calendar.book(11, 12, "A"))
        self.assertTrue(self.calendar.book(8, 9, "A"))

    def test_independent_rooms(self):
        self.assertTrue(self.calendar.book(9, 11, "A"))
        self.assertTrue(self.calendar.book(9, 11, "B"))

    def test_invalid_intervals(self):
        for start, end in [(14, 14), (14, 12), (-1, 2), (23, 25),
                           (True, 2), (1.5, 2), ("9:00", "10:00"),
                           ("12:60", "13:00"), (24, 24), (None, 3)]:
            with self.subTest(start=start, end=end):
                self.assertFalse(self.calendar.book(start, end, "A"))
        self.assertEqual(self.slots(), [])

    def test_invalid_rooms(self):
        for room in ["", "   ", None, 7]:
            self.assertFalse(self.calendar.book(9, 10, room))

    def test_minutes(self):
        self.assertTrue(self.calendar.book("09:15", "10:30", "A"))
        self.assertFalse(self.calendar.book("10:29", "11:00", "A"))
        self.assertTrue(self.calendar.book("10:30", "11:00", "A"))

    def test_cancel_exact(self):
        self.calendar.book(9, 11, "A")
        self.assertFalse(self.calendar.cancel(9, 10, "A"))
        self.assertFalse(self.calendar.cancel(9, 11, "B"))
        self.assertFalse(self.calendar.cancel(None, 11, "A"))
        self.assertTrue(self.calendar.cancel(9, 11, "A"))
        self.assertFalse(self.calendar.cancel(9, 11, "A"))
        self.assertEqual(self.slots("A"), [("A", "00:00", "24:00")])

    def test_sorted_gaps(self):
        for start, end in [(14, 16), (10, 12), (8, 10)]:
            self.calendar.book(start, end, "A")
        self.assertEqual(self.slots("A"), [
            ("A", "00:00", "08:00"), ("A", "12:00", "14:00"),
            ("A", "16:00", "24:00"),
        ])

    def test_full_day(self):
        self.assertTrue(self.calendar.book(0, "24:00", "A"))
        self.assertEqual(self.slots("A"), [])

    def test_unknown_room(self):
        self.assertEqual(self.slots("Nueva"),
                         [("Nueva", "00:00", "24:00")])
        self.assertEqual(self.slots(), [])

    def test_normalized_name(self):
        self.calendar.book(9, 11, " A ")
        self.assertFalse(self.calendar.book(9, 11, "A"))
        self.assertTrue(self.calendar.cancel(9, 11, " A "))

    def test_invalid_query(self):
        with self.assertRaises(ValueError):
            self.slots(" ")

    def test_table_output(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.calendar.get_available_slots("A")
        for text in ["Sala", "Inicio", "Fin", "00:00", "24:00"]:
            self.assertIn(text, output.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
