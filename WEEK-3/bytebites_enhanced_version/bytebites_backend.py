"""Shared backend helpers used by both local development and Vercel API routes."""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib import error, parse, request

from models import build_sample_menu


PROJECT_ROOT = Path(__file__).resolve().parent
ENV_PATH = PROJECT_ROOT / ".env"


def load_env_file() -> None:
    """Load simple KEY=VALUE pairs from the local .env file for local development."""
    if not ENV_PATH.exists():
        return

    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def get_menu_payload() -> list[dict[str, object]]:
    """Convert Python menu items into plain dictionaries for JSON responses."""
    menu = build_sample_menu()
    return [
        {
            "name": item.name,
            "price": item.price,
            "category": item.category,
            "popularityRating": item.popularity_rating,
        }
        for item in menu.items
    ]


def build_assistant_prompt(user_message: str, order_items: list[str]) -> str:
    """Build a controlled prompt that limits the model to the real ByteBites menu."""
    menu_json = json.dumps(get_menu_payload(), indent=2)
    order_summary = ", ".join(order_items) if order_items else "No current order items"

    return (
        "You are the ByteBites ordering assistant. "
        "Only recommend items that exist in the provided menu. "
        "Keep answers short, helpful, and natural. "
        "If the user asks for suggestions, mention item names, prices, and a brief reason. "
        "Do not invent menu items.\n\n"
        f"Current order: {order_summary}\n\n"
        f"Menu:\n{menu_json}\n\n"
        f"User request: {user_message}"
    )


def build_local_fallback_reply(user_message: str, order_items: list[str]) -> str:
    """Return a local rule-based reply so the demo still works without Gemini."""
    normalized_message = user_message.lower()
    items = get_menu_payload()

    if "drink" in normalized_message:
        candidates = [item for item in items if item["category"] == "Drinks"]
    elif "dessert" in normalized_message:
        candidates = [item for item in items if item["category"] == "Desserts"]
    elif "entree" in normalized_message or "meal" in normalized_message:
        candidates = [item for item in items if item["category"] == "Entrees"]
    else:
        candidates = items

    if "cheap" in normalized_message or "budget" in normalized_message or "under $" in normalized_message:
        candidates = sorted(candidates, key=lambda item: float(item["price"]))[:3]
    else:
        candidates = sorted(candidates, key=lambda item: float(item["popularityRating"]), reverse=True)[:3]

    order_note = f" Current order: {', '.join(order_items)}." if order_items else ""
    recommendation_lines = [
        f"- {item['name']} (${float(item['price']):.2f}) in {item['category']}"
        for item in candidates
    ]

    return (
        "Gemini is unavailable right now, so ByteBites switched to a local fallback recommender."
        f"{order_note}\n"
        "Here are good options based on your request:\n"
        + "\n".join(recommendation_lines)
    )


def call_gemini(user_message: str, order_items: list[str]) -> str:
    """Send the controlled ByteBites prompt to Gemini and return the text response."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return build_local_fallback_reply(user_message, order_items)

    prompt = build_assistant_prompt(user_message, order_items)
    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={parse.quote(api_key)}"
    )
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt,
                    }
                ]
            }
        ]
    }
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    gemini_request = request.Request(endpoint, data=body, headers=headers, method="POST")

    try:
        with request.urlopen(gemini_request, timeout=20) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        return (
            f"Gemini request failed with HTTP {exc.code}. "
            f"{details}\n\n{build_local_fallback_reply(user_message, order_items)}"
        )
    except Exception as exc:  # pragma: no cover - network-dependent fallback
        return (
            f"Gemini request could not be completed: {exc}\n\n"
            f"{build_local_fallback_reply(user_message, order_items)}"
        )

    candidates = response_payload.get("candidates", [])
    if not candidates:
        return build_local_fallback_reply(user_message, order_items)

    parts = candidates[0].get("content", {}).get("parts", [])
    text_parts = [part.get("text", "") for part in parts if part.get("text")]
    return "\n".join(text_parts).strip() or build_local_fallback_reply(user_message, order_items)
