"""Vercel-style API route for the ByteBites AI assistant."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler

from bytebites_backend import call_gemini, load_env_file


class handler(BaseHTTPRequestHandler):
    """Handle AI assistant requests from the browser."""

    def do_POST(self) -> None:  # noqa: N802
        load_env_file()
        content_length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(content_length).decode("utf-8") or "{}")
        user_message = str(payload.get("message", "")).strip()
        order_items = payload.get("orderItems", [])

        if not user_message:
            self._send_json(
                {"reply": "Ask ByteBites AI a menu question to get a recommendation."},
                HTTPStatus.BAD_REQUEST,
            )
            return

        reply = call_gemini(user_message, order_items if isinstance(order_items, list) else [])
        self._send_json({"reply": reply})

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _send_json(self, payload: dict[str, object], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
