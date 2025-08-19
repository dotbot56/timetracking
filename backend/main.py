from dataclasses import dataclass, field, asdict, is_dataclass
from datetime import date, time
from typing import List, Optional


@dataclass
class Expense:
    """Simple expense representation."""
    type: str
    amount: float
    note: Optional[str] = None


@dataclass
class TimeEntry:
    """Time entry recorded by a user on a site."""
    id: int
    user_id: int
    site_id: int
    date: date
    start_time: time
    end_time: time
    lunch_flat_applied: bool = False
    travel_minutes: int = 0
    expenses: List[Expense] = field(default_factory=list)


entries: List[TimeEntry] = []


def list_entries() -> List[TimeEntry]:
    """Return all stored time entries."""
    return entries


def create_entry(entry: TimeEntry) -> TimeEntry:
    """Store a new time entry, ensuring unique IDs."""
    if any(e.id == entry.id for e in entries):
        raise ValueError("Duplicate entry ID")
    entries.append(entry)
    return entry


# Helper used by server and tests to convert dataclasses to JSON serialisable dicts

def as_dict(obj):
    """Recursively convert dataclasses to dictionaries.

    Supports dataclass instances as well as lists and dictionaries containing
    dataclasses so that server responses can be JSON serialised.
    """
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, list):
        return [as_dict(item) for item in obj]
    if isinstance(obj, dict):
        return {key: as_dict(value) for key, value in obj.items()}
    return obj

    
