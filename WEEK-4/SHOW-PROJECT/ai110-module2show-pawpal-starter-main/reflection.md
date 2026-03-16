# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design focused on four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`. I wanted the structure to match the real-world problem closely. The `Owner` class was responsible for storing household information and managing multiple pets. The `Pet` class held each pet's details and its list of care tasks. The `Task` class represented one scheduled activity with attributes like title, time, duration, priority, frequency, and completion status. The `Scheduler` class acted as the decision-making layer that could collect tasks from every pet, organize them, and build a daily plan.

Three core user actions I identified early were:

- Add a pet to the household
- Schedule a care task for a pet
- View today's organized schedule

**b. Design changes**

My design changed during implementation in two important ways. First, I added `due_date` to the `Task` class because recurring tasks needed a real date to generate the next instance correctly. Second, I gave `Scheduler` a `mark_task_complete()` method instead of leaving recurrence logic only inside the UI. That kept the business logic inside the backend where it was easier to test and reuse.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers time, priority, recurrence, completion status, and the owner's total available minutes for the day. I decided that priority should matter most because missing a medication task is more serious than delaying a low-priority enrichment activity. After priority, I used time so the final schedule still reads like a realistic timeline.

**b. Tradeoffs**

One tradeoff is that my conflict detection only checks for exact matching times instead of overlapping durations. That means a task at 8:00 for 30 minutes and another at 8:15 will not be flagged. I think that is reasonable for this scenario because it keeps the algorithm lightweight, easy to explain, and easy to test while still catching the most obvious scheduling mistakes.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI as a design and review partner rather than letting it make every decision for me. It was most helpful for brainstorming the UML structure, suggesting how the `Scheduler` should access task data through the `Owner`, and helping compare ways to implement sorting and recurrence logic. The most effective prompts were specific ones like "How should the scheduler retrieve tasks from the owner's pets?" or "What is a simple way to detect duplicate task times?"

Using separate chats for different phases would help keep the work organized because design questions, testing questions, and UI questions are different kinds of problems. That separation makes it easier to focus on one layer of the system at a time.

**b. Judgment and verification**

One moment where I would not accept an AI suggestion as-is was around making the scheduling logic more complex with too many rules at once. A more advanced solution might have looked impressive, but it would have been harder to read and harder to verify. I kept a simpler version that prioritizes tasks, sorts them cleanly, and respects the owner's time budget. I verified the final logic by running the CLI demo and then writing pytest tests for the most important behaviors.

---

## 4. Testing and Verification

**a. What you tested**

I tested five core behaviors:

- Marking a task complete updates its status
- Adding a task to a pet increases the task count
- Tasks are sorted in chronological order
- Completing a daily task creates the next day's task
- Conflict detection returns a warning when two tasks share the same time

These tests were important because they covered both the basic object interactions and the smarter scheduling features that made the project more than just a data tracker.

**b. Confidence**

My confidence level is 4 out of 5. I feel good about the required behaviors because the backend logic is separated cleanly from the UI and covered by tests. If I had more time, I would test overlapping durations, invalid time formats submitted through the UI, weekly recurrence edge cases, and saving/loading data between sessions.

---

## 5. Reflection

**a. What went well**

The part I am most satisfied with is the separation between the logic layer and the interface. Building the backend first made it much easier to test the scheduler and then connect it to Streamlit without rewriting core behavior.

**b. What you would improve**

If I had another iteration, I would add persistent storage so pets and tasks survive after the app closes. I would also improve the scheduling algorithm to detect overlapping time windows and maybe support smarter prioritization rules beyond just high, medium, and low.

**c. Key takeaway**

One important thing I learned is that being the lead architect means deciding when to keep a system simple. AI can generate lots of ideas quickly, but it is still my job to choose the version that best fits the problem, stays readable, and can be verified with real tests.
