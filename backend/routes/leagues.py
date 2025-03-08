from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import SessionLocal
import database.crud as crud

league_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@league_router.get('/get_all_leagues')
async def get_all_leagues(db: Session = Depends(get_db)):
    """Returns all leagues"""
    return crud.get_all_leagues(db)