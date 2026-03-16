from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def print_table(title: str, rows: list[dict[str, object]]) -> None:
    """Print a compact text table without extra dependencies."""
    print(f"\n{title}")
    print("-" * len(title))

    if not rows:
        print("No items to display.")
        return

    headers = list(rows[0].keys())
    widths = {
        header: max(len(str(header)), max(len(str(row[header])) for row in rows))
        for header in headers
    }

    header_row = " | ".join(str(header).ljust(widths[header]) for header in headers)
    print(header_row)
    print("-+-".join("-" * widths[header] for header in headers))

    for row in rows:
        print(" | ".join(str(row[header]).ljust(widths[header]) for header in headers))


def build_demo_system() -> Scheduler:
    """Create sample pets and tasks for a CLI walkthrough."""
    owner = Owner(name="Jordan", time_available_minutes=120, preferences=["Morning walks"])

    mochi = Pet(name="Mochi", species="dog", age=4, notes="Enjoys long sniff walks.")
    luna = Pet(name="Luna", species="cat", age=2, notes="Needs evening medication.")

    today = date.today()
    mochi.add_task(
        Task(
            title="Morning walk",
            time="07:30",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            due_date=today,
        )
    )
    mochi.add_task(
        Task(
            title="Breakfast",
            time="07:00",
            duration_minutes=10,
            priority="high",
            frequency="daily",
            due_date=today,
        )
    )
    luna.add_task(
        Task(
            title="Medication",
            time="07:30",
            duration_minutes=5,
            priority="high",
            frequency="daily",
            due_date=today,
        )
    )
    luna.add_task(
        Task(
            title="Litter box refresh",
            time="18:00",
            duration_minutes=15,
            priority="medium",
            frequency="daily",
            due_date=today,
        )
    )

    owner.add_pet(mochi)
    owner.add_pet(luna)
    return Scheduler(owner)


if __name__ == "__main__":
    scheduler = build_demo_system()
    today = date.today()

    print_table("Today's Schedule", scheduler.schedule_as_rows(today))
    print_table("High Priority Plan", scheduler.build_daily_plan(today))

    conflicts = scheduler.detect_conflicts(today)
    print("\nConflict Check")
    print("--------------")
    if conflicts:
        for warning in conflicts:
            print(f"- {warning}")
    else:
        print("No conflicts detected.")
