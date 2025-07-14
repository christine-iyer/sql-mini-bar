from sqlalchemy import Column, String, Integer, JSON
from models.database import Base

class Bevvy(Base):
    __tablename__ = "bevs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    ingredients = Column(JSON, nullable=True)  # JSON column for ingredients
    picture = Column(String(255), nullable=True)  # URL for the picture