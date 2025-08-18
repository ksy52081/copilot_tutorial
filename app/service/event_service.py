from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.repository.event_repository import EventRepository
from app.schemas.event import EventCreate, EventResponse


class EventService:
    def __init__(self, db: Session):
        self.repository = EventRepository(db)
    
    def create_event(self, event_data: EventCreate) -> EventResponse:
        event = self.repository.create(event_data)
        return EventResponse.model_validate(event)
    
    def get_all_events(self) -> List[EventResponse]:
        events = self.repository.get_all()
        return [EventResponse.model_validate(event) for event in events]
    
    def get_event_by_id(self, event_id: int) -> EventResponse:
        event = self.repository.get_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return EventResponse.model_validate(event)
    
    def delete_event(self, event_id: int) -> bool:
        success = self.repository.delete(event_id)
        if not success:
            raise HTTPException(status_code=404, detail="Event not found")
        return success 