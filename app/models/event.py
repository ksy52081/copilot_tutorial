from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
