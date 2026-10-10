
import os
from pathlib import Path 

# points DATABASE_URL to a temporary SQLite database, so tests don't affect the real database

TEST_DATABASE_URL = f"sqlite:///{Path(__file__).resolve().parent}/test.db"

os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from app.database import Base, engine
from app.main import app
from app.seed_data import seed_database
from fastapi.testclient import TestClient
import pytest

@pytest.fixture()
def client():

    seed_database()  # Seed the test database with sample data

    with TestClient(app) as c:
        yield c

    # tear down test database
    Base.metadata.drop_all(bind=engine)
