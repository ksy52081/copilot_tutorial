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
    assert response.status_code == 404
    assert "Menu with id 999 not found" in response.json()["detail"]


def test_menu_for_nonexistent_event(client: TestClient):
    response = client.post("/api/events/999/menus", json={"name": "Test Menu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


def test_duplicate_menu_name_error(client: TestClient):
    """Test scenario 1: Error when adding menu with duplicate name"""
    # Create an event
    event_response = client.post("/api/events/", json={"name": "Test Event"})
    event_id = event_response.json()["id"]
    
    # Add first menu
    first_menu_response = client.post(
        f"/api/events/{event_id}/menus",
        json={"name": "Pizza"}
    )
    assert first_menu_response.status_code == 200
    
    # Try to add menu with same name - should fail
    duplicate_menu_response = client.post(
        f"/api/events/{event_id}/menus",
        json={"name": "Pizza"}
    )
    assert duplicate_menu_response.status_code == 400
    assert "already exists for this event" in duplicate_menu_response.json()["detail"]
    assert "Pizza" in duplicate_menu_response.json()["detail"]


def test_vote_with_invalid_menu_id_error(client: TestClient):
    """Test scenario 2: Error when voting with non-existent menu ID"""
    # Create an event
    event_response = client.post("/api/events/", json={"name": "Test Event"})
    event_id = event_response.json()["id"]
    
    # Try to vote for non-existent menu ID - should fail
    vote_response = client.post(
        f"/api/events/{event_id}/votes",
        json={"menu_id": 999}
    )
    assert vote_response.status_code == 404
    assert "Menu with id 999 not found" in vote_response.json()["detail"]


def test_vote_with_menu_from_different_event_error(client: TestClient):
    """Test additional scenario: Error when voting with menu from different event"""
    # Create two events
    event1_response = client.post("/api/events/", json={"name": "Event 1"})
    event1_id = event1_response.json()["id"]
    
    event2_response = client.post("/api/events/", json={"name": "Event 2"})
    event2_id = event2_response.json()["id"]
    
    # Add menu to event 1
    menu_response = client.post(
        f"/api/events/{event1_id}/menus",
        json={"name": "Pizza"}
    )
    menu_id = menu_response.json()["id"]
    
    # Try to vote for event1's menu in event2 - should fail
    vote_response = client.post(
        f"/api/events/{event2_id}/votes",
        json={"menu_id": menu_id}
    )
    assert vote_response.status_code == 400
    assert "Menu does not belong to this event" in vote_response.json()["detail"] 