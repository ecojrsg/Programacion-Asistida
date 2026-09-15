"""Reservas de salas para un día, sin dependencias externas."""

import re


class BookingCalendar:
    """Administra intervalos [inicio, fin) independientes por sala.

    Acepta horas enteras o cadenas HH:MM. 24:00 solo puede ser fin.
    Las salas distinguen mayúsculas y eliminan espacios exteriores.
    """

    def __init__(self):
        self._bookings = {}

    @staticmethod
    def _to_minutes(value):
        """Convierte una hora válida a minutos desde medianoche."""
        if type(value) is int and 0 <= value <= 24:
            return value * 60
        if isinstance(value, str) and re.fullmatch(r"\d{2}:\d{2}", value):
            hour, minute = map(int, value.split(":"))
            if 0 <= hour < 24 and 0 <= minute < 60:
                return hour * 60 + minute
            if hour == 24 and minute == 0:
                return 1440
        raise ValueError("Usa horas enteras de 0 a 24 o el formato HH:MM.")

    @staticmethod
    def _format_time(minutes):
        """Devuelve una hora de 24 horas con minutos."""
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    def _validate(self, start, end, room):
        """Valida el intervalo y el nombre antes de modificar datos."""
        if not isinstance(room, str) or not room.strip():
            raise ValueError("El nombre de la sala no puede estar vacío.")
        start = self._to_minutes(start)
        end = self._to_minutes(end)
        if not 0 <= start < end <= 1440:
            raise ValueError("El inicio debe ser anterior al fin del día.")
        return start, end, room.strip()

    def book(self, start, end, room):
        """Reserva si los datos son válidos y no existe un traslape."""
        try:
            start, end, room = self._validate(start, end, room)
        except ValueError:
            return False
        bookings = self._bookings.get(room, [])
        if any(start < old_end and old_start < end
               for old_start, old_end in bookings):
            return False
        self._bookings.setdefault(room, []).append((start, end))
        self._bookings[room].sort()
        return True

    def cancel(self, start, end, room):
        """Cancela únicamente una coincidencia exacta de sala y horario."""
        try:
            start, end, room = self._validate(start, end, room)
        except ValueError:
            return False
        bookings = self._bookings.get(room, [])
        if (start, end) not in bookings:
            return False
        bookings.remove((start, end))
        return True

    def get_available_slots(self, room=None):
        """Imprime una tabla y devuelve filas con sala, inicio y fin.

        Sin argumento consulta salas registradas. Una sala nueva que se
        consulte explícitamente aparece libre durante todo el día.
        """
        if room is not None:
            if not isinstance(room, str) or not room.strip():
                raise ValueError("Indica un nombre de sala válido.")
            rooms = [room.strip()]
        else:
            rooms = sorted(self._bookings)
        rows = []
        for name in rooms:
            cursor = 0
            for start, end in self._bookings.get(name, []):
                if cursor < start:
                    rows.append((name, self._format_time(cursor),
                                 self._format_time(start)))
                cursor = end
            if cursor < 1440:
                rows.append((name, self._format_time(cursor), "24:00"))
        width = max([4] + [len(name) for name in rooms])
        print(f"{'Sala':<{width}} | Inicio | Fin")
        print("-" * (width + 17))
        for name, start, end in rows:
            print(f"{name:<{width}} | {start}  | {end}")
        if not rows:
            print("Sin huecos libres o sin salas registradas.")
        return rows
