from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.bevs import router as bevs_router
# filepath: /Users/christineiyer/Documents/chez-le-weekend/sql-mini-bar/main.py
from sqlalchemy import create_engine
from models.bevvy import Base
from models import database
from database import DATABASE_URL

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include routers

app.include_router(bevs_router)
# Define a root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the SQL Mini Bar API!"}
# Create the database engine
engine = create_engine(DATABASE_URL)

# Create all tables
Base.metadata.create_all(bind=engine)