from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional


PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}
RECURRENCE_DELTAS = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}


@dataclass
class Task:
    """Represents one care activity for a pet."""

    title: str
    time: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "once"
    due_date: date = field(default_factory=date.today)
    notes: str = ""
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate incoming task data."""
        normalized_priority = self.priority.lower()
        normalized_frequency = self.frequency.lower()

        if normalized_priority not in PRIORITY_RANK:
            raise ValueError("Priority must be low, medium, or high.")
        if normalized_frequency not in {"once", "daily", "weekly"}:
            raise ValueError("Frequency must be once, daily, or weekly.")

        datetime.strptime(self.time, "%H:%M")
        self.priority = normalized_priority
        self.frequency = normalized_frequency

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task complete and return the next recurring instance when needed."""
        self.completed = True

        if self.frequency not in RECURRENCE_DELTAS:
            return None

        return Task(
            title=self.title,
            time=self.time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            due_date=self.due_date + RECURRENCE_DELTAS[self.frequency],
            notes=self.notes,
        )

    def sort_key(self) -> tuple[date, int, str]:
        """Return a sortable key for chronological ordering."""
        return (self.due_date, self.minutes_since_midnight(), self.title.lower())

    def minutes_since_midnight(self) -> int:
        """Convert task time into minutes for stable comparisons."""
        scheduled = datetime.strptime(self.time, "%H:%M")
        return scheduled.hour * 60 + scheduled.minute


@dataclass
class Pet:
    """Stores pet details and its care tasks."""

    name: str
    species: str
    age: int = 0
    notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task_title: str, due_time: str) -> bool:
        """Remove the first task matching title and time."""
        for index, task in enumerate(self.tasks):
            if task.title == task_title and task.time == due_time:
                del self.tasks[index]
                return True
        return False

    def get_tasks(self, include_completed: bool = True) -> list[Task]:
        """Return this pet's tasks, optionally hiding completed ones."""
        if include_completed:
            return list(self.tasks)
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """Represents the pet owner and their preferences."""

    name: str
    time_available_minutes: int = 180
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's household."""
        self.pets.append(pet)

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Find a pet by name."""
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet
        return None

    def all_tasks(self, include_completed: bool = True) -> list[tuple[Pet, Task]]:
        """Return every task across the owner's pets."""
        task_pairs: list[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.get_tasks(include_completed=include_completed):
                task_pairs.append((pet, task))
        return task_pairs


class Scheduler:
    """Organizes, filters, and explains the owner's pet-care schedule."""

    def __init__(self, owner: Owner) -> None:
        """Store the owner whose tasks this scheduler manages."""
        self.owner = owner

    def get_tasks_for_day(
        self,
        target_date: Optional[date] = None,
        include_completed: bool = False,
    ) -> list[tuple[Pet, Task]]:
        """Collect tasks scheduled for a specific date."""
        active_date = target_date or date.today()
        tasks = [
            (pet, task)
            for pet, task in self.owner.all_tasks(include_completed=include_completed)
            if task.due_date == active_date
        ]
        return self.sort_by_time(tasks)

    def sort_by_time(self, task_pairs: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Sort tasks chronologically."""
        return sorted(task_pairs, key=lambda pair: pair[1].sort_key())

    def sort_by_priority(self, task_pairs: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Sort tasks by priority first, then time."""
        return sorted(
            task_pairs,
            key=lambda pair: (PRIORITY_RANK[pair[1].priority], pair[1].sort_key()),
        )

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
        target_date: Optional[date] = None,
    ) -> list[tuple[Pet, Task]]:
        """Filter tasks by pet, completion status, and date."""
        task_pairs = self.owner.all_tasks(include_completed=True)

        if pet_name:
            task_pairs = [
                (pet, task)
                for pet, task in task_pairs
                if pet.name.lower() == pet_name.lower()
            ]
        if completed is not None:
            task_pairs = [
                (pet, task) for pet, task in task_pairs if task.completed is completed
            ]
        if target_date is not None:
            task_pairs = [
                (pet, task) for pet, task in task_pairs if task.due_date == target_date
            ]

        return self.sort_by_time(task_pairs)

    def detect_conflicts(
        self,
        target_date: Optional[date] = None,
    ) -> list[str]:
        """Return warnings when two tasks share the same date and time."""
        active_date = target_date or date.today()
        task_pairs = self.get_tasks_for_day(active_date, include_completed=False)
        seen: dict[tuple[date, str], list[str]] = {}
        warnings: list[str] = []

        for pet, task in task_pairs:
            key = (task.due_date, task.time)
            seen.setdefault(key, []).append(f"{pet.name}: {task.title}")

        for (due_date, due_time), matches in seen.items():
            if len(matches) > 1:
                task_list = ", ".join(matches)
                warnings.append(
                    f"Conflict on {due_date.isoformat()} at {due_time}: {task_list}"
                )

        return warnings

    def mark_task_complete(
        self,
        pet_name: str,
        task_title: str,
        due_time: str,
        target_date: Optional[date] = None,
    ) -> Optional[Task]:
        """Complete a task and add the next recurring task when applicable."""
        active_date = target_date or date.today()
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            return None

        for task in pet.tasks:
            if (
                task.title == task_title
                and task.time == due_time
                and task.due_date == active_date
                and not task.completed
            ):
                next_task = task.mark_complete()
                if next_task is not None:
                    pet.add_task(next_task)
                return next_task

        return None

    def build_daily_plan(
        self,
        target_date: Optional[date] = None,
        available_minutes: Optional[int] = None,
    ) -> list[dict[str, str | int]]:
        """Choose a realistic plan for the day based on priority and time budget."""
        active_date = target_date or date.today()
        remaining_minutes = (
            available_minutes
            if available_minutes is not None
            else self.owner.time_available_minutes
        )
        plan: list[dict[str, str | int]] = []

        for pet, task in self.sort_by_priority(
            self.get_tasks_for_day(active_date, include_completed=False)
        ):
            if task.duration_minutes > remaining_minutes:
                continue

            explanation = (
                f"Scheduled because {task.priority} priority tasks should be handled early"
                f" and it fits within the remaining {remaining_minutes} minutes."
            )
            plan.append(
                {
                    "pet": pet.name,
                    "task": task.title,
                    "time": task.time,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority.title(),
                    "reason": explanation,
                }
            )
            remaining_minutes -= task.duration_minutes

        return sorted(plan, key=lambda item: item["time"])

    def schedule_as_rows(
        self,
        target_date: Optional[date] = None,
        include_completed: bool = False,
    ) -> list[dict[str, str | int]]:
        """Return tasks in a table-friendly structure for CLI or UI output."""
        rows: list[dict[str, str | int]] = []
        for pet, task in self.get_tasks_for_day(
            target_date=target_date,
            include_completed=include_completed,
        ):
            rows.append(
                {
                    "Pet": pet.name,
                    "Species": pet.species.title(),
                    "Task": task.title,
                    "Time": task.time,
                    "Duration": task.duration_minutes,
                    "Priority": task.priority.title(),
                    "Frequency": task.frequency.title(),
                    "Status": "Done" if task.completed else "Pending",
                }
            )
        return rows
