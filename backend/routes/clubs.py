from typing import Any

import database.crud as crud
from database.database import SessionLocal
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

club_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@club_router.get("/get_all_clubs")
async def get_all_clubs(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    """Returns all leagues"""
    clubs = crud.get_all_clubs(db)
    return [
        {
            "id": club.id,
            "name": club.name,
            "league": club.league.name,  # Access League name
        }
        for club in clubs
    ]
