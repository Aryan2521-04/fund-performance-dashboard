from fastapi import FastAPI
from .database import Base, engine
from .routers import funds
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(CORSMiddleware, 
                   allow_origins=origins,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(funds.router)