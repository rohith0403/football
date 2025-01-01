from classes.League import League
from db.store import insert_league


def initialize_league():
    """
    Initialize the league with teams and fixtures
    """
    # Create a league
    leagues = [
        League(name="Premier League", country="England", tier=1),
        League(name="La Liga", country="Spain", tier=1),
        League(name="Serie A", country="Italy", tier=1),
        League(name="Bundesliga", country="Germany", tier=1),
        League(name="Ligue 1", country="France", tier=1)
    ]
    for league in leagues:
        insert_league(league)
    return leagues