import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.service.event_service import create_event_service, get_all_events_service
from app.schemas.event import EventCreate
from app.models.event import Event


@pytest.fixture
def db():
    """
    MagicMock을 사용한 가짜 DB 세션을 반환한다.
    """
    return MagicMock(spec=Session)


def test_create_event_service_calls_repository(monkeypatch, db):
    """
    create_event_service는 event_repository.create_event를 호출하고 Event 객체를 반환해야 한다.
    """
    # Given
    event_create = EventCreate(name="2025년 7월 회식")
    fake_event = Event(id=1, name="2025년 7월 회식")
    called = {}

    def fake_create_event(db_arg, name_arg):
        called["db"] = db_arg
        called["name"] = name_arg
        return fake_event

    monkeypatch.setattr("app.service.event_service.create_event", fake_create_event)

    # When
    result = create_event_service(db, event_create)

    # Then
    assert result == fake_event
    assert called["db"] == db
    assert called["name"] == "2025년 7월 회식"


def test_get_all_events_service_calls_repository(monkeypatch, db):
    """
    get_all_events_service는 event_repository.get_all_events를 호출하고 Event 리스트를 반환해야 한다.
    """
    # Given
    fake_events = [
        Event(id=1, name="2025년 7월 회식"),
        Event(id=2, name="2025년 8월 회식"),
    ]
    called = {}

    def fake_get_all_events(db_arg):
        called["db"] = db_arg
        return fake_events

    monkeypatch.setattr("app.service.event_service.get_all_events", fake_get_all_events)

    # When
    result = get_all_events_service(db)

    # Then
    assert result == fake_events
    assert called["db"] == db
