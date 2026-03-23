"""
CLI demo for the PawPal+ backend.
"""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_owner() -> Owner:
    """Create a demo owner with two pets and several tasks."""
    owner = Owner(name="Jordan", daily_minutes_available=90, preferences=["morning walks"])

    mochi = Pet(name="Mochi", species="dog", age=4)
    luna = Pet(name="Luna", species="cat", age=7)

    today = date.today()

    mochi.add_task(Task("Morning walk", "07:30", 25, "high", "daily", today))
    mochi.add_task(Task("Medication", "08:00", 5, "high", "daily", today))
    luna.add_task(Task("Breakfast", "08:00", 10, "medium", "daily", today))
    luna.add_task(Task("Evening play", "18:30", 20, "medium", "daily", today))

    owner.add_pet(mochi)
    owner.add_pet(luna)
    return owner


def print_schedule(schedule: dict) -> None:
    """Print a readable schedule to the terminal."""
    print(f"=== PawPal+ Schedule for {schedule['date']} ===")
    print(
        f"Planned {schedule['planned_minutes']} of "
        f"{schedule['available_minutes']} available minutes\n"
    )

    if not schedule["items"]:
        print("No tasks scheduled.")
    else:
        for item in schedule["items"]:
            print(
                f"{item['time']} | {item['pet']} | {item['task']} | "
                f"{item['duration']} min | {item['priority']}"
            )
            print(f"  Reason: {item['reason']}")

    if schedule["conflicts"]:
        print("\nWarnings:")
        for warning in schedule["conflicts"]:
            print(f"- {warning}")

    if schedule["skipped"]:
        print("\nSkipped:")
        for skipped in schedule["skipped"]:
            print(f"- {skipped}")


if __name__ == "__main__":
    owner = build_demo_owner()
    scheduler = Scheduler(owner)
    print_schedule(scheduler.generate_daily_schedule())
