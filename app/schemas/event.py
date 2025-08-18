from pydantic import BaseModel
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.menu import MenuResponse


class EventBase(BaseModel):
    name: str


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: int
    
    class Config:
        from_attributes = True


class EventWithMenus(EventResponse):
    menus: List["MenuResponse"] = [] 