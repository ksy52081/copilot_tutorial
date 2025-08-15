from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_event(client: TestClient, test_db: Session):
    """
    새로운 회식 이벤트를 생성하면 201과 이벤트 정보가 반환된다.
    """
    # Given: 생성할 이벤트 이름
    data = {"name": "2025년 7월 회식"}
    
    # When: POST /api/events 요청
    response = client.post("/api/events", json=data)
    
    # Then: 201, event_id와 name 반환
    assert response.status_code == 201
    body = response.json()
    assert body["event_id"] > 0
    assert body["name"] == data["name"]
    assert "created_at" in body


def test_list_events(client: TestClient, test_db: Session):
    """
    이벤트가 존재할 때 전체 목록을 조회하면 200과 리스트가 반환된다.
    """
    # Given: 이벤트 2개 생성
    client.post("/api/events", json={"name": "2025년 7월 회식"})
    client.post("/api/events", json={"name": "2025년 8월 회식"})
    
    # When: GET /api/events 요청
    response = client.get("/api/events")
    
    # Then: 200, 2개 이벤트 포함
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 2
    assert body[0]["name"] == "2025년 7월 회식"
    assert body[1]["name"] == "2025년 8월 회식"


def test_get_event_detail(client: TestClient, test_db: Session):
    """
    이벤트 상세 정보를 조회하면 메뉴 목록과 투표 현황이 함께 반환된다.
    """
    # Given: 이벤트와 메뉴 생성
    event_response = client.post("/api/events", json={"name": "회식"})
    event_id = event_response.json()["event_id"]
    client.post(f"/api/events/{event_id}/menus", json={"name": "삼겹살"})
    client.post(f"/api/events/{event_id}/menus", json={"name": "치킨"})
    
    # When: GET /api/events/{event_id} 요청
    response = client.get(f"/api/events/{event_id}")
    
    # Then: 200, 이벤트 정보와 메뉴 목록 반환
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "회식"
    assert len(data["menus"]) == 2
    assert data["menus"][0]["name"] == "삼겹살"
    assert data["menus"][1]["name"] == "치킨"


def test_add_menu_to_event(client: TestClient, test_db: Session):
    """
    이벤트에 새 메뉴를 추가하면 201과 메뉴 정보가 반환된다.
    """
    # Given: 이벤트 생성
    event_response = client.post("/api/events", json={"name": "회식"})
    event_id = event_response.json()["event_id"]
    
    # When: POST /api/events/{event_id}/menus 요청
    response = client.post(
        f"/api/events/{event_id}/menus",
        json={"name": "삼겹살"}
    )
    
    # Then: 201, 메뉴 정보 반환
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "삼겹살"
    assert data["event_id"] == event_id
    assert "menu_id" in data
    assert "created_at" in data


def test_vote_for_menu(client: TestClient, test_db: Session):
    """
    메뉴에 투표하면 201과 투표 정보가 반환되고, 투표수가 증가한다.
    """
    # Given: 이벤트와 메뉴 생성
    event_response = client.post("/api/events", json={"name": "회식"})
    event_id = event_response.json()["event_id"]
    menu_response = client.post(
        f"/api/events/{event_id}/menus",
        json={"name": "삼겹살"}
    )
    menu_id = menu_response.json()["menu_id"]
    
    # When: POST /api/events/menus/{menu_id}/vote 요청
    response = client.post(f"/api/events/menus/{menu_id}/vote")
    
    # Then: 201, 투표 정보 반환
    assert response.status_code == 201
    data = response.json()
    assert data["menu_id"] == menu_id
    assert "vote_id" in data
    assert "created_at" in data
    
    # And: 투표수 증가 확인
    event_response = client.get(f"/api/events/{event_id}")
    assert event_response.json()["menus"][0]["vote_count"] == 1


def test_get_nonexistent_event(client: TestClient, test_db: Session):
    """
    존재하지 않는 이벤트를 조회하면 404가 반환된다.
    """
    response = client.get("/api/events/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"
