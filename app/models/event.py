from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Event(BaseModel):
    __tablename__ = "events"
    
    name = Column(String, nullable=False)
    
    # Relationships
    menus = relationship("Menu", back_populates="event", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="event", cascade="all, delete-orphan") 