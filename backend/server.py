"""Simple HTTP server exposing time entry endpoints."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from typing import Any

from datetime import date as dt_date, time as dt_time

from backend.main import (
    TimeEntry,
    Expense,
    as_dict,
    create_entry,
    list_entries,
    register_user,
    login_user,
    list_pending_users,
    approve_user,
)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: Any) -> None:
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/time-entries":
            data = [as_dict(e) for e in list_entries()]
            self._send(200, data)
        elif self.path == "/users/pending":
            data = [as_dict(u) for u in list_pending_users()]
            self._send(200, data)
        else:
            self._send(404, {"detail": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/time-entries":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            entry = TimeEntry(
                id=data["id"],
                user_id=data["user_id"],
                site_id=data["site_id"],
                date=dt_date.fromisoformat(data["date"]),
                start_time=dt_time.fromisoformat(data["start_time"]),
                end_time=dt_time.fromisoformat(data["end_time"]),
                lunch_flat_applied=data.get("lunch_flat_applied", False),
                travel_minutes=data.get("travel_minutes", 0),
                expenses=[Expense(**exp) for exp in data.get("expenses", [])],
            )
            created = create_entry(entry)
            self._send(200, as_dict(created))
        elif self.path == "/register":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            try:
                user = register_user(data["username"], data["password"])
                self._send(201, as_dict(user))
            except ValueError as exc:
                self._send(400, {"detail": str(exc)})
        elif self.path == "/login":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            try:
                user = login_user(data["username"], data["password"])
                self._send(200, as_dict(user))
            except ValueError as exc:
                self._send(403, {"detail": str(exc)})
        elif self.path == "/users/approve":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            try:
                user = approve_user(data["username"], data["role"])
                self._send(200, as_dict(user))
            except ValueError as exc:
                self._send(400, {"detail": str(exc)})
        else:
            self._send(404, {"detail": "Not found"})

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run(port: int = 8000) -> None:
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Serving on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    run()

