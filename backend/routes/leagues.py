import database.crud as crud
from database.database import SessionLocal
from fastapi import APIRouter, Depends
from services.season_generator import generate_fixtures
from sqlalchemy.orm import Session

league_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@league_router.get("/get_all_leagues")
async def get_all_leagues(db: Session = Depends(get_db)):
    """Returns all leagues"""
    return crud.get_all_leagues(db)


@league_router.get("/fixtures/{league_id}")
async def get_fixtures(league_id, db: Session = Depends(get_db)):
    """Returns fixtures for a league"""
    return generate_fixtures(db, league_id)
