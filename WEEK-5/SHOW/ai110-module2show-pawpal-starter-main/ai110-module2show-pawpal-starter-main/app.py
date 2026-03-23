from __future__ import annotations

from datetime import date, datetime

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def get_owner() -> Owner:
    """Return the persistent owner object for this session."""
    if "owner" not in st.session_state:
        st.session_state.owner = Owner(
            name="Jordan",
            daily_minutes_available=120,
            preferences=["consistent routines"],
        )
    return st.session_state.owner


def task_rows(owner: Owner) -> list[dict]:
    """Return task rows formatted for the UI."""
    scheduler = Scheduler(owner)
    rows = []
    for item in scheduler.sort_by_time():
        pet = item["pet"]
        task = item["task"]
        rows.append(task.to_dict(pet.name))
    return rows


owner = get_owner()
scheduler = Scheduler(owner)

st.title("🐾 PawPal+")
st.caption("A smart pet care planner with sorting, conflict warnings, and recurring task support.")

with st.sidebar:
    st.subheader("Owner Profile")
    owner.name = st.text_input("Owner name", value=owner.name)
    owner.daily_minutes_available = st.slider(
        "Minutes available today",
        min_value=30,
        max_value=300,
        value=owner.daily_minutes_available,
        step=15,
    )
    st.write(f"Pets in system: {len(owner.pets)}")

st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=40, value=1)
    submitted_pet = st.form_submit_button("Add pet")
    if submitted_pet:
        if not pet_name.strip():
            st.warning("Please enter a pet name.")
        elif owner.get_pet(pet_name):
            st.warning("That pet already exists.")
        else:
            owner.add_pet(Pet(name=pet_name.strip(), species=species, age=int(age)))
            st.success(f"Added {pet_name.strip()} to PawPal+.")

if owner.pets:
    st.subheader("Add a Task")
    with st.form("add_task_form", clear_on_submit=True):
        pet_choice = st.selectbox("Pet", [pet.name for pet in owner.pets])
        task_title = st.text_input("Task title", value="Walk")
        due_date = st.date_input("Due date", value=date.today())
        due_time = st.time_input("Due time", value=datetime.strptime("08:00", "%H:%M").time())
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["high", "medium", "low"])
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        notes = st.text_input("Notes", value="")
        submitted_task = st.form_submit_button("Add task")
        if submitted_task:
            pet = owner.get_pet(pet_choice)
            if pet is None:
                st.error("Could not find that pet.")
            else:
                pet.add_task(
                    Task(
                        title=task_title.strip(),
                        due_time=due_time.strftime("%H:%M"),
                        duration_minutes=int(duration),
                        priority=priority,
                        frequency=frequency,
                        due_date=due_date,
                        notes=notes.strip(),
                    )
                )
                st.success(f"Added '{task_title.strip()}' for {pet_choice}.")
else:
    st.info("Add a pet first so you can start scheduling tasks.")

st.divider()
st.subheader("Current Tasks")
rows = task_rows(owner)
if rows:
    st.table(rows)
else:
    st.info("No tasks yet.")

st.divider()
st.subheader("Today's Smart Schedule")
schedule = scheduler.generate_daily_schedule(date.today())

if schedule["items"]:
    st.success(
        f"Planned {schedule['planned_minutes']} of {schedule['available_minutes']} available minutes."
    )
    st.table(schedule["items"])
else:
    st.info("No tasks scheduled for today yet.")

if schedule["conflicts"]:
    for warning in schedule["conflicts"]:
        st.warning(warning)

if schedule["skipped"]:
    for skipped in schedule["skipped"]:
        st.caption(skipped)

st.divider()
st.subheader("Complete a Task")
incomplete_rows = [row for row in rows if not row["completed"]]
if incomplete_rows:
    labels = [f"{row['pet']} | {row['time']} | {row['title']}" for row in incomplete_rows]
    selected_label = st.selectbox("Choose task to mark complete", labels)
    if st.button("Mark complete"):
        chosen = incomplete_rows[labels.index(selected_label)]
        scheduler.mark_task_complete(chosen["pet"], chosen["title"], chosen["time"])
        st.success("Task marked complete. Recurring tasks were rescheduled if needed.")
        st.rerun()
else:
    st.info("No incomplete tasks available.")
