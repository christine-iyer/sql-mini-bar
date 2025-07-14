from sqlalchemy import Column, String, Integer, JSON 
from models.database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bevvy(Base):
    __tablename__ = "bevs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    ingredients = Column(JSON(255), nullable=True)  # Comma-separated
    picture = Column(String(255), nullable=True)  # Comma-separated