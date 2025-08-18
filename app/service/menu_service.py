from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.repository.menu_repository import MenuRepository
from app.repository.event_repository import EventRepository
from app.schemas.menu import MenuCreate, MenuResponse


class MenuService:
    def __init__(self, db: Session):
        self.menu_repository = MenuRepository(db)
        self.event_repository = EventRepository(db)
    
    def create_menu(self, event_id: int, menu_data: MenuCreate) -> MenuResponse:
        # Check if event exists
        event = self.event_repository.get_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        menu = self.menu_repository.create(event_id, menu_data)
        return MenuResponse.model_validate(menu)
    
    def get_menus_by_event(self, event_id: int) -> List[MenuResponse]:
        # Check if event exists
        event = self.event_repository.get_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        menus = self.menu_repository.get_by_event_id(event_id)
        return [MenuResponse.model_validate(menu) for menu in menus] 