# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial design used four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`. `Owner` manages the top-level account state and available time. `Pet` stores pet-specific information and its assigned tasks. `Task` represents one care action with timing, duration, priority, recurrence, and completion state. `Scheduler` acts as the logic layer that retrieves tasks from the owner's pets and turns them into a usable daily plan.

**b. Design changes**

Yes. During implementation I added `due_date` directly to the `Task` model instead of only storing `due_time`. That change made recurring tasks and daily schedule generation much cleaner because the scheduler could compare exact dates instead of guessing whether something belonged to today.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers:

- task priority
- due time
- due date
- whether the task is already completed
- the owner's available minutes for the day

I treated priority and available time as the most important constraints because the app's main job is to help the owner decide what most needs attention when time is limited.

**b. Tradeoffs**

One tradeoff is that conflict detection only checks for exact matching start times instead of overlapping durations. That is simpler and easier to explain, but it means the system can miss partial overlaps like a 30-minute task at `09:00` and a 20-minute task at `09:10`. For this project, the simpler rule felt reasonable because it keeps the scheduler readable and testable.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI-style workflow patterns for structure, refactoring direction, and documentation-style thinking. The most helpful prompt style was asking for bounded design help, such as how a scheduler should retrieve tasks from an owner's pets, or how to keep the implementation modular while still being simple enough for a class project.

**b. Judgment and verification**

One point where I would not accept an AI suggestion blindly was recurrence and schedule selection. A more abstract design can look elegant, but I kept the implementation direct and readable by putting recurrence on the `Task` model and keeping scheduling decisions inside `Scheduler.generate_daily_schedule()`. I verified the behavior by running the CLI demo and writing pytest coverage for recurrence and conflicts.

---

## 4. Testing and Verification

**a. What you tested**

I tested:

- marking a task complete
- adding a task to a pet
- sorting tasks chronologically
- generating the next recurring task for a daily task
- conflict detection for duplicate times

These tests mattered because they cover the most important user-facing behaviors in the system.

**b. Confidence**

I am reasonably confident that the scheduler works correctly for the implemented feature set. If I had more time, I would add tests for empty schedules, weekly recurrence, skipped low-priority tasks when time runs out, and overlapping durations that do not start at the exact same minute.

---

## 5. Reflection

**a. What went well**

The clean split between `pawpal_system.py`, `main.py`, and `app.py` went well. That CLI-first structure made it much easier to verify the backend before wiring it into Streamlit.

**b. What you would improve**

On another iteration I would improve the conflict detection logic to account for duration overlap, add persistence to JSON so the app remembers pets between runs, and support editing or deleting tasks from the UI.

**c. Key takeaway**

One important takeaway is that being the lead architect means making the final judgment calls. AI can help brainstorm and accelerate implementation, but the human still has to keep the system coherent, test the logic, and decide which tradeoffs are acceptable.
