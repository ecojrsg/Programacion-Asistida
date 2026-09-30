import pytest

from wordle import (
    ABSENT,
    CORRECT,
    MAX_ATTEMPTS,
    MAX_WORD_LENGTH,
    MIN_WORD_LENGTH,
    PRESENT,
    SPANISH_WORDS,
    evaluate_guess,
    new_game,
    submit_guess,
)


def test_word_list_uses_only_allowed_lengths():
    assert SPANISH_WORDS
    assert all(MIN_WORD_LENGTH <= len(word) <= MAX_WORD_LENGTH for word in SPANISH_WORDS)


def test_word_length_boundaries_are_inclusive():
    assert len(new_game("arbol")["target"]) == MIN_WORD_LENGTH
    assert len(new_game("biblioteca")["target"]) == MAX_WORD_LENGTH
    with pytest.raises(ValueError, match="entre 5 y 10"):
        new_game("gato")
    with pytest.raises(ValueError, match="entre 5 y 10"):
        new_game("abcdefghijk")


def test_guess_must_be_a_known_word_with_target_length():
    game = new_game("papel")

    with pytest.raises(ValueError, match="5 letras"):
        submit_guess(game, "animal")
    with pytest.raises(ValueError, match="lista"):
        submit_guess(game, "xxxxx")
    assert game["guesses"] == []


def test_feedback_marks_exact_misplaced_and_duplicate_letters():
    assert evaluate_guess("papel", "palpa") == [
        CORRECT, CORRECT, PRESENT, PRESENT, ABSENT,
    ]
    assert evaluate_guess("perro", "rrrra") == [
        ABSENT, ABSENT, CORRECT, CORRECT, ABSENT,
    ]


def test_guess_is_case_and_accent_insensitive_but_preserves_enye():
    game = new_game("arbol")
    assert submit_guess(game, "ÁRBOL") == [CORRECT] * 5
    assert game["status"] == "won"

    enye_game = new_game("montaña")
    assert submit_guess(enye_game, "montaña") == [CORRECT] * 7
    assert enye_game["status"] == "won"


def test_win_and_loss_use_at_most_six_attempts():
    winning_game = new_game("papel")
    assert submit_guess(winning_game, "papel") == [CORRECT] * 5
    assert winning_game["status"] == "won"

    losing_game = new_game("papel")
    for attempt in range(MAX_ATTEMPTS):
        submit_guess(losing_game, "barco")
        expected_status = "lost" if attempt == MAX_ATTEMPTS - 1 else "playing"
        assert losing_game["status"] == expected_status
    assert len(losing_game["guesses"]) == MAX_ATTEMPTS
    with pytest.raises(ValueError, match="ya terminó"):
        submit_guess(losing_game, "papel")
