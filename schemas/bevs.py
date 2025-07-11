from pydantic import BaseModel
from typing import List, Optional

class BevvyCreate(BaseModel):
    name: str   
    ingredients: Optional[List[str]] = None  # Expecting a list of strings
    picture: Optional[str] = None   

class BevvyResponse(BaseModel):
    id: int
    name: str
    ingredients: Optional[List[str]]  # JSON array
    picture: Optional[str]  

class BevvyUpdate(BaseModel):
    name: Optional[str] = None
    ingredients: Optional[List[str]] = None  # Use List[str] for consistency
    picture: Optional[str] = None

    class Config:
        from_attributes = True