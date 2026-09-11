from __future__ import annotations

import argparse
import hmac
import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .server import MUDServer


STATIC_DIR = Path(__file__).with_name("static")
RENDER_DATA_DIR = Path("/var/data")


def default_bind_host() -> str:
    return os.environ.get("HOST", "0.0.0.0" if "PORT" in os.environ else "127.0.0.1")


def account_database_path() -> str:
    """Choose account storage and reject ephemeral Render configurations."""
    configured = os.environ.get("BREWMUD_DB_PATH")
    if os.environ.get("RENDER", "").casefold() != "true":
        return configured or "brewmud.db"

    if not configured:
        raise RuntimeError(
            "Persistent account storage is not configured. In Render, attach a disk "
            "at /var/data and set BREWMUD_DB_PATH=/var/data/brewmud.db."
        )

    database = Path(configured).expanduser().resolve()
    try:
        database.relative_to(RENDER_DATA_DIR)
    except ValueError as exc:
        raise RuntimeError(
            "BREWMUD_DB_PATH must be inside Render's persistent /var/data disk "
            "(recommended: /var/data/brewmud.db)."
        ) from exc

    if not RENDER_DATA_DIR.is_mount():
        raise RuntimeError(
            "BREWMUD_DB_PATH points to /var/data, but no persistent disk is mounted "
            "there. Add the disk on the Render service's Disks page before accepting accounts."
        )
    return str(database)


def instructor_password_matches(provided: str, configured: str) -> bool:
    return bool(configured) and hmac.compare_digest(provided, configured)


class BrewMUDHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, server_address, handler_class=BaseHTTPRequestHandler):
        database_path = account_database_path()
        super().__init__(server_address, handler_class)
        self.database_path = database_path
        self.storage_mode = "persistent" if os.environ.get("RENDER", "").casefold() == "true" else "local"
        self.world = MUDServer(self.database_path)
        self.instructor_password = os.environ.get("BREWMUD_ADMIN_PASSWORD", "")

    def server_close(self) -> None:
        self.world.close()
        super().server_close()


class RequestHandler(BaseHTTPRequestHandler):
    server: BrewMUDHTTPServer

    def do_HEAD(self) -> None:
        """Answer platform availability probes without sending a response body."""
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/api/status"}:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", "0")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return
        self.send_response(HTTPStatus.NOT_FOUND)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
            return
        if parsed.path == "/instructor":
            self._send_file(STATIC_DIR / "instructor.html", "text/html; charset=utf-8")
            return
        if parsed.path == "/app.js":
            self._send_file(STATIC_DIR / "app.js", "text/javascript; charset=utf-8")
            return
        if parsed.path == "/style.css":
            self._send_file(STATIC_DIR / "style.css", "text/css; charset=utf-8")
            return
        if parsed.path == "/instructor.js":
            self._send_file(STATIC_DIR / "instructor.js", "text/javascript; charset=utf-8")
            return
        if parsed.path == "/instructor.css":
            self._send_file(STATIC_DIR / "instructor.css", "text/css; charset=utf-8")
            return
        if parsed.path == "/api/events":
            token = parse_qs(parsed.query).get("token", [""])[0]
            try:
                self._json({"messages": self.server.world.poll(token)})
            except KeyError as exc:
                self._json({"error": str(exc)}, HTTPStatus.UNAUTHORIZED)
            return
        if parsed.path == "/api/status":
            self._json({"players": self.server.world.player_count(),
                        "account_storage": self.server.storage_mode})
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
                token, output = self.server.world.login(
                    str(body.get("name", "")), str(body.get("password", ""))
                )
                self._json({"token": token, "output": output, "show_instructions": False,
                            "awaiting_continue": self.server.world.awaiting_continue(token)})
            except ValueError as exc:
                self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return
        if self.path == "/api/register":
            try:
                token, output = self.server.world.register(
                    str(body.get("name", "")), str(body.get("password", ""))
                )
                self._json({"token": token, "output": output, "show_instructions": True,
                            "awaiting_continue": self.server.world.awaiting_continue(token)},
                           HTTPStatus.CREATED)
            except ValueError as exc:
                self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return
        if self.path == "/api/command":
            try:
                output = self.server.world.command(str(body.get("token", "")), str(body.get("command", "")))
                token = str(body.get("token", ""))
                self._json({"output": output,
                            "awaiting_continue": self.server.world.awaiting_continue(token)})
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
        if self.path == "/api/instructor/progress":
            if not self.server.instructor_password:
                self._json(
                    {"error": "Instructor tracking is not configured."},
                    HTTPStatus.SERVICE_UNAVAILABLE,
                )
                return
            if not instructor_password_matches(
                str(body.get("password", "")), self.server.instructor_password
            ):
                self._json({"error": "Incorrect instructor password."}, HTTPStatus.UNAUTHORIZED)
                return
            self._json({"players": self.server.world.instructor_progress()})
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
    parser.add_argument("--host", default=default_bind_host(),
                        help="Address to bind (default: localhost only)")
    parser.add_argument("--port", default=int(os.environ.get("PORT", "8000")), type=int,
                        help="Port to bind (default: 8000, or the PORT environment variable)")
    args = parser.parse_args()
    server = BrewMUDHTTPServer((args.host, args.port), RequestHandler)
    print(f"BrewMUD is running at http://{args.host}:{args.port}")
    print(f"Account storage: {server.storage_mode} ({server.database_path})")
    print("Press Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBrewMUD stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
