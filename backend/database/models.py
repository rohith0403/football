from sqlalchemy import Column, ForeignKey, Integer, String
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


class Club(Base):
    """Club Table"""

    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    league_id = Column(Integer, ForeignKey("leagues.id"))  # Foreign key reference

    # A club is associated with a league and players
    league = relationship("League", back_populates="clubs")  # Relationship to League
    players = relationship("Player", back_populates="club")  # Relationship to Player


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
