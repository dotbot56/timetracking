from datetime import date, time

import pytest

from backend.main import (
    Expense,
    TimeEntry,
    User,
    create_entry,
    list_entries,
    register_user,
    login_user,
    list_pending_users,
    approve_user,
    users,
)


def test_create_and_list_entries():
    entry = TimeEntry(
        id=1,
        user_id=1,
        site_id=1,
        date=date(2024, 1, 1),
        start_time=time(8, 0, 0),
        end_time=time(16, 0, 0),
        lunch_flat_applied=False,
        travel_minutes=0,
        expenses=[],
    )
    created = create_entry(entry)
    assert created.id == 1
    entries = list_entries()
    assert len(entries) == 1
    assert entries[0].id == 1


def test_user_registration_and_login():
    users.clear()
    users["admin"] = User("admin", "admin", "admin", True)
    register_user("alice", "pw")
    pending = list_pending_users()
    assert any(u.username == "alice" for u in pending)
    with pytest.raises(ValueError):
        login_user("alice", "pw")
    approve_user("alice", "mitarbeiter")
    user = login_user("alice", "pw")
    assert user.role == "mitarbeiter"
