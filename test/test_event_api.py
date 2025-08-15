from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_event():
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


def test_list_events():
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
    assert len(body) >= 2
    assert any(e["name"] == "2025년 7월 회식" for e in body)
    assert any(e["name"] == "2025년 8월 회식" for e in body)
