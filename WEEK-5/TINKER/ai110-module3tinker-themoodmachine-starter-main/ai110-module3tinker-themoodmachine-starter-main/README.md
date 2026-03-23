# The Mood Machine

The Mood Machine is a sentiment classifier for short posts. This finished version includes a rule based model with custom scoring logic and a small machine learning baseline trained on the same labeled dataset.

## What I Implemented

- Expanded `SAMPLE_POSTS` and `TRUE_LABELS` with realistic examples that include slang, sarcasm, emoticons, and mixed feelings
- Upgraded `MoodAnalyzer.preprocess()` to normalize text and preserve simple emoticons
- Added rule based scoring with:
  - positive and negative vocabulary lookups
  - negation handling like `not happy`
  - contrast handling after words like `but`
  - simple emoticon and slang support
  - a `mixed` label when both positive and negative signals are present
- Added explanation output so each prediction shows the tokens, hits, and scoring notes
- Kept the ML comparison workflow in `ml_experiments.py`

## Repo Structure

```text
dataset.py
mood_analyzer.py
main.py
ml_experiments.py
model_card.md
requirements.txt
```

## How the Rule Based Model Works

1. `preprocess()` lowercases text, removes apostrophes, soft-normalizes repeated characters, and tokenizes words plus emoticons like `:)`.
2. `score_text()` checks tokens against positive and negative word sets.
3. Negation flips the next sentiment token.
4. Contrast words like `but` give extra weight to the phrase that follows.
5. `predict_label()` maps the final score to `positive`, `negative`, `neutral`, or `mixed`.

## Example Breakers

- `I absolutely love getting stuck in traffic`
- `This playlist is sick`
- `I am fine :) just exhausted`
- `I am not mad, just drained`

These help show where the rule based system improves and where it still struggles.

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the rule based analyzer:

```bash
python main.py
```

Run the machine learning comparison:

```bash
python ml_experiments.py
```

## Results Summary

- The rule based model is predictable and easy to explain.
- It handles clear vocabulary and some negation much better than the starter version.
- It still struggles with sarcasm and any phrase where tone depends on broader context.
- The ML model can learn useful word associations from the labeled examples, but it is very sensitive to the small dataset.

## Files to Review

- `dataset.py` for the labeled examples and vocabulary
- `mood_analyzer.py` for the scoring logic
- `model_card.md` for evaluation notes, limitations, and ethical considerations



<img src="https://github.com/user-attachments/assets/016a08a3-90df-48ce-b345-2c9f9c1ee2c1" alt="screenshot 1" width="600" />