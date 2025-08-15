from pydantic import BaseModel


class EventCreate(BaseModel):
    name: str


class EventRead(BaseModel):
    event_id: int
    name: str

    class Config:
        orm_mode = True
