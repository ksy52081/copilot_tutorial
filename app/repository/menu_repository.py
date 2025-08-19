from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.menu import Menu
from app.schemas.menu import MenuCreate


class MenuRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, event_id: int, menu_data: MenuCreate) -> Menu:
        menu = Menu(event_id=event_id, name=menu_data.name)
        self.db.add(menu)
        self.db.commit()
        self.db.refresh(menu)
        return menu
    
    def get_by_event_id(self, event_id: int) -> List[Menu]:
        return self.db.query(Menu).filter(Menu.event_id == event_id).all()
    
    def get_by_id(self, menu_id: int) -> Optional[Menu]:
        return self.db.query(Menu).filter(Menu.id == menu_id).first()
    
    def get_by_name_and_event(self, event_id: int, menu_name: str) -> Optional[Menu]:
        return self.db.query(Menu).filter(
            Menu.event_id == event_id, 
            Menu.name == menu_name
        ).first()
    
    def delete(self, menu_id: int) -> bool:
        menu = self.get_by_id(menu_id)
        if menu:
            self.db.delete(menu)
            self.db.commit()
            return True
        return False 