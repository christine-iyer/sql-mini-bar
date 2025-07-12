from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.bevvy import Bevvy
from schemas.bevs import BevvyCreate, BevvyResponse, BevvyUpdate
from models.database import get_db
from typing import List
import logging
import json

# Initialize the router
router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)

# POST endpoint to create a new bevvy
@router.post("/bevs/", response_model=BevvyResponse)
async def create_bevvy(bevvy: BevvyCreate, db: Session = Depends(get_db)):
    logging.info(f"Received bevvy data: {bevvy}")
    
    # Check if the bevvy already exists
    db_bevvy = db.query(Bevvy).filter(Bevvy.name == bevvy.name).first()
    if db_bevvy:
        raise HTTPException(status_code=400, detail="Bevvy already exists")
    
    # Create a new bevvy record
    new_bevvy = Bevvy(
        name=bevvy.name,
        ingredients=bevvy.ingredients,  # Directly assign the list
        picture=bevvy.picture,
    )
    db.add(new_bevvy)
    db.commit()
    db.refresh(new_bevvy)
    
    return new_bevvy
# GET endpoint to retrieve all bevs
@router.get("/bevs/", response_model=List[BevvyResponse])
async def get_bevs(db: Session = Depends(get_db)):
    bevs = db.query(Bevvy).all()
    for bevvy in bevs:
        if isinstance(bevvy.ingredients, str):  # If ingredients is a JSON string
            try:
                bevvy.ingredients = json.loads(bevvy.ingredients)  # Deserialize JSON string
            except json.JSONDecodeError:
                bevvy.ingredients = []  # Default to an empty list if deserialization fails
    return bevs

# GET endpoint to retrieve a single bevvy by ID
@router.get("/bevs/{bevvy_id}", response_model=BevvyResponse)
async def get_bevvy(bevvy_id: int, db: Session = Depends(get_db)):
    bevvy = db.query(Bevvy).filter(Bevvy.id == bevvy_id).first()
    if not bevvy:
        raise HTTPException(status_code=404, detail="Bevvy not found")
    
    # Deserialize ingredients for the response
    if isinstance(bevvy.ingredients, str):  # If ingredients is a JSON string
        try:
            bevvy.ingredients = json.loads(bevvy.ingredients)
        except json.JSONDecodeError:
            bevvy.ingredients = []  # Default to an empty list if deserialization fails
    return bevvy

# PUT endpoint to update a bevvy by ID
@router.put("/bevs/{bevvy_id}", response_model=BevvyResponse)
async def update_bevvy(bevvy_id: int, updated_data: BevvyUpdate, db: Session = Depends(get_db)):
    # Query the bevvy by ID
    bevvy = db.query(Bevvy).filter(Bevvy.id == bevvy_id).first()
    
    # If the bevvy does not exist, raise a 404 error
    if not bevvy:
        raise HTTPException(status_code=404, detail="Bevvy not found")
    
    # Update the fields provided in the request body
    for key, value in updated_data.dict(exclude_unset=True).items():  # Use .dict() to convert to a dictionary
        if key == "ingredients" and isinstance(value, list):  # Serialize ingredients if it's a list
            value = json.dumps(value)
        if hasattr(bevvy, key):  # Check if the field exists in the model
            setattr(bevvy, key, value)
    
    # Commit the changes to the database
    db.commit()
    db.refresh(bevvy)
    
    # Deserialize ingredients for the response
    if isinstance(bevvy.ingredients, str):  # If ingredients is a JSON string
        try:
            bevvy.ingredients = json.loads(bevvy.ingredients)
        except json.JSONDecodeError:
            bevvy.ingredients = []  # Default to an empty list if deserialization fails
    return bevvy
# DELETE endpoint to delete a bevvy by ID
@router.delete("/bevs/{bevvy_id}")
async def delete_bevvy(bevvy_id: int, db: Session = Depends(get_db)):
    # Query the bevvy by ID
    db_bevvy = db.query(Bevvy).filter(Bevvy.id == bevvy_id).first()
    
    # If the bevvy does not exist, raise a 404 error
    if not db_bevvy:
        raise HTTPException(status_code=404, detail="Bevvy not found")
    
    # Delete the bevvy from the database
    db.delete(db_bevvy)
    db.commit()
    
    return {"message": "Bevvy deleted successfully"}