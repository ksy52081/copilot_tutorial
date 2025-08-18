from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.event import Event
from app.schemas.event import EventCreate


class EventRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, event_data: EventCreate) -> Event:
        event = Event(name=event_data.name)
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event
    
    def get_all(self) -> List[Event]:
        return self.db.query(Event).all()
    
    def get_by_id(self, event_id: int) -> Optional[Event]:
        return self.db.query(Event).filter(Event.id == event_id).first()
    
    def delete(self, event_id: int) -> bool:
        event = self.get_by_id(event_id)
        if event:
            self.db.delete(event)
            self.db.commit()
            return True
        return False 