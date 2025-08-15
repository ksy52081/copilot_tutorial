from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models to register them with Base
from .event import Event
from .menu import Menu
from .vote import Vote
