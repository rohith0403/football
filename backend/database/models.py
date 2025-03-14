from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


class League(Base):
    """League Table"""

    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    clubs = relationship("Club", back_populates="league")  # Relationship to Club
    league_table = relationship("LeagueTable", back_populates="league")
    fixtures = relationship("Fixtures", back_populates="league")


class Club(Base):
    """Club Table"""

    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    league_id = Column(Integer, ForeignKey("leagues.id"))  # Foreign key reference

    # A club is associated with a league and players
    league = relationship("League", back_populates="clubs")  # Relationship to League
    players = relationship("Player", back_populates="club")  # Relationship to Player
    league_table = relationship("LeagueTable", back_populates="club")
    home_fixtures = relationship(
        "Fixtures", foreign_keys="Fixtures.home_club_id", back_populates="home_club"
    )
    away_fixtures = relationship(
        "Fixtures", foreign_keys="Fixtures.away_club_id", back_populates="away_club"
    )


class Player(Base):
    """Player Table"""

    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, index=True)
    club_id = Column(
        Integer, ForeignKey("clubs.id"), nullable=True
    )  # Foreign key reference

    # A player is associated with a club
    club = relationship("Club", back_populates="players")  # Relationship to Club


class LeagueTable(Base):
    """League Table"""

    __tablename__ = "league_table"

    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    games_played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    points = Column(Integer, default=0)
    recent_form = Column(String, default="")  # Last 5 matches (e.g., "WWLDW")

    club = relationship("Club", back_populates="league_table")
    league = relationship("League", back_populates="league_table")
    season = relationship("Season", back_populates="league_table")
    # fixtures = relationship("Fixtures", back_populates="league_table")


class Season(Base):
    """Seasons Table"""

    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True, index=True)
    season_number = Column(Integer, unique=True)

    league_table = relationship("LeagueTable", back_populates="season")


class Fixtures(Base):
    "Fixtures Table"

    __tablename__ = "fixtures"

    id = Column(Integer, primary_key=True, index=True)
    gameweek = Column(Integer, unique=False)
    home_club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    away_club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    # league_table_id = Column(Integer, ForeignKey("league_table.id"), nullable=False)
    home_club_goals = Column(Integer, unique=False)
    away_club_goals = Column(Integer, unique=False)
    played_status = Column(Boolean, default=False)

    home_club = relationship(
        "Club", foreign_keys=[home_club_id], back_populates="home_fixtures"
    )
    away_club = relationship(
        "Club", foreign_keys=[away_club_id], back_populates="away_fixtures"
    )
    league = relationship("League", back_populates="fixtures")
    # league_table = relationship("LeagueTable", back_populates="fixtures")
