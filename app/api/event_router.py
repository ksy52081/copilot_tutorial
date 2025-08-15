from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.event import EventCreate, EventRead
from app.service.event_service import create_event_service, get_all_events_service

from typing import List


# DB 세션 의존성 함수는 app/db.py에 분리되어 있습니다.
from app.db import get_db
router = APIRouter(prefix="/api/events", tags=["events"])


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    created = create_event_service(db, event)
    return EventRead.from_orm(created)


@router.get("", response_model=List[EventRead])
def list_events(db: Session = Depends(get_db)):
    events = get_all_events_service(db)
    return [EventRead.from_orm(e) for e in events]
