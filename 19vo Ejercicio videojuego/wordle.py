"""Reglas y vocabulario del comodín Wordle."""

from __future__ import annotations

import random
import unicodedata

MIN_WORD_LENGTH = 5
MAX_WORD_LENGTH = 10
MAX_ATTEMPTS = 6

SPANISH_WORDS = (
    "amigo", "arbol", "avion", "barco", "brisa", "campo", "canto", "cielo",
    "claro", "clase", "coche", "color", "dulce", "feliz", "fruta", "hogar",
    "joven", "libro", "llave", "madre", "mundo", "noche", "papel", "pared",
    "perro", "playa", "queso", "reloj", "sabor", "sueño", "tecla", "trigo",
    "valor", "verde", "viaje", "vuelo", "animal", "bosque", "buscar", "cabeza",
    "camino", "camisa", "ciudad", "comida", "cuerpo", "dinero", "fuerte", "jardin",
    "lengua", "madera", "musica", "pelota", "piedra", "puente", "rapido", "sombra",
    "sonido", "tomate", "verdad", "alegria", "caballo", "castigo", "colores", "cultura",
    "cuidado", "familia", "hormiga", "lectura", "montaña", "naranja", "pintura", "secreto",
    "sonrisa", "tarjeta", "trabajo", "ventana", "aventura", "castillo", "estrella", "juguetes",
    "mariposa", "montañas", "sombrero", "tesorera", "valiosos", "viajeros", "volcanes", "caminante",
    "carretera", "esperanza", "escaleras", "girasoles", "maravilla", "marineros", "personaje", "primavera",
    "serpiente", "biblioteca", "calendario", "compañeros", "despedidas", "dinosaurio", "estudiante", "explorador",
    "imaginario", "naturaleza", "revolucion", "tecnologia",
)

_WORD_SET = frozenset(SPANISH_WORDS)

CORRECT = "correct"
PRESENT = "present"
ABSENT = "absent"


def normalize_word(word: str) -> str:
    """Ignore case and written accents while keeping ñ as a distinct letter."""
    decomposed = unicodedata.normalize("NFD", word.strip().casefold())
    letters: list[str] = []
    for character in decomposed:
        if unicodedata.combining(character):
            if character == "\u0303" and letters and letters[-1] == "n":
                letters[-1] = "ñ"
            continue
        letters.append(character)
    return "".join(letters)


def _known_word(word: str) -> str:
    normalized = normalize_word(word)
    if not normalized or any(not ("a" <= letter <= "z" or letter == "ñ") for letter in normalized):
        raise ValueError("La palabra solo puede contener letras del español.")
    if not MIN_WORD_LENGTH <= len(normalized) <= MAX_WORD_LENGTH:
        raise ValueError("La palabra debe tener entre 5 y 10 letras.")
    if normalized not in _WORD_SET:
        raise ValueError("La palabra no está en la lista disponible.")
    return normalized


def new_game(target: str | None = None) -> dict:
    """Create an isolated game, optionally with a deterministic target."""
    answer = _known_word(target if target is not None else random.choice(SPANISH_WORDS))
    return {"target": answer, "guesses": [], "status": "playing"}


def evaluate_guess(target: str, guess: str) -> list[str]:
    """Return Wordle colors, counting exact matches before misplaced letters."""
    target = normalize_word(target)
    guess = normalize_word(guess)
    if len(target) != len(guess):
        raise ValueError("La palabra debe tener la misma cantidad de letras que el objetivo.")

    feedback = [ABSENT] * len(guess)
    remaining: dict[str, int] = {}
    for index, (letter, answer_letter) in enumerate(zip(guess, target)):
        if letter == answer_letter:
            feedback[index] = CORRECT
        else:
            remaining[answer_letter] = remaining.get(answer_letter, 0) + 1

    for index, letter in enumerate(guess):
        if feedback[index] == ABSENT and remaining.get(letter, 0):
            feedback[index] = PRESENT
            remaining[letter] -= 1
    return feedback


def submit_guess(game: dict, guess: str) -> list[str]:
    """Validate and record a guess, updating the game outcome in place."""
    if game["status"] != "playing":
        raise ValueError("Esta partida ya terminó.")

    normalized = _known_word(guess)
    if len(normalized) != len(game["target"]):
        raise ValueError(f"La palabra debe tener {len(game['target'])} letras.")

    feedback = evaluate_guess(game["target"], normalized)
    game["guesses"].append({"word": normalized, "feedback": feedback})
    if normalized == game["target"]:
        game["status"] = "won"
    elif len(game["guesses"]) == MAX_ATTEMPTS:
        game["status"] = "lost"
    return feedback
