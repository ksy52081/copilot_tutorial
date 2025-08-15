from typing import List
from sqlalchemy.orm import Session

from app.models.vote import Vote


def create_vote(db: Session, menu_id: int) -> Vote:
    vote = Vote(menu_id=menu_id)
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return vote


def get_votes_by_menu(db: Session, menu_id: int) -> List[Vote]:
    return db.query(Vote).filter(Vote.menu_id == menu_id).all()
