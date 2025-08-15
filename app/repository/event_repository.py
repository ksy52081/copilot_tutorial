from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.event import Event
from app.models.menu import Menu
from app.models.vote import Vote


def create_event(db: Session, name: str) -> Event:
    event = Event(name=name)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_all_events(db: Session, skip: int = 0, limit: int = 100) -> List[Event]:
    return db.query(Event).offset(skip).limit(limit).all()


def get_event_by_id(db: Session, event_id: int) -> Optional[Event]:
    return db.query(Event).filter(Event.event_id == event_id).first()


def get_event_with_menus(db: Session, event_id: int) -> Optional[Event]:
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if event:
        # Get vote counts for each menu
        menus = db.query(Menu, func.count(Vote.vote_id).label('vote_count'))\
            .outerjoin(Vote)\
            .filter(Menu.event_id == event_id)\
            .group_by(Menu.menu_id)\
            .all()
        
        # Update menu objects with vote counts
        event.menus = [menu for menu, _ in menus]
        for menu, vote_count in menus:
            setattr(menu, 'vote_count', vote_count)
    
    return event
