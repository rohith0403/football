from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, Base
from database.crud import initialize_leagues
from routes.leagues import apirouter

# Define allowed origins
origins = [
    "http://localhost:3000",  # Allow frontend running on localhost
]



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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(apirouter, tags=["Leagues"])

@app.get("/")
async def root():
    return {"message": "FastAPI is running"}

