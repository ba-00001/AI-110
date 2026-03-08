"""Vercel-style API route for serving the ByteBites menu."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler

from bytebites_backend import get_menu_payload, load_env_file


class handler(BaseHTTPRequestHandler):
    """Serve the menu payload from a Python serverless function."""

    def do_GET(self) -> None:  # noqa: N802
        load_env_file()
        payload = json.dumps({"items": get_menu_payload()}).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

