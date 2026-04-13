# Tinker: BugHound

## Activity Overview

**Estimated time:** ~45 minutes

You are working on BugHound, an experimental AI powered debugging assistant. BugHound is not just a tool that points out problems. It is designed to behave like a cautious teammate that:

- examines code
- proposes changes
- evaluates the risk of those changes
- decides whether to act automatically or defer to a human

BugHound follows an agentic workflow rather than a single AI call. Some parts of this workflow rely on simple rules. Other parts rely on a large language model. Crucially, BugHound also includes reliability checks that can override or reject AI generated output when it seems unsafe.

Your task in this activity is not to make BugHound perfect. It is to understand how agentic systems are structured, where they fail, and how testing and guardrails shape their behavior.

## Goals

By the end of this activity, you will be able to:

- Describe an agentic workflow that includes analysis, action, evaluation, and reflection.
- Integrate an AI model into a larger system rather than treating it as a standalone solution.
- Reason about reliability, risk, and failure modes in AI assisted coding tools.
- Use testing and guardrails to limit unsafe or low confidence AI behavior.
- Reflect on when autonomous systems should defer to human judgment.

## Tinker Instructions

### Part 1: Exploring the Agentic Workflow

- Set up the BugHound starter repo locally.
- Create a virtual environment and install dependencies from `requirements.txt`.
- Open `bughound_app.py`, `bughound_agent.py`, and `reliability/risk_assessor.py`.
- Run the app in Streamlit.
- In the sidebar, use **Heuristic only (no API)** mode first.
- Paste in code from `sample_code/` and observe the output.
- Read the agent trace from top to bottom.

Questions to think through:

- Where does BugHound decide what problems exist in the code?
- Where does it decide how to change the code?
- Where does it decide whether the change is safe?
- What happens when the result feels incomplete or questionable?

### Part 2: Integrating an AI Analyzer

- Review the analyzer prompt files in `prompts/`.
- Create a `.env` file from `.env.example` and add your Gemini API key.
- Inspect the `analyze` method in `bughound_agent.py`.
- Run BugHound in Gemini mode on at least two files from `sample_code/`.
- Compare Gemini mode with heuristic mode.
- Make one reliability improvement to how AI analysis output is handled.

Focus on:

- How strict the agent should be when accepting model output
- When it should fall back to heuristics
- Whether the model output is easy for the agent to parse and trust

### Part 3: Proposing Fixes and Evaluating Risk

- Inspect the `propose_fix` method in `bughound_agent.py`.
- Read the fixer prompts in `prompts/`.
- Run BugHound in Gemini mode on a file with multiple issues.
- Review the diff and proposed fix carefully.
- Open `reliability/risk_assessor.py`.
- Make one deliberate change to the risk logic that affects whether BugHound auto-fixes or defers to a human.

### Part 4: Testing, Reliability, and Guardrails

- Skim the tests in `tests/`.
- Notice how `test_agent_workflow.py` uses a `MockClient` to test fallback behavior without real API calls.
- Run the tests.
- Try three kinds of input:
  - a mostly clean file
  - a clearly broken file
  - a weird edge case
- Identify one failure mode and add a guardrail for it.
- Add or update a test so that failure mode is checked offline.

### Part 5: Reflection and Model Card

Complete `model_card.md` and cover:

- system overview
- workflow
- tested inputs and outputs
- reliability and safety rules
- observed failure modes
- heuristic vs Gemini comparison
- human-in-the-loop triggers
- one concrete improvement idea

## Checkpoints

- You can run BugHound locally and explain the agentic loop.
- You integrated Gemini as a tool inside the workflow, not as a full replacement.
- You changed the risk or reliability logic in a deliberate way.
- You added or updated at least one guardrail-backed test.
- You completed the model card with reflections on reliability and human review.
