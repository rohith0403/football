import random

from database.crud import add_fixture, get_all_clubs_with_league_id


def generate_fixtures(db, league_id):
    """
    Generate double round-robin fixtures for the given clubs and shuffle them.

    :param league_id: ID of the league
    :return: List of fixtures structured as (gameweek, home_team, away_team).
    """
    clubs = get_all_clubs_with_league_id(db, league_id)
    num_clubs = len(clubs)
    num_gameweeks = (num_clubs - 1) * 2  # Double round-robin gameweeks

    # Generate all matchups (each team plays home & away)
    matches = [(home, away) for i, home in enumerate(clubs) for away in clubs[i + 1 :]]
    matches += [
        (away, home) for home, away in matches
    ]  # Reverse for home & away fixtures

    # Shuffle fixtures to randomize order
    random.shuffle(matches)

    # Allocate matches to gameweeks ensuring each team plays only once per gameweek
    gameweeks = [[] for _ in range(num_gameweeks)]
    used_clubs_per_week = [set() for _ in range(num_gameweeks)]

    for home, away in matches:
        for gw in range(num_gameweeks):
            # If condition to check no yeam plays twice in a game week
            if (
                home not in used_clubs_per_week[gw]
                and away not in used_clubs_per_week[gw]
            ):
                gameweeks[gw].append((home, away))
                used_clubs_per_week[gw].update([home, away])
                break

    # Convert to structured output
    structured_fixtures = []
    for gw, matches in enumerate(gameweeks, start=1):
        for home, away in matches:
            add_fixture(
                db,
                gameweek=gw,
                home_club_id=home.id,
                away_club_id=away.id,
                league_id=league_id,
            )
            structured_fixtures.append((gw, home, away))

    fixtures = []
    # return structured_fixtures
    for gameweek, home, away in structured_fixtures:
        fixtures.append(f"Gameweek {gameweek}: {home.name} vs {away.name}")
    return fixtures
