from pydantic import BaseModel, Field, field_validator


class MenuBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Menu name")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Menu name cannot be empty or only whitespace')
        return v.strip()


class MenuCreate(MenuBase):
    pass


class MenuResponse(MenuBase):
    id: int
    event_id: int
    
    class Config:
        from_attributes = True 