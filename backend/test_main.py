from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_create_and_list_entries():
    payload = {
        "id": 1,
        "user_id": 1,
        "site_id": 1,
        "date": "2024-01-01",
        "start_time": "08:00:00",
        "end_time": "16:00:00",
        "lunch_flat_applied": False,
        "travel_minutes": 0,
        "expenses": []
    }
    response = client.post("/time-entries", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

    list_resp = client.get("/time-entries")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1
