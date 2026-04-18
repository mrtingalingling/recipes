from sqlalchemy import Column, Integer, String, Text, DateTime
from .db import Base
import datetime

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    ingredients = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
