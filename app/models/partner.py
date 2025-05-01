from sqlalchemy import Column, Integer, String 
from ..database.db import Base


class Partner(Base):
    __tablename__ = 'partners'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    social_media = Column(String, nullable=False)
    
    