from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.menu import Menu


def create_menu(db: Session, event_id: int, name: str) -> Menu:
    menu = Menu(event_id=event_id, name=name)
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


def get_menu_by_id(db: Session, menu_id: int) -> Optional[Menu]:
    return db.query(Menu).filter(Menu.menu_id == menu_id).first()


def get_menus_by_event(db: Session, event_id: int) -> List[Menu]:
    return db.query(Menu).filter(Menu.event_id == event_id).all()
