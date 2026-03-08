"""Pytest coverage for the ByteBites models."""

from models import Customer, Menu, MenuItem, Order


def build_menu() -> Menu:
    """Create a reusable menu fixture without relying on pytest fixtures."""
    menu = Menu()
    menu.add_item(MenuItem("Spicy Burger", 8.75, "Entrees", 4.8))
    menu.add_item(MenuItem("Large Soda", 2.50, "Drinks", 4.1))
    menu.add_item(MenuItem("Iced Tea", 2.75, "Drinks", 4.4))
    menu.add_item(MenuItem("Brownie", 3.25, "Desserts", 4.7))
    return menu


def test_calculate_total_with_multiple_items() -> None:
    """Order totals should include every selected item."""
    menu = build_menu()
    order = Order([menu.items[0], menu.items[1], menu.items[3]])

    assert order.calculate_total() == 14.50


def test_order_total_is_zero_when_empty() -> None:
    """An empty order should safely return a total of zero."""
    order = Order()

    assert order.calculate_total() == 0


def test_filter_by_category_returns_only_matching_items() -> None:
    """Filtering drinks should not return entrees or desserts."""
    menu = build_menu()

    drinks = menu.filter_by_category("Drinks")

    assert [item.name for item in drinks] == ["Large Soda", "Iced Tea"]


def test_sort_by_popularity_returns_highest_rated_first() -> None:
    """Sorting should place the most popular item at the front by default."""
    menu = build_menu()

    sorted_items = menu.sort_by_popularity()

    assert [item.name for item in sorted_items] == [
        "Spicy Burger",
        "Brownie",
        "Iced Tea",
        "Large Soda",
    ]


def test_customer_is_verified_after_first_purchase() -> None:
    """Verification should change once a customer has order history."""
    customer = Customer("Jordan Lee")
    order = Order([MenuItem("Large Soda", 2.50, "Drinks", 4.1)])

    assert customer.is_verified() is False

    customer.add_purchase(order)

    assert customer.is_verified() is True
