from sqlalchemy.orm import Session
from app.repository.event_repository import create_event, get_all_events
from app.schemas.event import EventCreate
from app.models.event import Event


def create_event_service(db: Session, event_create: EventCreate) -> Event:
    return create_event(db, event_create.name)


def get_all_events_service(db: Session) -> list[Event]:
    return get_all_events(db)
