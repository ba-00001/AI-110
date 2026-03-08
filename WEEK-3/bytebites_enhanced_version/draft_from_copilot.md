# Draft UML From Standard AI Prompt

This file represents an early rough draft before refinement.

```text
+------------------+
| Customer         |
+------------------+
| name             |
| purchase_history |
+------------------+
| add_purchase()   |
| is_verified()    |
+------------------+

+------------------+
| MenuItem         |
+------------------+
| name             |
| price            |
| category         |
| popularity       |
+------------------+

+------------------+
| Menu             |
+------------------+
| items            |
+------------------+
| add_item()       |
| filter_category()|
| sort_popularity()|
+------------------+

+------------------+
| Order            |
+------------------+
| customer         |
| selected_items   |
+------------------+
| add_item()       |
| total_cost()     |
+------------------+
```

## Review Notes
- This draft was close, but it introduced a `customer` link inside `Order` that the feature request did not require.
- The method names needed cleanup so they matched a consistent style.
- The final design keeps the same four classes, but removes any unnecessary structure.
