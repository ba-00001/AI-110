# PawPal+

PawPal+ is a pet care management system that combines a Python logic layer, a CLI demo, automated tests, and a Streamlit interface. The app helps an owner manage pets, create care tasks, generate a daily plan, detect simple conflicts, and handle recurring tasks.

## Features

- Object-oriented system built with `Owner`, `Pet`, `Task`, and `Scheduler`
- Daily schedule generation based on task priority, due time, and available minutes
- Sorting by date and time
- Filtering by pet and completion status in the scheduler layer
- Conflict warnings when tasks share the same scheduled time
- Daily and weekly recurrence when a repeating task is marked complete
- Streamlit UI connected to the backend logic through `st.session_state`
- CLI demo script for backend verification
- Automated pytest suite for core scheduling behaviors

## Project Structure

```text
app.py
main.py
pawpal_system.py
reflection.md
tests/test_pawpal.py
uml_final.svg
requirements.txt
```

## System Design

### Core Classes

- `Task`: stores task title, due time, duration, priority, frequency, due date, and completion status
- `Pet`: stores pet details and a list of tasks
- `Owner`: stores owner details, available time, preferences, and pets
- `Scheduler`: retrieves tasks, sorts them, filters them, detects conflicts, marks tasks complete, and builds a daily schedule

### Final UML

The final class diagram is saved in `uml_final.svg`.

## Smarter Scheduling

The scheduler includes several algorithmic features:

- `sort_by_time()` returns tasks in chronological order
- `filter_tasks()` narrows tasks by pet or completion state
- `detect_conflicts()` returns warnings for duplicate times
- `generate_daily_schedule()` chooses tasks that fit the owner's available minutes while prioritizing higher-priority tasks first
- `mark_task_complete()` creates the next task automatically for daily and weekly recurring items

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the CLI demo:

```bash
python main.py
```

Run the Streamlit app:

```bash
streamlit run app.py
```

## Testing PawPal+

Run tests with:

```bash
python -m pytest
```

The tests cover:

- task completion status
- adding tasks to a pet
- chronological sorting
- daily recurrence creation
- duplicate-time conflict detection

**Confidence Level:** `4/5 stars`

I am confident in the core scheduling behaviors covered by the tests and CLI demo. The main remaining gaps are richer overlap detection and more advanced prioritization rules.

## Demo Notes

The Streamlit app lets you:

- add pets
- add scheduled tasks
- view current task data
- generate today's smart schedule
- mark tasks complete and automatically reschedule recurring tasks

## Reflection

See `reflection.md` for design decisions, tradeoffs, testing notes, and AI collaboration details.


<img src="https://github.com/user-attachments/assets/831f501f-23d9-4a92-bc81-79f336e1fcd4" alt="screenshot 1" width="600" />