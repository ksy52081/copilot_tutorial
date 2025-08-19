from pydantic import BaseModel, Field


class VoteBase(BaseModel):
    menu_id: int = Field(..., gt=0, description="Menu ID must be positive")


class VoteCreate(VoteBase):
    pass


class VoteResponse(VoteBase):
    id: int
    event_id: int
    
    class Config:
        from_attributes = True


class VoteResult(BaseModel):
    menu_id: int
    menu_name: str
    vote_count: int 