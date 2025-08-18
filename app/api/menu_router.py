from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.service.menu_service import MenuService
from app.schemas.menu import MenuCreate, MenuResponse

router = APIRouter(prefix="/api/events", tags=["menus"])


@router.post("/{event_id}/menus", response_model=MenuResponse)
def create_menu(
    event_id: int,
    menu_data: MenuCreate,
    db: Session = Depends(get_db)
):
    service = MenuService(db)
    return service.create_menu(event_id, menu_data)


@router.get("/{event_id}/menus", response_model=List[MenuResponse])
def get_menus(
    event_id: int,
    db: Session = Depends(get_db)
):
    service = MenuService(db)
    return service.get_menus_by_event(event_id) 