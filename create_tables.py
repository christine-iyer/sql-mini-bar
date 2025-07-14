# filepath: /Users/christineiyer/Documents/chez-le-weekend/sql-mini-bar/create_tables.py
from models.database import Base, engine
from models.bevvy import Bevvy  # Ensure the model is imported

# Create all tables
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")