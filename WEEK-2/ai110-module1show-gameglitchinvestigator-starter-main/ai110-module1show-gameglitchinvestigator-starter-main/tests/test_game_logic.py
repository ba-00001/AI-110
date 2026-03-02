from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from logic_utils import (
    check_guess,
    describe_distance,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "Correct!"


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "Go LOWER!"


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "Go HIGHER!"


def test_parse_guess_rejects_decimal_input():
    ok, guess, err = parse_guess("12.5")
    assert ok is False
    assert guess is None
    assert err == "Use a whole number."


def test_parse_guess_accepts_trimmed_integer_input():
    ok, guess, err = parse_guess(" 42 ")
    assert ok is True
    assert guess == 42
    assert err is None


def test_hard_mode_range_is_larger_than_normal():
    assert get_range_for_difficulty("Hard") == (1, 200)


def test_win_score_rewards_faster_guess():
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 5) == 60


def test_wrong_guess_score_does_not_go_below_zero():
    assert update_score(0, "Too High", 1) == 0
    assert update_score(10, "Too Low", 2) == 5


def test_parse_guess_accepts_negative_integer_input():
    ok, guess, err = parse_guess("-7")
    assert ok is True
    assert guess == -7
    assert err is None


def test_parse_guess_rejects_large_non_numeric_input():
    ok, guess, err = parse_guess("999999999999999999999999x")
    assert ok is False
    assert guess is None
    assert err == "That is not a number."


def test_describe_distance_uses_temperature_bands():
    assert describe_distance(50, 50) == "Exact"
    assert describe_distance(54, 50) == "Hot"
    assert describe_distance(62, 50) == "Warm"
    assert describe_distance(90, 50) == "Cold"
