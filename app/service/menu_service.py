from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repository import menu_repository, vote_repository
from app.schemas.event import MenuRead, VoteRead


def create_menu_service(db: Session, menu_name: str, event_id: int) -> MenuRead:
    menu = menu_repository.create_menu(db, event_id, menu_name)
    return MenuRead.model_validate(menu)


def get_menus_by_event_service(db: Session, event_id: int) -> List[MenuRead]:
    menus = menu_repository.get_menus_by_event(db, event_id)
    return [MenuRead.model_validate(menu) for menu in menus]


def vote_for_menu_service(db: Session, menu_id: int) -> VoteRead:
    menu = menu_repository.get_menu_by_id(db, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    vote = vote_repository.create_vote(db, menu_id)
    return VoteRead.model_validate(vote)
