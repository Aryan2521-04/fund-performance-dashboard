from fastapi import FastAPI
from .database import Base, engine
from .routers import funds


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(funds.router)