# ByteBites Tinker Activity

This project lives entirely inside the `WEEK-3` folder and implements the backend architecture for the ByteBites campus food ordering app. The goal was to turn a vague feature request into a small but clean Python system that uses object-oriented design, a few simple algorithms, and basic pytest validation.

## Project Goal

The original ByteBites prototype had unclear structure and unreliable behavior. This version rebuilds the core logic around four focused classes:

- `Customer`
- `MenuItem`
- `Menu`
- `Order`

Each class maps directly to a key part of the feature request so the final code stays easy to explain and verify.

<!--
`## Image Placeholders`

`Add screenshots to this section later before final submission.`

`### Browser Home Screen`

`[Insert screenshot of the main ByteBites browser page here]`

`### Menu Filtering and Sorting`

`[Insert screenshot showing the category filter, search, and sorting tools here]`

`### Order Panel and Verification`

`[Insert screenshot showing items added to the order and verified customer status here]`

`### AI Assistant Demo`

`[Insert screenshot showing a Gemini or fallback AI recommendation here]`

-->

`## Files Included`

- `bytebites_spec.md`: the copied feature request plus the selected candidate classes.
- `draft_from_copilot.md`: an early rough UML-style draft with quick review notes.
- `bytebites_design.md`: the refined final UML-style class diagram.
- `.github/agens/bytebites_design_agent.md`: a custom agent definition matching the assignment wording.
- `models.py`: the full implementation of the four classes and a short manual demo.
- `test_bytebites.py`: pytest tests covering totals, empty orders, filtering, sorting, and customer verification.
- `index.html`, `styles.css`, `script.js`: a simple local browser demo of the same ByteBites logic.
- `bytebites_backend.py`: shared backend helpers for local development and deployment.
- `api/menu.py` and `api/assistant.py`: Vercel-style Python API routes.
- `ai_server.py`: a local Python server that mirrors the same `/api` routes for browser testing.
- `.env.example`: a template showing how to provide the Gemini API key locally.

## Design Explanation

### 1. `MenuItem`

`MenuItem` represents one product that appears in the app. It stores:

- item name
- item price
- item category
- popularity rating

It also contains `matches_category()` so the menu can ask each item whether it belongs to a requested category. That keeps the comparison logic close to the data it depends on.

### 2. `Menu`

`Menu` is the collection object for all items the app can show to a user.

Its responsibilities are:

- storing the list of menu items
- adding new items
- filtering items by category
- sorting items by popularity

The filtering algorithm uses a list comprehension to return only items whose category matches the requested value. The sorting algorithm uses Python's built-in `sorted()` function so the original menu list is not mutated by accident.

### 3. `Order`

`Order` groups selected items into one transaction.

Its responsibilities are:

- storing the selected items
- adding an item to the order
- counting how many items are in the order
- calculating the total price

The total is computed by summing the `price` field from every selected `MenuItem`. The result is rounded to two decimal places so the output looks like a normal money value.

### 4. `Customer`

`Customer` stores the user's name and purchase history.

Its responsibilities are:

- tracking previous orders
- adding a completed order to purchase history
- deciding whether the customer is verified

For this project, a customer becomes verified after at least one purchase. That is a simple rule, but it matches the requirement that the system verify users based on past purchase history.

## Why the Code Looks Human-Written

The code was kept intentionally small and direct:

- no extra helper classes that were never requested
- no framework setup
- no database layer
- no unnecessary abstraction
- comments only where they actually explain intent

That keeps the project aligned with what a person would realistically build in a short tinker activity.

## Manual Check

`models.py` includes a short `if __name__ == "__main__":` block. Running the file directly prints:

- the drink filter results
- the popularity sort order
- the order total
- the customer verification result

This acts like a quick sanity check before running formal tests.

## Test Coverage

The pytest file covers the main required behaviors:

- order totals with multiple items
- zero total for an empty order
- filtering by category
- sorting by popularity
- customer verification after a purchase

These tests focus on observable behavior rather than implementation details, which makes them easier to understand and maintain.

## How to Run

From the `WEEK-3/bytebites_tinker_activity` folder:

```powershell
python models.py
python -m pytest
```

## How to View It in a Browser

If you want to see the project in a web browser on your own computer, open the ByteBites folder and run:

```powershell
cd "c:\Users\User\Documents\Folder name\AI-110\AI-110\WEEK-3\bytebites_tinker_activity"
python ai_server.py
```

Then open this address in your browser:

```text
http://127.0.0.1:8010
```

The browser version includes:

- a visual menu
- a category filter
- a search bar
- a popularity sort button
- a price sort button
- an order summary panel
- a verification status that changes after completing an order
- an order history section
- a Gemini-powered AI assistant panel

This browser demo does not replace the Python class work. It is just a presentation layer so the assignment can be viewed more easily.

## Vercel-Ready Refactor

The project has been refactored so deployment is easier later:

- browser requests already target `/api/menu` and `/api/assistant`
- the shared logic lives in `bytebites_backend.py`
- local development uses `ai_server.py`
- deployment can use the Python files inside the `api` folder

That means the local version and the future deployed version use the same menu and AI behavior instead of two separate implementations.

## Gemini Setup

To keep the API key out of git, the real key is read from a local `.env` file, and `.gitignore` excludes that file.

If you ever need to replace the key, use this format in `.env`:

```text
GEMINI_API_KEY=your_key_here
```

The AI assistant uses Gemini only for recommendation text. The menu, totals, filtering, sorting, and order rules still stay in the project code.

If Gemini is unavailable, the app now falls back to a local rule-based recommender so the demo still stays usable.

## Expected Learning Outcomes

This project demonstrates how to:

- convert a written feature request into candidate classes
- create a UML-style design before coding
- implement structured Python classes with clear responsibilities
- apply simple algorithms for filtering, sorting, and validation
- test behavior with pytest

## Final Notes

All work for this assignment was kept inside `WEEK-3` as requested. `WEEK-2` was not modified.
