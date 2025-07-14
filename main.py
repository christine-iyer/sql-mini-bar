# filepath: /Users/christineiyer/Documents/chez-le-weekend/sql-mini-bar/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.bevs import router as bevs_router
import models.bevvy  # Ensure models are imported
import models.database 
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

# Define a root routeclear

@app.get("/")
def read_root():
    return {"message": "Welcome to the SQL Mini Bar API!"}