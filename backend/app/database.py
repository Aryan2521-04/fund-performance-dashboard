from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Generator

# Database connection
engine = create_engine("sqlite:///./database.db", echo=True, connect_args={"check_same_thread": False})

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
