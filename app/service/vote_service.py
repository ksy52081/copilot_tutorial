from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.repository.vote_repository import VoteRepository
from app.repository.event_repository import EventRepository
from app.repository.menu_repository import MenuRepository
from app.schemas.vote import VoteCreate, VoteResponse, VoteResult


class VoteService:
    def __init__(self, db: Session):
        self.vote_repository = VoteRepository(db)
        self.event_repository = EventRepository(db)
        self.menu_repository = MenuRepository(db)
    
    def create_vote(self, event_id: int, vote_data: VoteCreate) -> VoteResponse:
        # Check if event exists
        event = self.event_repository.get_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Check if menu exists
        menu = self.menu_repository.get_by_id(vote_data.menu_id)
        if not menu:
            raise HTTPException(status_code=404, detail=f"Menu with id {vote_data.menu_id} not found")
        
        # Check if menu belongs to the event
        if menu.event_id != event_id:
            raise HTTPException(status_code=400, detail="Menu does not belong to this event")
        
        vote = self.vote_repository.create(event_id, vote_data)
        return VoteResponse.model_validate(vote)
    
    def get_vote_results(self, event_id: int) -> List[VoteResult]:
        # Check if event exists
        event = self.event_repository.get_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return self.vote_repository.get_vote_results(event_id) 