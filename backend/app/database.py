from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Generator
from pathlib import Path
import os

# default used when DATABASE_URL is not set
DEFAULT_DATABASE_URL = f"sqlite:///{Path(__file__).resolve().parent.parent}/database.db"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

# Database connection
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

# Create a base class for declarative models
Base = declarative_base()

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

# Dependency to get a database session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


