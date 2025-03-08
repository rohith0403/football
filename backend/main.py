from contextlib import asynccontextmanager
from fastapi import FastAPI
from database.database import engine, Base
from database.crud import initialize_leagues

# Lifecycle event to initialize database
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs on startup"""
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)  # Creates tables if they don't exist
    initialize_leagues()
    yield  # Hand over control to the app
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "FastAPI is running"}
