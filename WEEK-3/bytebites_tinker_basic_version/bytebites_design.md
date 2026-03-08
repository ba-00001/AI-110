# Final ByteBites UML Design

```text
+-----------------------------------------------------------+
| Customer                                                  |
+-----------------------------------------------------------+
| - name: str                                               |
| - purchase_history: list[Order]                           |
+-----------------------------------------------------------+
| + add_purchase(order: Order) -> None                      |
| + is_verified() -> bool                                   |
+-----------------------------------------------------------+

+-----------------------------------------------------------+
| MenuItem                                                  |
+-----------------------------------------------------------+
| - name: str                                               |
| - price: float                                            |
| - category: str                                           |
| - popularity_rating: float                                |
+-----------------------------------------------------------+
| + matches_category(category: str) -> bool                 |
+-----------------------------------------------------------+

+-----------------------------------------------------------+
| Menu                                                      |
+-----------------------------------------------------------+
| - items: list[MenuItem]                                   |
+-----------------------------------------------------------+
| + add_item(item: MenuItem) -> None                        |
| + filter_by_category(category: str) -> list[MenuItem]     |
| + sort_by_popularity(descending: bool = True)             |
|   -> list[MenuItem]                                       |
+-----------------------------------------------------------+

+-----------------------------------------------------------+
| Order                                                     |
+-----------------------------------------------------------+
| - selected_items: list[MenuItem]                          |
+-----------------------------------------------------------+
| + add_item(item: MenuItem) -> None                        |
| + calculate_total() -> float                              |
| + item_count() -> int                                     |
+-----------------------------------------------------------+
```

## Relationship Summary
- A `Menu` contains many `MenuItem` objects.
- An `Order` contains many selected `MenuItem` objects.
- A `Customer` keeps a history of past `Order` objects.

## Why This Design Fits the Spec
- It models the four core nouns from the feature request directly.
- It keeps data storage and behavior close together in each class.
- It supports the three required behaviors: filtering menu items, sorting by popularity, and calculating totals.
