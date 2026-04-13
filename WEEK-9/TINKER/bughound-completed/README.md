# BugHound Completed Activity

This is my completed Week 9 Tinker project based on the BugHound starter. I kept the original agentic workflow, then made targeted reliability improvements so the agent is more cautious when Gemini output is weak or when a proposed fix changes too much code.

## What I Changed

- Added stricter validation for AI analyzer output in `bughound_agent.py`
- Added a larger-edit risk signal in `reliability/risk_assessor.py`
- Prevented low-severity issues from auto-fixing when the rewrite footprint is too large
- Added tests for incomplete model output and overly large rewrites
- Completed the reflection in `model_card.md`

## How to Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run bughound_app.py
```

## How to Test

```bash
pytest
```

## Notes

- Use **Heuristic only (no API)** mode first to preserve Gemini free-tier quota.
- If you use Gemini mode, add your key to `.env` using `.env.example` as a template.
- The app is designed to show the full agent trace so you can inspect how BugHound analyzed, fixed, tested, and reflected on each run.
