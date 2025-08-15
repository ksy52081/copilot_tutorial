from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class EventBase(BaseModel):
    name: str


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    event_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MenuBase(BaseModel):
    name: str


class MenuCreate(MenuBase):
    pass


class MenuRead(MenuBase):
    menu_id: int
    event_id: int
    created_at: datetime
    vote_count: Optional[int] = None

    class Config:
        from_attributes = True


class VoteCreate(BaseModel):
    menu_id: int


class VoteRead(BaseModel):
    vote_id: int
    menu_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class EventDetailRead(EventRead):
    menus: List[MenuRead] = []
