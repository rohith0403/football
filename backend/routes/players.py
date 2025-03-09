from typing import Any

import database.crud as crud
from database.database import SessionLocal
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

player_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@player_router.get("/get_all_players")
async def get_all_clubs(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    """Returns all leagues"""
    players = crud.get_all_players(db)
    return [
        {
            "id": player.id,
            "name": player.name,
            "age": player.age,
            "club": player.club.name,
        }
        for player in players
    ]
