from dataclasses import dataclass, field, asdict, is_dataclass
from datetime import date, time
from typing import Dict, List, Optional


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


@dataclass
class User:
    """Simple user representation."""
    username: str
    password: str
    role: str = "mitarbeiter"
    approved: bool = False


users: Dict[str, User] = {"admin": User("admin", "admin", "admin", True)}


def register_user(username: str, password: str) -> User:
    """Register a new user pending approval."""
    if username in users:
        raise ValueError("Username exists")
    user = User(username=username, password=password)
    users[username] = user
    return user


def list_pending_users() -> List[User]:
    """Return users awaiting approval."""
    return [u for u in users.values() if not u.approved]


def approve_user(username: str, role: str) -> User:
    """Approve a user and set their role."""
    user = users.get(username)
    if not user:
        raise ValueError("User not found")
    user.role = role
    user.approved = True
    return user


def login_user(username: str, password: str) -> User:
    """Login a user if approved."""
    user = users.get(username)
    if not user or user.password != password or not user.approved:
        raise ValueError("Invalid credentials or not approved")
    return user


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

    
