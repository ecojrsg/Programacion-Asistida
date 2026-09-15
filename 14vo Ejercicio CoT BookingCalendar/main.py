"""Demostración reproducible de BookingCalendar."""

from booking_calendar import BookingCalendar


def main():
    calendar = BookingCalendar()
    operations = [
        (8, 10, "Sala 1"),
        (10, 12, "Sala 1"),
        (9, 11, "Sala 1"),
        (14, 16, "Sala 1"),
        (16, 17, "Sala 2"),
        (14, 14, "Sala 1"),
        ("18:30", "19:15", "Sala 2"),
    ]
    for start, end, room in operations:
        result = calendar.book(start, end, room)
        print(f"Reservar {room} ({start}, {end}): {result}")
    print("Cancelar inexistente:", calendar.cancel(9, 11, "Sala 3"))
    print("Cancelar Sala 1 (14, 16):", calendar.cancel(14, 16, "Sala 1"))
    print("\nDisponibilidad después de cancelar:")
    calendar.get_available_slots()


if __name__ == "__main__":
    main()
