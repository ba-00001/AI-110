# BugHound Model Card

## 1) What is this system?

**Name:** BugHound  
**Purpose:** BugHound is an experimental AI-powered debugging assistant that reviews short Python snippets, proposes a fix, and evaluates whether that fix is safe enough to auto-apply.  
**Intended users:** Students learning agentic workflows, prompt integration, and AI reliability guardrails.

## 2) How does it work?

BugHound follows a small agentic loop: plan, analyze, act, test, and reflect.

- **Plan:** The agent logs that it is running a debugging workflow.
- **Analyze:** In offline mode it uses heuristics to look for `print(...)`, `TODO`, and bare `except:` patterns. In Gemini mode it asks the model for structured JSON issue objects, then validates that structure before trusting it.
- **Act:** If issues are found, BugHound proposes a fix using either heuristics or Gemini. The fixer is supposed to preserve behavior and keep changes small.
- **Test:** The reliability layer scores the proposed fix using issue severity and structural change checks.
- **Reflect:** The agent decides whether the fix should be auto-applied or sent to a human for review.

Heuristics are more predictable but narrower. Gemini can produce richer analysis, but only if its output is parseable and complete enough for the workflow to trust.

## 3) Inputs and outputs

**Inputs I tested**

- `sample_code/cleanish.py`
- `sample_code/mixed_issues.py`
- `sample_code/flaky_try_except.py`
- a short empty-style case with almost no meaningful code

Most inputs were short functions, try/except blocks, or tiny scripts with simple code smells.

**Outputs**

- Issue types included `Code Quality`, `Reliability`, and `Maintainability`
- Proposed fixes included replacing `print(...)` with `logging.info(...)` and replacing bare `except:` with `except Exception as e:`
- Risk reports included a numeric score, a risk level, reasons, and an `should_autofix` decision

## 4) Reliability and safety rules

### Rule 1: penalize missing fixes

- **What it checks:** If the fixer returns an empty string, the risk score drops to 0 and the change is marked high risk.
- **Why it matters:** An agent should not auto-apply a missing or broken result.
- **Possible false positive:** A model refusal could still contain useful analysis, but the system treats the fix as completely unusable.
- **Possible false negative:** A non-empty fix can still be dangerous even if it avoids this rule.

### Rule 2: penalize removed return behavior

- **What it checks:** If the original code has `return` and the proposed fix removes it entirely, the score drops.
- **Why it matters:** Return-value changes often alter behavior in subtle ways.
- **Possible false positive:** A refactor could preserve behavior while reorganizing return logic in a different way.
- **Possible false negative:** The fixer might keep `return` statements but still change what is returned.

### Rule 3: penalize large edit footprints

- **What it checks:** If the rewritten code changes a large portion of the file, the score is reduced and low-severity issues no longer auto-fix.
- **Why it matters:** Small style issues should not trigger sweeping rewrites.
- **Possible false positive:** A compact original file may hit the threshold quickly.
- **Possible false negative:** A risky semantic change can still happen in only a few lines.

## 5) Observed failure modes

### Failure mode 1: incomplete AI analysis output

One risk is that the model returns JSON that is technically valid but not useful, such as an issue with an empty message. Before my change, BugHound could accept that too easily. I added a guardrail so incomplete issue objects trigger a fallback to heuristics.

### Failure mode 2: over-editing for low-severity issues

Another failure mode is a large rewrite for something minor like a `print(...)` statement. That kind of change feels risky because it may alter behavior more than the detected issue justifies. I tightened the risk assessment so low-severity issues do not auto-fix when the edit footprint is too large.

## 6) Heuristic vs Gemini comparison

- **What Gemini can do better:** Gemini can notice more contextual issues and explain them in a richer way.
- **What heuristics do better:** Heuristics are predictable and reliable for the exact patterns they target.
- **How fixes differ:** Heuristic fixes are narrow and mechanical. Gemini fixes can be more natural but also more likely to over-edit or drift from the requested structure.
- **Did the risk scorer agree with my intuition?** Mostly yes after the guardrail change. The new large-edit rule makes the system more cautious in cases where I would want review.

## 7) Human-in-the-loop decision

BugHound should refuse to auto-fix when the detected issue is low severity but the proposed rewrite changes a large portion of the file. That is a sign the model may be optimizing style while accidentally changing behavior.

- **Trigger:** Low-severity issue plus large edit footprint
- **Where to implement it:** `reliability/risk_assessor.py`
- **User message:** "BugHound found a low-risk issue, but the proposed rewrite changes too much of the file. Human review is recommended before applying this fix."

## 8) Improvement idea

One low-complexity improvement would be to compare the number of function definitions before and after the fix. If the fixer adds or removes functions unexpectedly, the risk score should increase. That would catch another kind of over-editing without requiring a full AST-based analysis pipeline.
