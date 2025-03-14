from services.player_generator import generate_player
from sqlalchemy import desc
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import Club, Fixtures, League, LeagueTable, Player, Season, User


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


def get_all_clubs_with_league_id(db: Session, league_id: int):
    """Fetches all clubs from DB with league id: league_id"""
    return db.query(Club).filter(Club.league_id == league_id).all()


def get_all_players(db: Session):
    """Fetches all players from DB"""
    return db.query(Player).all()


def add_fixture(
    db: Session,
    gameweek: int,
    home_club_id: int,
    away_club_id: int,
    league_id: int,
    # league_table_id: int,
):
    """Add a single Fixture to the Fixtures table"""
    db = SessionLocal()
    db.add(
        Fixtures(
            gameweek=gameweek,
            home_club_id=home_club_id,
            away_club_id=away_club_id,
            league_id=league_id,
            # league_table_id=league_table_id,
            home_club_goals=0,
            away_club_goals=0,
            played_status=False,
        )
    )
    db.commit()
    db.close()


def initialize_leagues():
    """Create tables and insert initial data if they do not exist."""
    Base.metadata.create_all(bind=engine)  # Ensure tables exist
    db = SessionLocal()
    try:
        if not db.query(League).first():  # Check if table is empty
            print("Initializing Leagues table...")
            league1 = League(name="Premier League")
            # league2 = League(name="La Liga")
            # db.add_all([league1, league2])
            db.add(league1)
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
            # la_liga = League(name="La Liga")
            # db.add_all([premier_league, la_liga])
            db.add(premier_league)
            db.commit()

        else:
            premier_league = (
                db.query(League).filter(League.name == "Premier League").first()
            )
            # la_liga = db.query(League).filter(League.name == "La Liga").first()

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

            # la_liga_clubs: list[str] = [
            #     "Alavés",
            #     "Athletic Bilbao",
            #     "Atlético Madrid",
            #     "Barcelona",
            #     "Cádiz",
            #     "Celta Vigo",
            #     "Elche",
            #     "Espanyol",
            #     "Getafe",
            #     "Girona",
            #     "Granada",
            #     "Las Palmas",
            #     "Mallorca",
            #     "Osasuna",
            #     "Rayo Vallecano",
            #     "Real Betis",
            #     "Real Madrid",
            #     "Real Sociedad",
            #     "Sevilla",
            #     "Valencia",
            # ]

            db.add_all(
                [
                    Club(name=club, league_id=premier_league.id)
                    for club in premier_league_clubs
                ]
            )
            # db.add_all(
            #     [Club(name=club, league_id=la_liga.id) for club in la_liga_clubs]
            # )

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


def initialize_seasons():
    """Initialize Seasons in the DB"""
    Base.metadata.create_all(bind=engine)  # Create tables

    db = SessionLocal()
    # If Season table empty, initialize the first season
    if not db.query(Season).first():
        print("Initializing Season table...")
        db.add(Season(season_number=1))
        db.commit()
        if db.query(League).first() and db.query(Club).first():
            leagues = get_all_leagues(db)
            latest_season = db.query(Season).order_by(desc(Season.id)).first()
            for league in leagues:
                initialize_league_table(league_id=league.id, season_id=latest_season.id)
    db.close()


def initialize_league_table(league_id, season_id):
    """Initialize league table in the DB"""
    Base.metadata.create_all(bind=engine)  # Create tables
    db = SessionLocal()
    # If League Table table is empty, initialize the league table
    if not db.query(LeagueTable).filter(LeagueTable.id == league_id).first():
        print("Initializing League Table table...")
        clubs = get_all_clubs_with_league_id(db, league_id)
        db.add_all(
            [
                LeagueTable(season_id=season_id, league_id=league_id, club_id=club.id)
                for club in clubs
            ]
        )
        db.commit()
    db.close()
