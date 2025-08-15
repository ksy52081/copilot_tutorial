from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.event import (
    EventCreate, EventRead, EventDetailRead,
    MenuCreate, MenuRead, VoteCreate, VoteRead
)
from app.service.event_service import (
    create_event_service,
    get_all_events_service,
    get_event_detail_service,
    add_menu_to_event_service
)
from app.service.menu_service import vote_for_menu_service


router = APIRouter(prefix="/api/events", tags=["events"])


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """Create a new event"""
    return create_event_service(db, event)


@router.get("", response_model=List[EventRead])
def list_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of all events"""
    return get_all_events_service(db, skip, limit)


@router.get("/{event_id}", response_model=EventDetailRead)
def get_event_detail(event_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific event including its menus"""
    return get_event_detail_service(db, event_id)


@router.post("/{event_id}/menus", response_model=MenuRead, status_code=status.HTTP_201_CREATED)
def add_menu_to_event(
    event_id: int,
    menu: MenuCreate,
    db: Session = Depends(get_db)
):
    """Add a new menu to an event"""
    return add_menu_to_event_service(db, event_id, menu.name)


@router.post("/menus/{menu_id}/vote", response_model=VoteRead, status_code=status.HTTP_201_CREATED)
def vote_for_menu(
    menu_id: int,
    db: Session = Depends(get_db)
):
    """Vote for a specific menu"""
    return vote_for_menu_service(db, menu_id)
