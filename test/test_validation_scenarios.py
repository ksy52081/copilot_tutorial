from fastapi.testclient import TestClient


def test_empty_event_name_error(client: TestClient):
    """Test validation: Empty event name should fail"""
    response = client.post("/api/events/", json={"name": ""})
    assert response.status_code == 422
    assert "validation error" in response.json()["detail"][0]["type"]


def test_whitespace_only_event_name_error(client: TestClient):
    """Test validation: Whitespace-only event name should fail"""
    response = client.post("/api/events/", json={"name": "   "})
    assert response.status_code == 422
    assert "Event name cannot be empty or only whitespace" in str(response.json())


def test_too_long_event_name_error(client: TestClient):
    """Test validation: Event name exceeding max length should fail"""
    long_name = "a" * 101  # 101 characters
    response = client.post("/api/events/", json={"name": long_name})
    assert response.status_code == 422
    assert "at most 100 characters" in str(response.json())


def test_empty_menu_name_error(client: TestClient):
    """Test validation: Empty menu name should fail"""
    # Create an event first
    event_response = client.post("/api/events/", json={"name": "Test Event"})
    event_id = event_response.json()["id"]
    
    # Try to add menu with empty name
    response = client.post(f"/api/events/{event_id}/menus", json={"name": ""})
    assert response.status_code == 422
    assert "validation error" in response.json()["detail"][0]["type"]


def test_whitespace_only_menu_name_error(client: TestClient):
    """Test validation: Whitespace-only menu name should fail"""
    # Create an event first
    event_response = client.post("/api/events/", json={"name": "Test Event"})
    event_id = event_response.json()["id"]
    
    # Try to add menu with whitespace-only name
    response = client.post(f"/api/events/{event_id}/menus", json={"name": "   "})
    assert response.status_code == 422
    assert "Menu name cannot be empty or only whitespace" in str(response.json())


def test_too_long_menu_name_error(client: TestClient):
    """Test validation: Menu name exceeding max length should fail"""
    # Create an event first
    event_response = client.post("/api/events/", json={"name": "Test Event"})
    event_id = event_response.json()["id"]
    
    # Try to add menu with too long name
    long_name = "a" * 51  # 51 characters
    response = client.post(f"/api/events/{event_id}/menus", json={"name": long_name})
    assert response.status_code == 422
    assert "at most 50 characters" in str(response.json())


def test_negative_menu_id_vote_error(client: TestClient):
    """Test validation: Negative menu ID should fail"""
    # Create an event first
    event_response = client.post("/api/events/", json={"name": "Test Event"})
    event_id = event_response.json()["id"]
    
    # Try to vote with negative menu ID
    response = client.post(f"/api/events/{event_id}/votes", json={"menu_id": -1})
    assert response.status_code == 422
    assert "greater than 0" in str(response.json())


def test_zero_menu_id_vote_error(client: TestClient):
    """Test validation: Zero menu ID should fail"""
    # Create an event first
    event_response = client.post("/api/events/", json={"name": "Test Event"})
    event_id = event_response.json()["id"]
    
    # Try to vote with zero menu ID
    response = client.post(f"/api/events/{event_id}/votes", json={"menu_id": 0})
    assert response.status_code == 422
    assert "greater than 0" in str(response.json())


def test_missing_required_fields(client: TestClient):
    """Test validation: Missing required fields should fail"""
    # Missing event name
    response = client.post("/api/events/", json={})
    assert response.status_code == 422
    
    # Create event for menu test
    event_response = client.post("/api/events/", json={"name": "Test Event"})
    event_id = event_response.json()["id"]
    
    # Missing menu name
    response = client.post(f"/api/events/{event_id}/menus", json={})
    assert response.status_code == 422
    
    # Missing menu_id for vote
    response = client.post(f"/api/events/{event_id}/votes", json={})
    assert response.status_code == 422


def test_invalid_data_types(client: TestClient):
    """Test validation: Invalid data types should fail"""
    # Create an event first
    event_response = client.post("/api/events/", json={"name": "Test Event"})
    event_id = event_response.json()["id"]
    
    # String instead of integer for menu_id
    response = client.post(f"/api/events/{event_id}/votes", json={"menu_id": "abc"})
    assert response.status_code == 422
    assert "int parsing" in str(response.json()).lower() or "invalid" in str(response.json()).lower()


def test_name_trimming_works(client: TestClient):
    """Test that names with leading/trailing spaces are trimmed"""
    # Event name with spaces should be trimmed
    response = client.post("/api/events/", json={"name": "  Test Event  "})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Event"
    
    event_id = response.json()["id"]
    
    # Menu name with spaces should be trimmed
    response = client.post(f"/api/events/{event_id}/menus", json={"name": "  Pizza  "})
    assert response.status_code == 200
    assert response.json()["name"] == "Pizza" 