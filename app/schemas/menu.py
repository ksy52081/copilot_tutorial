from pydantic import BaseModel


class MenuBase(BaseModel):
    name: str


class MenuCreate(MenuBase):
    pass


class MenuResponse(MenuBase):
    id: int
    event_id: int
    
    class Config:
        from_attributes = True 