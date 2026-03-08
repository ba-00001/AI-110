# ByteBites Feature Specification

## Client Feature Request
We need to build the backend logic for the ByteBites app. The system needs to manage our customers, tracking their names and their past purchase history so the system can verify they are real users.

These customers need to browse specific food items (like a "Spicy Burger" or "Large Soda"), so we must track the name, price, category, and popularity rating for every item we sell.

We also need a way to manage the full collection of items - a digital list that holds all items and lets us filter by category such as "Drinks" or "Desserts".

Finally, when a user picks items, we need to group them into a single transaction. This transaction object should store the selected items and compute the total cost.

## Candidate Classes
1. `Customer`
2. `MenuItem`
3. `Menu`
4. `Order`

## Interpretation Notes
- `Customer` should store a name and a list of previous purchases.
- `MenuItem` is the individual food or drink entry the customer can browse.
- `Menu` is the collection object responsible for storing, filtering, and sorting items.
- `Order` groups selected items into one transaction and calculates the final total.

## Design Boundaries
- Keep the design focused on the four classes above.
- Use simple Python data structures instead of databases or web frameworks.
- Support filtering by category, sorting items by popularity, and calculating order totals.
