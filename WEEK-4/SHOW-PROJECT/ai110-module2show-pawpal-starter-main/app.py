from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def get_owner() -> Owner:
    """Create the shared owner object once per Streamlit session."""
    if "owner" not in st.session_state:
        st.session_state.owner = Owner(
            name="Jordan",
            time_available_minutes=120,
            preferences=["Morning walks", "Short evening cleanup"],
        )
    return st.session_state.owner


owner = get_owner()
scheduler = Scheduler(owner)
today = date.today()

st.title("🐾 PawPal+")
st.caption("A smart pet care planner for keeping feedings, walks, meds, and appointments organized.")

with st.expander("Project Summary", expanded=True):
    st.markdown(
        """
PawPal+ uses a modular Python backend to manage pets, tasks, and a daily plan.
The scheduler can sort by time, filter by pet or status, detect exact-time conflicts,
and automatically create the next task when a recurring item is completed.
"""
    )

st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value=owner.name)
time_budget = st.number_input(
    "Available minutes for today's care",
    min_value=30,
    max_value=720,
    value=owner.time_available_minutes,
    step=15,
)
owner.name = owner_name
owner.time_available_minutes = int(time_budget)

st.divider()

st.subheader("Add a Pet")
with st.form("pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=30, value=1)
    pet_notes = st.text_input("Notes")
    add_pet = st.form_submit_button("Save pet")

if add_pet:
    if not pet_name.strip():
        st.error("Enter a pet name before saving.")
    elif owner.get_pet(pet_name.strip()):
        st.warning("That pet already exists in this session.")
    else:
        owner.add_pet(Pet(name=pet_name.strip(), species=species, age=int(age), notes=pet_notes.strip()))
        st.success(f"Added {pet_name.strip()} to PawPal+.")

pet_names = [pet.name for pet in owner.pets]

if owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {
                "Name": pet.name,
                "Species": pet.species.title(),
                "Age": pet.age,
                "Notes": pet.notes or "-",
                "Tasks": len(pet.tasks),
            }
            for pet in owner.pets
        ]
    )
else:
    st.info("Add a pet to get started.")

st.divider()

st.subheader("Schedule a Task")
if not pet_names:
    st.info("Create at least one pet before adding tasks.")
else:
    with st.form("task_form", clear_on_submit=True):
        task_pet = st.selectbox("Pet", pet_names)
        task_title = st.text_input("Task title", placeholder="Morning walk")
        task_time = st.text_input("Time (HH:MM)", value="07:30")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["high", "medium", "low"])
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        task_notes = st.text_input("Task notes")
        add_task = st.form_submit_button("Add task")

    if add_task:
        pet = owner.get_pet(task_pet)
        if not task_title.strip():
            st.error("Enter a task title before saving.")
        elif pet is None:
            st.error("Select a valid pet.")
        else:
            try:
                pet.add_task(
                    Task(
                        title=task_title.strip(),
                        time=task_time.strip(),
                        duration_minutes=int(duration),
                        priority=priority,
                        frequency=frequency,
                        due_date=today,
                        notes=task_notes.strip(),
                    )
                )
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.success(f"Added {task_title.strip()} for {task_pet}.")

st.divider()

st.subheader("Today's Tasks")
filter_pet = st.selectbox("Filter by pet", ["All pets"] + pet_names)
status_filter = st.selectbox("Filter by status", ["Pending", "Completed", "All"])

completed_filter = {"Pending": False, "Completed": True, "All": None}[status_filter]
selected_pet = None if filter_pet == "All pets" else filter_pet
filtered_tasks = scheduler.filter_tasks(
    pet_name=selected_pet,
    completed=completed_filter,
    target_date=today,
)

if filtered_tasks:
    st.table(
        [
            {
                "Pet": pet.name,
                "Task": task.title,
                "Time": task.time,
                "Priority": task.priority.title(),
                "Frequency": task.frequency.title(),
                "Status": "Done" if task.completed else "Pending",
            }
            for pet, task in filtered_tasks
        ]
    )
else:
    st.info("No tasks match the current filters.")

if filtered_tasks:
    pending_labels = [
        f"{pet.name} | {task.time} | {task.title}"
        for pet, task in filtered_tasks
        if not task.completed
    ]
    if pending_labels:
        selected_label = st.selectbox("Mark a task complete", pending_labels)
        if st.button("Complete selected task"):
            pet_name_value, due_time, task_title_value = [part.strip() for part in selected_label.split("|", 2)]
            next_task = scheduler.mark_task_complete(
                pet_name=pet_name_value,
                task_title=task_title_value,
                due_time=due_time,
                target_date=today,
            )
            st.success("Task marked complete.")
            if next_task:
                st.info(
                    f"Recurring task created for {next_task.due_date.isoformat()} at {next_task.time}."
                )
            st.rerun()

st.divider()

st.subheader("Smart Schedule")
plan = scheduler.build_daily_plan(today)
conflicts = scheduler.detect_conflicts(today)

if conflicts:
    for warning in conflicts:
        st.warning(warning)
else:
    st.success("No scheduling conflicts detected for today.")

if plan:
    st.table(plan)
else:
    st.info("Add tasks to generate a daily plan.")

st.markdown("### Why this plan works")
if plan:
    for item in plan:
        st.write(
            f"- {item['time']} | {item['pet']} | {item['task']} ({item['priority']}) - {item['reason']}"
        )
else:
    st.caption("The scheduler explanations will appear here after tasks are added.")
