from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repository import event_repository
from app.repository import menu_repository
from app.schemas.event import EventCreate, EventRead, EventDetailRead, MenuRead


def create_event_service(db: Session, event_create: EventCreate) -> EventRead:
    event = event_repository.create_event(db, event_create.name)
    return EventRead.model_validate(event)


def get_all_events_service(db: Session, skip: int = 0, limit: int = 100) -> List[EventRead]:
    events = event_repository.get_all_events(db, skip, limit)
    return [EventRead.model_validate(event) for event in events]


def get_event_detail_service(db: Session, event_id: int) -> EventDetailRead:
    event = event_repository.get_event_with_menus(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventDetailRead.model_validate(event)


def add_menu_to_event_service(db: Session, event_id: int, menu_name: str) -> MenuRead:
    event = event_repository.get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    menu = menu_repository.create_menu(db, event_id, menu_name)
    return MenuRead.model_validate(menu)
