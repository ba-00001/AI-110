import random

import streamlit as st

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


def reset_round(low: int, high: int) -> None:
    """Start a fresh round using the current difficulty range."""
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []


st.set_page_config(page_title="Glitchy Guesser")

st.title("Game Glitch Investigator")
st.caption("A repaired number guessing game built from an AI-generated starter.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if "secret" not in st.session_state:
    reset_round(low, high)

if st.session_state.difficulty != difficulty:
    # FIX: Reset the round when the user changes difficulty so the secret matches the selected range.
    st.session_state.difficulty = difficulty
    reset_round(low, high)

st.subheader("Make a guess")
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {max(attempt_limit - st.session_state.attempts, 0)}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess")
with col2:
    new_game = st.button("New Game")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIX: Reset the full round state instead of only changing part of session state.
    reset_round(low, high)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    elif guess_int < low or guess_int > high:
        st.error(f"Enter a number between {low} and {high}.")
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX: Refactored comparison logic into logic_utils.py and removed the broken int/string switching.
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint and outcome != "Win":
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! "
                f"The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )

st.divider()
st.caption("Built from a buggy AI draft and repaired with debugging plus tests.")
