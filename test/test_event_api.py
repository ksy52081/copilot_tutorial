import pytest
from fastapi.testclient import TestClient


def test_create_event(client: TestClient):
    response = client.post("/api/events/", json={"name": "Team Lunch"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Team Lunch"
    assert "id" in data


def test_get_all_events(client: TestClient):
    # Create some events first
    client.post("/api/events/", json={"name": "Event 1"})
    client.post("/api/events/", json={"name": "Event 2"})
    
    response = client.get("/api/events/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Event 1"
    assert data[1]["name"] == "Event 2"


def test_get_event_by_id(client: TestClient):
    # Create an event first
    create_response = client.post("/api/events/", json={"name": "Test Event"})
    event_id = create_response.json()["id"]
    
    response = client.get(f"/api/events/{event_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Event"
    assert data["id"] == event_id


def test_get_nonexistent_event(client: TestClient):
    response = client.get("/api/events/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found" 