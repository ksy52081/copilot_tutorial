from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.models.vote import Vote
from app.models.menu import Menu
from app.schemas.vote import VoteCreate, VoteResult


class VoteRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, event_id: int, vote_data: VoteCreate) -> Vote:
        vote = Vote(event_id=event_id, menu_id=vote_data.menu_id)
        self.db.add(vote)
        self.db.commit()
        self.db.refresh(vote)
        return vote
    
    def get_by_event_id(self, event_id: int) -> List[Vote]:
        return self.db.query(Vote).filter(Vote.event_id == event_id).all()
    
    def get_vote_results(self, event_id: int) -> List[VoteResult]:
        results = (
            self.db.query(
                Menu.id.label('menu_id'),
                Menu.name.label('menu_name'),
                func.count(Vote.id).label('vote_count')
            )
            .outerjoin(Vote, (Vote.menu_id == Menu.id) & (Vote.event_id == event_id))
            .filter(Menu.event_id == event_id)
            .group_by(Menu.id, Menu.name)
            .all()
        )
        
        return [
            VoteResult(
                menu_id=result.menu_id,
                menu_name=result.menu_name,
                vote_count=result.vote_count
            )
            for result in results
        ]
    
    def delete(self, vote_id: int) -> bool:
        vote = self.db.query(Vote).filter(Vote.id == vote_id).first()
        if vote:
            self.db.delete(vote)
            self.db.commit()
            return True
        return False 