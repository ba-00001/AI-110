# Reflection: Game Glitch Investigator

## 1. What was broken when you started?

When I first inspected the app, it looked like a simple Streamlit guessing game, but the behavior did not match the labels on the screen. One obvious bug was that the hints were backwards: a guess that was too high returned "Go HIGHER!" and a guess that was too low returned "Go LOWER!" The game also switched the secret number between an integer and a string on alternating turns, which could make valid guesses compare incorrectly. I also found an attempt counter bug where the app started at 1 attempt before the player guessed anything, so the "attempts left" display was wrong from the beginning.

## 2. How did you use AI as a teammate?

I used an AI coding assistant as a second set of eyes to inspect the logic and help organize the refactor. One correct suggestion was to move the reusable game rules out of `app.py` and into `logic_utils.py` so the functions could be tested without running Streamlit. I verified that suggestion by updating the imports in `app.py`, running pytest, and confirming that the logic functions worked directly in the test file. One misleading AI-style pattern in the starter code was the fallback that compared guesses as strings after a `TypeError`; that made the code look "defensive" but actually introduced incorrect comparisons, so I removed it and verified the fix by restoring direct integer comparisons only.

## 3. Debugging and testing your fixes

I decided a bug was fixed only when the code path was simpler and there was a direct way to verify the behavior. I added pytest cases for winning guesses, too-high and too-low guesses, decimal input rejection, hard-mode range selection, and score updates. Those tests showed that the hints now match the actual comparison result and that invalid decimal guesses are rejected instead of being silently rounded. AI helped most with suggesting the shape of the tests, but I still had to review each assertion so it matched the actual function return values.

## 4. What did you learn about Streamlit and state?

This project reinforced that Streamlit reruns the script from top to bottom whenever the user interacts with a widget, so values must be stored in `st.session_state` if they need to survive between reruns. A stable game needs the secret number, attempts, score, and status to live in session state instead of being recreated unpredictably during each interaction. I explained it to myself as "the script refreshes every click, but session state is the notebook where the app remembers what already happened." The key change was to centralize round resets so the app now creates and resets the secret number in one place based on the selected difficulty.

## 5. Looking ahead: your developer habits

One habit I want to reuse is separating pure logic from UI code as early as possible, because it makes debugging faster and testing more reliable. Next time I work with AI on a coding task, I want to ask for smaller, more targeted changes instead of trusting broad "fix everything" patterns that can hide new bugs. This project changed the way I think about AI-generated code because it showed that code can sound confident and still be logically wrong, so verification matters more than the explanation.
