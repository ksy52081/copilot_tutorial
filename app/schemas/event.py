from pydantic import BaseModel, Field, field_validator
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.menu import MenuResponse


class EventBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Event name")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Event name cannot be empty or only whitespace')
        return v.strip()


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: int
    
    class Config:
        from_attributes = True


class EventWithMenus(EventResponse):
    menus: List["MenuResponse"] = [] 