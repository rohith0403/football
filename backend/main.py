from contextlib import asynccontextmanager

from database.crud import initialize_clubs, initialize_leagues, initialize_players
from database.database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.clubs import club_router
from routes.leagues import league_router
from routes.players import player_router

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
    initialize_clubs()
    initialize_players()
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

app.include_router(league_router, tags=["Leagues"])
app.include_router(club_router, tags=["Clubs"])
app.include_router(player_router, tags=["Players"])


@app.get("/")
async def root():
    return {"message": "FastAPI is running"}
