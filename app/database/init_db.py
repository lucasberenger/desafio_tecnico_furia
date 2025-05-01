from ..models import partner
from .db import engine, Base

def init_db():
    """Create the database tables."""
    Base.metadata.create_all(bind=engine)