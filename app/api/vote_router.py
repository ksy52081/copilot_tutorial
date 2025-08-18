from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.service.vote_service import VoteService
from app.schemas.vote import VoteCreate, VoteResponse, VoteResult

router = APIRouter(prefix="/api/events", tags=["votes"])


@router.post("/{event_id}/votes", response_model=VoteResponse)
def create_vote(
    event_id: int,
    vote_data: VoteCreate,
    db: Session = Depends(get_db)
):
    service = VoteService(db)
    return service.create_vote(event_id, vote_data)


@router.get("/{event_id}/results", response_model=List[VoteResult])
def get_vote_results(
    event_id: int,
    db: Session = Depends(get_db)
):
    service = VoteService(db)
    return service.get_vote_results(event_id) 