import pytest
from fastapi.testclient import TestClient


def test_complete_voting_workflow(client: TestClient):
    # Step 1: Create an event
    event_response = client.post("/api/events/", json={"name": "Team Dinner"})
    assert event_response.status_code == 200
    event_id = event_response.json()["id"]
    
    # Step 2: Add menus to the event
    menu1_response = client.post(
        f"/api/events/{event_id}/menus",
        json={"name": "Pizza"}
    )
    assert menu1_response.status_code == 200
    menu1_id = menu1_response.json()["id"]
    
    menu2_response = client.post(
        f"/api/events/{event_id}/menus",
        json={"name": "Burger"}
    )
    assert menu2_response.status_code == 200
    menu2_id = menu2_response.json()["id"]
    
    # Step 3: Get menus for the event
    menus_response = client.get(f"/api/events/{event_id}/menus")
    assert menus_response.status_code == 200
    menus = menus_response.json()
    assert len(menus) == 2
    
    # Step 4: Vote for menus
    # Vote for Pizza (2 votes)
    client.post(f"/api/events/{event_id}/votes", json={"menu_id": menu1_id})
    client.post(f"/api/events/{event_id}/votes", json={"menu_id": menu1_id})
    
    # Vote for Burger (1 vote)
    client.post(f"/api/events/{event_id}/votes", json={"menu_id": menu2_id})
    
    # Step 5: Check voting results
    results_response = client.get(f"/api/events/{event_id}/results")
    assert results_response.status_code == 200
    results = results_response.json()
    assert len(results) == 2
    
    # Find Pizza and Burger results
    pizza_result = next(r for r in results if r["menu_name"] == "Pizza")
    burger_result = next(r for r in results if r["menu_name"] == "Burger")
    
    assert pizza_result["vote_count"] == 2
    assert burger_result["vote_count"] == 1


def test_vote_for_nonexistent_event(client: TestClient):
    response = client.post("/api/events/999/votes", json={"menu_id": 1})
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


def test_vote_for_invalid_menu(client: TestClient):
    # Create an event
    event_response = client.post("/api/events/", json={"name": "Test Event"})
    event_id = event_response.json()["id"]
    
    # Try to vote for a non-existent menu
    response = client.post(f"/api/events/{event_id}/votes", json={"menu_id": 999})
    assert response.status_code == 400
    assert "Menu not found" in response.json()["detail"]


def test_menu_for_nonexistent_event(client: TestClient):
    response = client.post("/api/events/999/menus", json={"name": "Test Menu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found" 