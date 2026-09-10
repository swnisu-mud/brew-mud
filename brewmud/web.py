from __future__ import annotations

import argparse
import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .server import MUDServer


STATIC_DIR = Path(__file__).with_name("static")


class BrewMUDHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, server_address, handler_class=BaseHTTPRequestHandler):
        super().__init__(server_address, handler_class)
        self.world = MUDServer()


class RequestHandler(BaseHTTPRequestHandler):
    server: BrewMUDHTTPServer

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
            return
        if parsed.path == "/app.js":
            self._send_file(STATIC_DIR / "app.js", "text/javascript; charset=utf-8")
            return
        if parsed.path == "/style.css":
            self._send_file(STATIC_DIR / "style.css", "text/css; charset=utf-8")
            return
        if parsed.path == "/api/events":
            token = parse_qs(parsed.query).get("token", [""])[0]
            try:
                self._json({"messages": self.server.world.poll(token)})
            except KeyError as exc:
                self._json({"error": str(exc)}, HTTPStatus.UNAUTHORIZED)
            return
        if parsed.path == "/api/status":
            self._json({"players": self.server.world.player_count()})
            return
        self._json({"error": "Not found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        try:
            body = self._read_json()
        except (ValueError, json.JSONDecodeError) as exc:
            self._json({"error": f"Invalid request: {exc}"}, HTTPStatus.BAD_REQUEST)
            return

        if self.path == "/api/login":
            try:
                token, output = self.server.world.login(str(body.get("name", "")))
                self._json({"token": token, "output": output})
            except ValueError as exc:
                self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return
        if self.path == "/api/command":
            try:
                output = self.server.world.command(str(body.get("token", "")), str(body.get("command", "")))
                self._json({"output": output})
            except KeyError as exc:
                self._json({"error": str(exc)}, HTTPStatus.UNAUTHORIZED)
            return
        if self.path == "/api/logout":
            try:
                self.server.world.logout(str(body.get("token", "")))
                self._json({"ok": True})
            except KeyError:
                self._json({"ok": True})
            return
        self._json({"error": "Not found"}, HTTPStatus.NOT_FOUND)

    def _read_json(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0"))
        if length > 10_000:
            raise ValueError("request is too large")
        data = json.loads(self.rfile.read(length) or b"{}")
        if not isinstance(data, dict):
            raise ValueError("JSON body must be an object")
        return data

    def _json(self, data: dict[str, object], status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(encoded)

    def _send_file(self, path: Path, content_type: str) -> None:
        try:
            data = path.read_bytes()
        except OSError:
            self._json({"error": "Asset not found"}, HTTPStatus.NOT_FOUND)
            return
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args) -> None:
        # Keep request logs concise while retaining useful local diagnostics.
        super().log_message(format, *args)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the BrewMUD multiplayer web server")
    parser.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"),
                        help="Address to bind (default: localhost only)")
    parser.add_argument("--port", default=int(os.environ.get("PORT", "8000")), type=int,
                        help="Port to bind (default: 8000, or the PORT environment variable)")
    args = parser.parse_args()
    server = BrewMUDHTTPServer((args.host, args.port), RequestHandler)
    print(f"BrewMUD is running at http://{args.host}:{args.port}")
    print("Press Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBrewMUD stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
