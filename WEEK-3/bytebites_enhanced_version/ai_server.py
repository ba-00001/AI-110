"""Local ByteBites browser server that mirrors the future Vercel API routes."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from bytebites_backend import call_gemini, get_menu_payload, load_env_file


PROJECT_ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8010


class ByteBitesHandler(SimpleHTTPRequestHandler):
    """Serve the static app files and mirror the future `/api/*` routes locally."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/api/menu":
            self._send_json({"items": get_menu_payload()})
            return

        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/assistant":
            self.send_error(HTTPStatus.NOT_FOUND, "Unknown API route")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(content_length).decode("utf-8") or "{}")
        user_message = str(payload.get("message", "")).strip()
        order_items = payload.get("orderItems", [])

        if not user_message:
            self._send_json({"reply": "Ask ByteBites AI a menu question to get a recommendation."}, HTTPStatus.BAD_REQUEST)
            return

        reply = call_gemini(user_message, order_items if isinstance(order_items, list) else [])
        self._send_json({"reply": reply})

    def log_message(self, format: str, *args) -> None:
        """Keep the terminal output compact while serving the local demo."""
        print(f"[ByteBites] {format % args}")

    def _send_json(self, payload: dict[str, object], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server() -> None:
    """Start the local ByteBites AI demo server."""
    load_env_file()
    server = ThreadingHTTPServer((HOST, PORT), ByteBitesHandler)
    print(f"ByteBites AI server running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
