from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def make_scheduler() -> tuple[Scheduler, Pet]:
    """Build a simple scheduler fixture for tests."""
    owner = Owner(name="Alex", time_available_minutes=90)
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    return Scheduler(owner), pet


def test_mark_complete_updates_status() -> None:
    """Completed tasks should record their finished state."""
    task = Task(title="Breakfast", time="08:00", duration_minutes=10)

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
    """Pets should track newly added tasks."""
    _, pet = make_scheduler()

    pet.add_task(Task(title="Walk", time="07:00", duration_minutes=20))

    assert len(pet.tasks) == 1


def test_sorting_returns_tasks_in_time_order() -> None:
    """Scheduler should sort tasks chronologically."""
    scheduler, pet = make_scheduler()
    today = date.today()
    pet.add_task(Task(title="Evening walk", time="18:00", duration_minutes=20, due_date=today))
    pet.add_task(Task(title="Breakfast", time="07:30", duration_minutes=10, due_date=today))
    pet.add_task(Task(title="Medication", time="12:00", duration_minutes=5, due_date=today))

    ordered = scheduler.get_tasks_for_day(today)

    assert [task.title for _, task in ordered] == ["Breakfast", "Medication", "Evening walk"]


def test_daily_recurrence_creates_next_task() -> None:
    """Completing a daily task should create tomorrow's copy."""
    scheduler, pet = make_scheduler()
    today = date.today()
    pet.add_task(
        Task(
            title="Breakfast",
            time="08:00",
            duration_minutes=10,
            priority="high",
            frequency="daily",
            due_date=today,
        )
    )

    next_task = scheduler.mark_task_complete("Mochi", "Breakfast", "08:00", today)

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True


def test_conflict_detection_flags_duplicate_times() -> None:
    """Two tasks at the same time should raise a warning."""
    scheduler, pet = make_scheduler()
    today = date.today()
    pet.add_task(Task(title="Breakfast", time="08:00", duration_minutes=10, due_date=today))
    pet.add_task(Task(title="Medication", time="08:00", duration_minutes=5, due_date=today))

    warnings = scheduler.detect_conflicts(today)

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
