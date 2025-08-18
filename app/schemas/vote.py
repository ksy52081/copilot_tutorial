from pydantic import BaseModel


class VoteBase(BaseModel):
    menu_id: int


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