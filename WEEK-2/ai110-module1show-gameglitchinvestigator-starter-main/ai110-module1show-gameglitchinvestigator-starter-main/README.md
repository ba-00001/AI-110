# Game Glitch Investigator: The Impossible Guesser

## The Situation

This project is a Streamlit number guessing game that started as buggy AI-generated code.
The goal was to debug the app, move the game rules into a reusable logic module, and verify the fixes with pytest.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`
3. Run tests: `pytest`

## Your Mission

1. Play the game and inspect the "Developer Debug Info" panel.
2. Find the broken state and logic behavior.
3. Refactor reusable logic into `logic_utils.py`.
4. Add tests that prove the repairs are working.

## Document Your Experience

- The game asks the player to guess a secret number based on the chosen difficulty range.
- The main bugs at the start were reversed high/low hints, inconsistent comparisons caused by switching the secret number between `int` and `str`, an off-by-one attempt counter, and a broken new-game reset that ignored the selected difficulty.
- I fixed the game by moving `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` into `logic_utils.py`, correcting the hint logic, stabilizing session state resets, and adding pytest coverage for parsing, scoring, and difficulty ranges.

## Demo


## Preview

<img src="https://github.com/user-attachments/assets/6507d5f4-69f6-4874-b366-0ad7fee98d53" alt="Playlist Chaos Preview" width="600" />

<img src="https://github.com/user-attachments/assets/5414a3e2-2cc5-4ba9-b484-1bbb07781d7a" alt="Playlist Chaos Preview" width="600" />

## Stretch Features

- Added enhanced game UI feedback with color-coded "Hot / Warm / Cold" messages after each valid guess.
- Added a sidebar guess-history table that shows the attempt number, guess, result, and heat rating for the current round.
- Added extra edge-case pytest coverage for negative input, invalid large input, and the new distance-label helper logic.
