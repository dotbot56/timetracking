from datetime import date, time

from backend.main import Expense, TimeEntry, create_entry, list_entries


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
