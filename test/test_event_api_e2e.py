from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_event_and_list():
    """
    이벤트를 생성한 후 전체 목록에서 해당 이벤트가 조회되어야 한다.
    """
    # Given: 새로운 이벤트 생성
    data = {"name": "2025년 9월 회식"}
    resp = client.post("/api/events", json=data)
    assert resp.status_code == 201
    created = resp.json()
    # When: 전체 이벤트 목록 조회
    resp2 = client.get("/api/events")
    assert resp2.status_code == 200
    # Then: 생성한 이벤트가 목록에 포함되어야 한다
    assert any(
        e["event_id"] == created["event_id"] and e["name"] == data["name"]
        for e in resp2.json()
    )


def test_create_multiple_events_and_list_order():
    """
    여러 이벤트를 생성하면, 목록 조회 시 모두 반환되어야 한다.
    """
    # Given: 이벤트 2개 생성
    client.post("/api/events", json={"name": "2025년 10월 회식"})
    client.post("/api/events", json={"name": "2025년 11월 회식"})
    # When: 전체 이벤트 목록 조회
    resp = client.get("/api/events")
    assert resp.status_code == 200
    names = [e["name"] for e in resp.json()]
    # Then: 두 이벤트 이름이 모두 포함되어야 한다
    assert "2025년 10월 회식" in names
    assert "2025년 11월 회식" in names


def test_create_event_with_empty_name():
    """
    이벤트 이름이 비어있으면 422 Unprocessable Entity가 반환되어야 한다.
    """
    # Given: 빈 이름으로 이벤트 생성
    resp = client.post("/api/events", json={"name": ""})
    # Then: 422 반환
    assert resp.status_code == 422
