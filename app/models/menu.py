from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Menu(BaseModel):
    __tablename__ = "menus"
    
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    name = Column(String, nullable=False)
    
    # Relationships
    event = relationship("Event", back_populates="menus")
    votes = relationship("Vote", back_populates="menu", cascade="all, delete-orphan") 