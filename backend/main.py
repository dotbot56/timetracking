from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date, time
from typing import List, Optional

app = FastAPI(title="Timetracking API")

class Expense(BaseModel):
    type: str
    amount: float
    note: Optional[str] = None

class TimeEntry(BaseModel):
    id: int
    user_id: int
    site_id: int
    date: date
    start_time: time
    end_time: time
    lunch_flat_applied: bool = False
    travel_minutes: int = 0
    expenses: List[Expense] = []

entries: List[TimeEntry] = []

@app.get("/time-entries", response_model=List[TimeEntry])
def list_entries() -> List[TimeEntry]:
    """Return all stored time entries."""
    return entries

@app.post("/time-entries", response_model=TimeEntry)
def create_entry(entry: TimeEntry) -> TimeEntry:
    """Create a new time entry in memory."""
    if any(e.id == entry.id for e in entries):
        raise HTTPException(status_code=400, detail="Duplicate entry ID")
    entries.append(entry)
    return entry

