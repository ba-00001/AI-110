from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def build_scheduler() -> Scheduler:
    owner = Owner(name="Tester", daily_minutes_available=120)
    pet = Pet(name="Mochi", species="dog")
    other = Pet(name="Luna", species="cat")
    today = date.today()

    pet.add_task(Task("Walk", "09:00", 20, "high", "daily", today))
    pet.add_task(Task("Breakfast", "08:00", 10, "medium", "once", today))
    other.add_task(Task("Medication", "09:00", 5, "high", "once", today))

    owner.add_pet(pet)
    owner.add_pet(other)
    return Scheduler(owner)


def test_mark_complete_changes_status() -> None:
    task = Task("Walk", "09:00", 20, "high")
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_count() -> None:
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task("Walk", "09:00", 20, "high"))
    assert len(pet.tasks) == 1


def test_sorting_returns_chronological_order() -> None:
    scheduler = build_scheduler()
    sorted_items = scheduler.sort_by_time()
    time_pairs = [(item["task"].due_date, item["task"].due_time) for item in sorted_items]
    assert time_pairs == sorted(time_pairs)
    assert sorted_items[0]["task"].title == "Breakfast"


def test_daily_recurrence_creates_next_task() -> None:
    scheduler = build_scheduler()
    scheduler.mark_task_complete("Mochi", "Walk", "09:00")
    pet = scheduler.owner.get_pet("Mochi")
    assert pet is not None

    recurring_tasks = [task for task in pet.tasks if task.title == "Walk" and not task.completed]
    assert len(recurring_tasks) == 1
    assert recurring_tasks[0].due_date == date.today() + timedelta(days=1)


def test_conflict_detection_flags_duplicate_time() -> None:
    scheduler = build_scheduler()
    conflicts = scheduler.detect_conflicts(date.today())
    assert any("09:00" in conflict for conflict in conflicts)
