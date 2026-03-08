"""Core ByteBites models used for the Week 3 tinker activity.

Classes in this file:
- Customer: tracks a user's name and previous orders.
- MenuItem: stores information about one food or drink item.
- Menu: stores the full collection of items and supports filtering/sorting.
- Order: groups selected items and computes the transaction total.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MenuItem:
    """Represent one menu entry that a customer can browse or order."""

    name: str
    price: float
    category: str
    popularity_rating: float

    def matches_category(self, category: str) -> bool:
        """Return True when the item belongs to the requested category."""
        return self.category.strip().lower() == category.strip().lower()


@dataclass
class Order:
    """Represent a single transaction made up of selected menu items."""

    selected_items: list[MenuItem] = field(default_factory=list)

    def add_item(self, item: MenuItem) -> None:
        """Append a menu item to the transaction."""
        self.selected_items.append(item)

    def calculate_total(self) -> float:
        """Add the prices of all selected items and return the total."""
        total = sum(item.price for item in self.selected_items)
        return round(total, 2)

    def item_count(self) -> int:
        """Return the number of items currently in the order."""
        return len(self.selected_items)


@dataclass
class Customer:
    """Represent a customer and the orders already placed by that user."""

    name: str
    purchase_history: list[Order] = field(default_factory=list)

    def add_purchase(self, order: Order) -> None:
        """Store a completed order in the customer's history."""
        self.purchase_history.append(order)

    def is_verified(self) -> bool:
        """Treat customers with at least one previous order as verified."""
        return len(self.purchase_history) > 0


@dataclass
class Menu:
    """Represent the full collection of ByteBites menu items."""

    items: list[MenuItem] = field(default_factory=list)

    def add_item(self, item: MenuItem) -> None:
        """Add one new menu item to the menu collection."""
        self.items.append(item)

    def filter_by_category(self, category: str) -> list[MenuItem]:
        """Return only the items that match the requested category."""
        return [item for item in self.items if item.matches_category(category)]

    def sort_by_popularity(self, descending: bool = True) -> list[MenuItem]:
        """Return a new list sorted by popularity without mutating the menu."""
        return sorted(
            self.items,
            key=lambda item: item.popularity_rating,
            reverse=descending,
        )


def build_sample_menu() -> Menu:
    """Create a small sample menu for quick manual checking."""
    menu = Menu()
    menu.add_item(MenuItem("Spicy Burger", 8.75, "Entrees", 4.8))
    menu.add_item(MenuItem("Large Soda", 2.50, "Drinks", 4.1))
    menu.add_item(MenuItem("Chocolate Cookie", 1.95, "Desserts", 4.6))
    menu.add_item(MenuItem("Iced Tea", 2.75, "Drinks", 4.4))
    menu.add_item(MenuItem("Loaded Fries", 4.95, "Entrees", 4.5))
    menu.add_item(MenuItem("Vanilla Shake", 3.95, "Desserts", 4.7))
    menu.add_item(MenuItem("Chicken Wrap", 7.25, "Entrees", 4.3))
    menu.add_item(MenuItem("Strawberry Lemonade", 3.10, "Drinks", 4.2))
    menu.add_item(MenuItem("Apple Pie Bites", 3.50, "Desserts", 4.5))
    menu.add_item(MenuItem("Buffalo Tenders", 6.85, "Entrees", 4.6))
    return menu


if __name__ == "__main__":
    # This small demo gives a quick human-readable sanity check without pytest.
    sample_menu = build_sample_menu()
    drink_names = [item.name for item in sample_menu.filter_by_category("drinks")]
    popular_names = [item.name for item in sample_menu.sort_by_popularity()]

    sample_order = Order()
    sample_order.add_item(sample_menu.items[0])
    sample_order.add_item(sample_menu.items[1])

    sample_customer = Customer("Jordan Lee")
    sample_customer.add_purchase(sample_order)

    print("Drink filter:", drink_names)
    print("Popularity sort:", popular_names)
    print("Order total:", sample_order.calculate_total())
    print("Customer verified:", sample_customer.is_verified())
