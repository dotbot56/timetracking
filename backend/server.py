"""Simple HTTP server exposing time entry endpoints."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from typing import Any

from datetime import date as dt_date, time as dt_time

from backend.main import TimeEntry, create_entry, list_entries, as_dict, Expense


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: Any) -> None:
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/time-entries":
            data = [as_dict(e) for e in list_entries()]
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
        else:
            self._send(404, {"detail": "Not found"})


def run(port: int = 8000) -> None:
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Serving on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    run()

