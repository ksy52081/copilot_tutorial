from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.event import EventCreate, EventRead
from app.service.event_service import create_event_service, get_all_events_service

from typing import List


# DB 세션 의존성 (예시)
def get_db():
    from app.models.event import Base
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(
        "sqlite:///./test.db", connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(prefix="/api/events", tags=["events"])


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    created = create_event_service(db, event)
    return EventRead.from_orm(created)


@router.get("", response_model=List[EventRead])
def list_events(db: Session = Depends(get_db)):
    events = get_all_events_service(db)
    return [EventRead.from_orm(e) for e in events]
