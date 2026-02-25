from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

"""
This file configures SQLite,
 creates a connection engine, defines a session factory, 
registers your models, 
and provides a safe way for FastAPI to use and close database sessions per request.
"""
# Project root = parent of the "app" folder
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "course_tracker.db"

# Use sqlite and store db @ db_path
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Manage connections and allow multiple threads
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# temp space for DB comms
# prevent auto saves with autocmmit = F and don't send partial changes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass

# FASTAPI request in -> creates session-> Route runs w/ db -> CRUD queries -> send response -> db.close closes

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()