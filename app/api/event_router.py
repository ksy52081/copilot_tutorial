from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.service.event_service import EventService
from app.schemas.event import EventCreate, EventResponse

router = APIRouter(prefix="/api/events", tags=["events"])


@router.post("/", response_model=EventResponse)
def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db)
):
    service = EventService(db)
    return service.create_event(event_data)


@router.get("/", response_model=List[EventResponse])
def get_all_events(db: Session = Depends(get_db)):
    service = EventService(db)
    return service.get_all_events()
