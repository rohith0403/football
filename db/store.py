""" File for creating tables and querying records"""

import json
import logging
import sqlite3

from classes.Team import Team

# Constants
DB_FILE = "league_simulation.db"

# Set up logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def get_db_connection():
    """
    Returns a new SQLite connection for each thread.
    """
    return sqlite3.connect(DB_FILE, check_same_thread=False)


def create_tables():
    """
    Creates the seasons table if it does not already exist.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS seasons (
                id INTEGER PRIMARY KEY AUTOINCREMENT
            )
            """
        )
        conn.commit()


def create_new_season():
    """
    Creates a new season entry and returns the season ID.

    Returns:
        int: The ID of the new season.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO seasons DEFAULT VALUES")
        new_season_id = cursor.lastrowid
        conn.commit()
    create_tables_for_new_season(new_season_id)
    return new_season_id


def fetch_season_id():
    """
    Fetches the latest season_id from the database.

    Returns:
        int: The most recent season_id. Returns 1 if no season exists.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            # Fetch the max id from the season table
            cursor.execute("SELECT MAX(id) FROM seasons")
            result = cursor.fetchone()
            return result[0]
        except sqlite3.Error as error:
            LOGGER.error("Error fetching season id from season table: %s", error)
    return 0


def save_teams_to_season_table(teams, season_id):
    """
    Saves the given teams to a season-specific table.

    Args:
        teams (list): List of Team objects to be saved.
        season_id (int): The ID of the season.
    """
    season_table = f"teams_season{season_id}"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {season_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 0,
                variable_name TEXT UNIQUE,
                name TEXT UNIQUE,
                offense REAL,
                defense REAL,
                points INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                goals_scored INTEGER DEFAULT 0,
                goals_conceded INTEGER DEFAULT 0,
                budget INTEGER,
                form TEXT,
                fixtures_played TEXT
            )
            """
        )
        for team in teams:
            cursor.execute(
                f"""
                INSERT OR IGNORE INTO {season_table} (
                    variable_name,
                    name,
                    offense,
                    defense,
                    points,
                    wins,
                    draws,
                    losses,
                    goals_scored,
                    goals_conceded,
                    budget,
                    form,
                    fixtures_played
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    team.variable_name,
                    team.name,
                    team.offense,
                    team.defense,
                    team.points,
                    team.wins,
                    team.draws,
                    team.losses,
                    team.goals_scored,
                    team.goals_against,
                    team.budget,
                    json.dumps(team.form),
                    json.dumps(team.fixtures_played),
                ),
            )
        conn.commit()


def update_teams_in_season_table(teams, season_id):
    """
    Updates the given teams in a season-specific table. If the team already exists, it updates the record;
    otherwise, it inserts a new record.

    Args:
        teams (list): List of Team objects to be updated.
        season_id (int): The ID of the season.
    """
    season_table = f"teams_season{season_id}"
    with get_db_connection() as conn:
        cursor = conn.cursor()

        for team in teams:
            cursor.execute(
                f"""
                INSERT OR REPLACE INTO {season_table} (
                    variable_name,
                    name,
                    offense,
                    defense,
                    points,
                    wins,
                    draws,
                    losses,
                    goals_scored,
                    goals_conceded,
                    budget,
                    form,
                    fixtures_played
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    team.variable_name,
                    team.name,
                    team.offense,
                    team.defense,
                    team.points,
                    team.wins,
                    team.draws,
                    team.losses,
                    team.goals_scored,
                    team.goals_against,
                    team.budget,
                    json.dumps(team.form),
                    json.dumps(team.fixtures_played),
                ),
            )
        conn.commit()


def fetch_teams_from_season_table(season_id):
    """
    Fetches all teams from a specific season's table.

    Args:
        season_id (int): The ID of the season.

    Returns:
        list: List of Team objects.
    """
    season_table = f"teams_season{season_id}"
    teams = []
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {season_table}")
            for row in cursor.fetchall():
                team = Team(
                    variable_name=row[1],
                    name=row[2],
                    offense=row[3],
                    defense=row[4],
                    points=row[5],
                    wins=row[6],
                    draws=row[7],
                    losses=row[8],
                    goals_scored=row[9],
                    goals_against=row[10],
                    budget=row[11],
                )
                team.form = json.loads(row[12])
                team.fixtures_played = json.loads(row[13])

                teams.append(team)
        except sqlite3.Error as error:
            LOGGER.error("Error fetching teams from teams table: %s", error)
    return teams


def save_league_history_to_season_table(snapshot, season_id):
    """
    Saves league history (gameweeks) to a season-specific table.

    Args:
        snapshot (dict): The league history to save.
        season_id (int): The ID of the season.
    """
    season_table = f"gameweeks_season{season_id}"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {season_table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                f"INSERT INTO {season_table} (data) VALUES (?)",
                (json.dumps(snapshot),),
            )
            conn.commit()
        except sqlite3.Error as error:
            LOGGER.error("Error saving league history: %s", error)


def fetch_league_history_from_season_table(season_id):
    """
    Fetches league history (gameweeks) from a season-specific table.

    Args:
        season_id (int): The ID of the season.

    Returns:
        list: List of gameweeks (deserialized JSON).
    """
    season_table = f"gameweeks_season{season_id}"
    gameweeks = []
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {season_table}")
            for row in cursor.fetchall():
                gameweeks.append(json.loads(row[1]))
        except sqlite3.Error as error:
            LOGGER.error("Error fetching league history: %s", error)
    return gameweeks


def create_tables_for_new_season(season_id):
    """
    Creates the tables for teams and gameweeks for a new season.

    Args:
        season_id (int): The ID of the new season.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS teams_season{season_id} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                variable_name TEXT UNIQUE,
                name TEXT UNIQUE,
                offense REAL,
                defense REAL,
                points INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                goals_scored INTEGER DEFAULT 0,
                goals_conceded INTEGER DEFAULT 0,
                budget INTEGER,
                form TEXT,
                fixtures_played TEXT
            )
            """
        )
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS gameweeks_season{season_id} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL
            )
            """
        )
        conn.commit()


def wipe_season_data():
    """
    Deletes all season-specific data but retains the structure.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            max_season_id = fetch_season_id()
            for season_id in range(1, max_season_id + 1):
                cursor.execute(f"DROP TABLE IF EXISTS teams_season{season_id}")
                cursor.execute(f"DROP TABLE IF EXISTS gameweeks_season{season_id}")
            cursor.execute("DROP TABLE IF EXISTS seasons")
            conn.commit()
            LOGGER.info("Season-specific data wiped successfully.")
        except sqlite3.Error as error:
            LOGGER.error("Error wiping season data: %s", error)


def update_offense_defense_ratings_for_new_season(current_season_id, new_season_id):
    """
    Updating offense and defense based on performace on previous years"""
    # Fetch teams from the current season
    current_teams = fetch_teams_from_season_table(current_season_id)

    # Fetch max goals scored and min goals conceded in the current season
    max_goals_scored = max(team.goals_scored for team in current_teams)
    min_goals_conceded = min(team.goals_against for team in current_teams)
    new_teams = []
    for team in current_teams:
        # Calculate the new offense rating
        calculated_offense_rating = round(
            (team.goals_scored / max_goals_scored) * 99, 2
        )
        new_offense_rating = (team.offense + calculated_offense_rating) / 2

        # Calculate the new defense rating
        calculated_defense_rating = (min_goals_conceded / team.goals_against) * 99
        new_defense_rating = (team.defense + calculated_defense_rating) / 2
        new_team = Team(
            team.variable_name,
            team.name,
            new_offense_rating,
            new_defense_rating,
            budget=team.budget,
        )
        new_teams.append(new_team)
        save_teams_to_season_table(new_teams, new_season_id)
