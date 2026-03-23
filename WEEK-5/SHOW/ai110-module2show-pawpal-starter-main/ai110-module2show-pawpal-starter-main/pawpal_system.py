"""
Core logic layer for the PawPal+ scheduling system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """
    Represents a single care activity for a pet.
    """

    title: str
    due_time: str
    duration_minutes: int
    priority: str
    frequency: str = "once"
    due_date: date = field(default_factory=date.today)
    completed: bool = False
    notes: str = ""

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.completed = True

    def sort_key(self) -> tuple:
        """Return a tuple used for schedule sorting."""
        parsed_time = datetime.strptime(self.due_time, "%H:%M").time()
        return (self.due_date, parsed_time, PRIORITY_ORDER.get(self.priority, 3), self.title)

    def next_occurrence(self) -> Optional["Task"]:
        """Create the next recurring task, if this task repeats."""
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(days=7)
        else:
            return None

        return Task(
            title=self.title,
            due_time=self.due_time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            due_date=next_date,
            notes=self.notes,
        )

    def to_dict(self, pet_name: str) -> Dict[str, object]:
        """Return a serializable representation for the UI."""
        return {
            "pet": pet_name,
            "title": self.title,
            "date": self.due_date.isoformat(),
            "time": self.due_time,
            "duration": self.duration_minutes,
            "priority": self.priority,
            "frequency": self.frequency,
            "completed": self.completed,
            "notes": self.notes,
        }


@dataclass
class Pet:
    """
    Stores pet details and the tasks assigned to that pet.
    """

    name: str
    species: str
    age: int = 0
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def active_tasks(self) -> List[Task]:
        """Return incomplete tasks."""
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """
    Represents the pet owner and their planning preferences.
    """

    name: str
    daily_minutes_available: int = 120
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet for this owner."""
        self.pets.append(pet)

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Find a pet by name."""
        pet_name = pet_name.strip().lower()
        for pet in self.pets:
            if pet.name.lower() == pet_name:
                return pet
        return None

    def all_tasks(self) -> List[Dict[str, object]]:
        """Return all tasks paired with their pet."""
        all_items: List[Dict[str, object]] = []
        for pet in self.pets:
            for task in pet.tasks:
                all_items.append({"pet": pet, "task": task})
        return all_items


class Scheduler:
    """
    Retrieves, organizes, and validates pet care tasks.
    """

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_all_tasks(self) -> List[Dict[str, object]]:
        """Return all owner tasks, grouped by pet in a flat list."""
        return self.owner.all_tasks()

    def sort_by_time(self, tasks: Optional[List[Dict[str, object]]] = None) -> List[Dict[str, object]]:
        """Sort tasks by date, time, and priority."""
        items = tasks if tasks is not None else self.get_all_tasks()
        return sorted(items, key=lambda item: item["task"].sort_key())

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[Dict[str, object]]:
        """Filter tasks by pet name and completion status."""
        items = self.get_all_tasks()
        filtered: List[Dict[str, object]] = []
        for item in items:
            pet = item["pet"]
            task = item["task"]
            if pet_name and pet.name.lower() != pet_name.lower():
                continue
            if completed is not None and task.completed != completed:
                continue
            filtered.append(item)
        return self.sort_by_time(filtered)

    def detect_conflicts(self, target_date: Optional[date] = None) -> List[str]:
        """Flag tasks that share the same due time on a given date."""
        items = self.sort_by_time()
        conflicts: List[str] = []
        seen: Dict[tuple, str] = {}

        for item in items:
            pet = item["pet"]
            task = item["task"]
            if task.completed:
                continue
            if target_date and task.due_date != target_date:
                continue

            key = (task.due_date, task.due_time)
            label = f"{pet.name}: {task.title}"
            if key in seen:
                conflicts.append(
                    f"Conflict at {task.due_date.isoformat()} {task.due_time}: "
                    f"{seen[key]} overlaps with {label}"
                )
            else:
                seen[key] = label
        return conflicts

    def mark_task_complete(self, pet_name: str, task_title: str, due_time: str) -> Optional[Task]:
        """Complete a task and create the next recurring task when needed."""
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            return None

        for task in pet.tasks:
            if task.title == task_title and task.due_time == due_time and not task.completed:
                task.mark_complete()
                recurring = task.next_occurrence()
                if recurring is not None:
                    pet.add_task(recurring)
                return task
        return None

    def generate_daily_schedule(self, target_date: Optional[date] = None) -> Dict[str, object]:
        """Build a simple schedule that respects available minutes and priority."""
        target_date = target_date or date.today()
        daily_items = [
            item
            for item in self.get_all_tasks()
            if item["task"].due_date == target_date and not item["task"].completed
        ]
        sorted_items = sorted(
            daily_items,
            key=lambda item: (
                PRIORITY_ORDER.get(item["task"].priority, 3),
                datetime.strptime(item["task"].due_time, "%H:%M").time(),
            ),
        )

        chosen: List[Dict[str, object]] = []
        skipped: List[str] = []
        total_minutes = 0

        for item in sorted_items:
            pet = item["pet"]
            task = item["task"]
            if total_minutes + task.duration_minutes <= self.owner.daily_minutes_available:
                chosen.append(
                    {
                        "pet": pet.name,
                        "task": task.title,
                        "time": task.due_time,
                        "duration": task.duration_minutes,
                        "priority": task.priority,
                        "reason": (
                            f"Included because it is {task.priority} priority and fits within "
                            f"the remaining {self.owner.daily_minutes_available - total_minutes} minutes."
                        ),
                    }
                )
                total_minutes += task.duration_minutes
            else:
                skipped.append(
                    f"Skipped {pet.name}'s '{task.title}' because only "
                    f"{self.owner.daily_minutes_available - total_minutes} minutes were left."
                )

        return {
            "date": target_date.isoformat(),
            "planned_minutes": total_minutes,
            "available_minutes": self.owner.daily_minutes_available,
            "items": chosen,
            "skipped": skipped,
            "conflicts": self.detect_conflicts(target_date),
        }
