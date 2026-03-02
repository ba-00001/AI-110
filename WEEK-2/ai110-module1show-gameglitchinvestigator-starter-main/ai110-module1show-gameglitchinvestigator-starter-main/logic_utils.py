def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 200),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    cleaned = str(raw).strip()
    if not cleaned:
        return False, None, "Enter a guess."

    if "." in cleaned:
        return False, None, "Use a whole number."

    try:
        value = int(cleaned)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "Correct!"

    if guess > secret:
        return "Too High", "Go LOWER!"

    return "Too Low", "Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = max(100 - 10 * (attempt_number - 1), 10)
        return current_score + points

    if outcome in {"Too High", "Too Low"}:
        return max(current_score - 5, 0)

    return current_score
