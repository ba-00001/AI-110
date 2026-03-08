"""Basic ByteBites class implementation for the original Week 3 assignment."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MenuItem:
    """Store one item that appears on the ByteBites menu."""

    name: str
    price: float
    category: str
    popularity_rating: float

    def matches_category(self, category: str) -> bool:
        """Return True when the item category matches the requested category."""
        return self.category.strip().lower() == category.strip().lower()


@dataclass
class Order:
    """Group selected menu items into one transaction."""

    selected_items: list[MenuItem] = field(default_factory=list)

    def add_item(self, item: MenuItem) -> None:
        """Add one menu item to the current order."""
        self.selected_items.append(item)

    def calculate_total(self) -> float:
        """Return the total price for all selected items."""
        return round(sum(item.price for item in self.selected_items), 2)

    def item_count(self) -> int:
        """Return the number of items in the order."""
        return len(self.selected_items)


@dataclass
class Customer:
    """Store customer identity and previous orders."""

    name: str
    purchase_history: list[Order] = field(default_factory=list)

    def add_purchase(self, order: Order) -> None:
        """Save a completed order to the customer's history."""
        self.purchase_history.append(order)

    def is_verified(self) -> bool:
        """A customer is verified after at least one past purchase."""
        return len(self.purchase_history) > 0


@dataclass
class Menu:
    """Store the collection of available ByteBites items."""

    items: list[MenuItem] = field(default_factory=list)

    def add_item(self, item: MenuItem) -> None:
        """Add one item to the menu."""
        self.items.append(item)

    def filter_by_category(self, category: str) -> list[MenuItem]:
        """Return items that belong to the requested category."""
        return [item for item in self.items if item.matches_category(category)]

    def sort_by_popularity(self, descending: bool = True) -> list[MenuItem]:
        """Return a new list sorted by popularity."""
        return sorted(
            self.items,
            key=lambda item: item.popularity_rating,
            reverse=descending,
        )


def build_sample_menu() -> Menu:
    """Create a small sample menu for basic manual testing."""
    menu = Menu()
    menu.add_item(MenuItem("Spicy Burger", 8.75, "Entrees", 4.8))
    menu.add_item(MenuItem("Large Soda", 2.50, "Drinks", 4.1))
    menu.add_item(MenuItem("Chocolate Cookie", 1.95, "Desserts", 4.6))
    menu.add_item(MenuItem("Iced Tea", 2.75, "Drinks", 4.4))
    return menu


if __name__ == "__main__":
    # This manual check keeps the basic version aligned with the original task.
    sample_menu = build_sample_menu()
    sample_order = Order([sample_menu.items[0], sample_menu.items[1]])
    sample_customer = Customer("Jordan Lee")
    sample_customer.add_purchase(sample_order)

    print("Drink filter:", [item.name for item in sample_menu.filter_by_category("Drinks")])
    print("Popularity sort:", [item.name for item in sample_menu.sort_by_popularity()])
    print("Order total:", sample_order.calculate_total())
    print("Customer verified:", sample_customer.is_verified())
