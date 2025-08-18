from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Vote(BaseModel):
    __tablename__ = "votes"
    
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    
    # Relationships
    event = relationship("Event", back_populates="votes")
    menu = relationship("Menu", back_populates="votes") 