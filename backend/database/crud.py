from services.player_generator import generate_player
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import Club, League, Player, User


def create_user(db: Session, name: str, email: str):
    new_user = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refresh to get updated data
    return new_user


def get_users(db: Session):
    return db.query(User).all()


def get_all_leagues(db: Session):
    """Fetches all leagues from DB"""
    return db.query(League).all()


def get_all_clubs(db: Session):
    """Fetches all clubs from DB"""
    return db.query(Club).all()


def get_all_players(db: Session):
    """Fetches all players from DB"""
    return db.query(Player).all()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


def initialize_leagues():
    """Create tables and insert initial data if they do not exist."""
    Base.metadata.create_all(bind=engine)  # Ensure tables exist
    db = SessionLocal()
    try:
        if not db.query(League).first():  # Check if table is empty
            print("Initializing Leagues table...")
            league1 = League(name="Premier League")
            league2 = League(name="La Liga")
            db.add_all([league1, league2])
            db.commit()
            print("Inserted initial data.")
    finally:
        db.close()


def initialize_clubs():
    """Create tables and insert initial data if they do not exist."""
    Base.metadata.create_all(bind=engine)  # Create tables

    db = SessionLocal()
    # Only initalize if Club doesnt exist
    if not db.query(Club).first():
        print("Initializing Clubs table...")
        # Check if leagues exist
        if not db.query(League).first():
            premier_league = League(name="Premier League")
            la_liga = League(name="La Liga")
            db.add_all([premier_league, la_liga])
            db.commit()

        else:
            premier_league = (
                db.query(League).filter(League.name == "Premier League").first()
            )
            la_liga = db.query(League).filter(League.name == "La Liga").first()

            # Club data without emojis
            premier_league_clubs: list[str] = [
                "Arsenal",
                "Aston Villa",
                "Brentford",
                "Brighton & Hove Albion",
                "Burnley",
                "Chelsea",
                "Crystal Palace",
                "Everton",
                "Fulham",
                "Liverpool",
                "Luton Town",
                "Manchester City",
                "Manchester United",
                "Newcastle United",
                "Nottingham Forest",
                "Sheffield United",
                "Tottenham Hotspur",
                "West Ham United",
                "Wolverhampton Wanderers",
                "Bournemouth",
            ]

            la_liga_clubs: list[str] = [
                "Alavés",
                "Athletic Bilbao",
                "Atlético Madrid",
                "Barcelona",
                "Cádiz",
                "Celta Vigo",
                "Elche",
                "Espanyol",
                "Getafe",
                "Girona",
                "Granada",
                "Las Palmas",
                "Mallorca",
                "Osasuna",
                "Rayo Vallecano",
                "Real Betis",
                "Real Madrid",
                "Real Sociedad",
                "Sevilla",
                "Valencia",
            ]

            db.add_all(
                [
                    Club(name=club, league_id=premier_league.id)
                    for club in premier_league_clubs
                ]
            )
            db.add_all(
                [Club(name=club, league_id=la_liga.id) for club in la_liga_clubs]
            )

            db.commit()

    db.close()


def initialize_players():
    """Initialize Players in the DB"""
    Base.metadata.create_all(bind=engine)  # Create tables

    db = SessionLocal()
    # If player table empty, populate with random players
    if not db.query(Player).first():
        print("Initializing Players table...")
        clubs: list[Club] = db.query(Club).all()
        for club in clubs:
            for _ in range(24):
                player_name, player_age = generate_player()
                db.add(Player(name=player_name, age=player_age, club_id=club.id))
        db.commit()

    db.close()
