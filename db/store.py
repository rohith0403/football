""" File for creating tables and querying records"""

import json
import logging
import sqlite3

from classes.League import League
from classes.Player import Player
from classes.Team import Team
from models.models import Attributes

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
    """Creates tables in the SQLite database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS leagues (
            name TEXT PRIMARY KEY,
            country TEXT,
            tier INTEGER
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS teams (
                name TEXT PRIMARY KEY,
                league TEXT,
                team_ability REAL,
                budget INTEGER,
                roster TEXT,
                stats TEXT,
                current_form TEXT,
                FOREIGN KEY (league) REFERENCES leagues(name)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS seasons (
                id INTEGER PRIMARY KEY AUTOINCREMENT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS PlayerPool (
            id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            nationalities TEXT,
            team TEXT,
            price INTEGER,
            attributes TEXT, -- JSON string for nested Pydantic object
            position TEXT,
            current_ability INTEGER,
            stats TEXT,
            form TEXT
            )
            """
        )
        conn.commit()


def insert_league(league):
    """
    Inserts a league into the leagues table in SQLite3.

    Args:
        league (League): The League object to be inserted.
    """
    league_data = (
        league.name,
        league.country,
        league.tier,
    )
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO leagues (name, country, tier)
            VALUES (?, ?, ?)
            """,
            league_data,
        )
        conn.commit()


def insert_team(team):
    """
    Inserts a team into the teams table in SQLite3.

    Args:
        team (Team): The Team object to be inserted.
    """
    team_data = (
        team.name,
        team.league,
        team.team_ability,
        team.budget,
        json.dumps(team.roster),
        json.dumps(team.stats),
        json.dumps(team.current_form),
    )
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO teams (name, league, team_ability, budget, roster, stats, current_form )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            team_data,
        )
        conn.commit()


def insert_player(player):
    """
    Insert a player into the PlayerPool table in SQLite3.

    :param player: Player object to be inserted.
    :param db_path: Path to the SQLite database file.
    """

    # Prepare player data for insertion
    player_data = (
        player.uid,
        player.name,
        player.age,
        json.dumps(player.nationalities),  # Store nationalities as JSON
        player.team,
        player.price,
        json.dumps(player.attributes.json()),  # Store attributes as JSON
        player.position,
        player.current_ability,
        json.dumps(player.stats),  # Store stats as JSON
        json.dumps(player.form),
    )
    with get_db_connection() as conn:
        # Insert data into the table
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO PlayerPool (
                id, name, age, nationalities, team, price,
                attributes, position, current_ability, stats, form
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            player_data,
        )
        conn.commit()


def fetch_all_leagues():
    """
    Fetches all leagues from the leagues table in SQLite3.

    Returns:
        list: List of league records as dictionaries.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            # Fetch all rows from the table
            cursor.execute("SELECT * FROM leagues")
            rows = cursor.fetchall()
            leagues = []
            for row in rows:
                league = League(
                    name=row[0],
                    country=row[1],
                    tier=row[2],
                )
                leagues.append(league)
        except sqlite3.Error as error:
            LOGGER.error("Error fetching leagues from leagues table: %s", error)
    return leagues


def fetch_all_teams():
    """
    Fetches all teams from the teams table in SQLite3.

    Returns:
        list: List of team records as dictionaries.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            # Fetch all rows from the table
            cursor.execute("SELECT * FROM teams")
            rows = cursor.fetchall()
            teams = []
            for row in rows:
                team = Team(
                    name=row[0],
                    league=row[1],
                    team_ability=row[2],
                    budget=row[3],
                )
                team.roster = json.loads(row[4])
                team.stats = json.loads(row[5])
                team.current_form = json.loads(row[6])
                teams.append(team)
        except sqlite3.Error as error:
            LOGGER.error("Error fetching teams from teams table: %s", error)
    return teams


def fetch_all_players(attributes_model=Attributes):
    """
    Fetches all players from the PlayerPool table in SQLite3.

    :param db_path: Path to the SQLite database file.
    :return: List of player records as dictionaries.
    """
    players = []
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            # Fetch all rows from the table
            cursor.execute("SELECT * FROM PlayerPool")
            rows = cursor.fetchall()
            # Convert rows to a list of dictionaries
            for row in rows:
                raw_json = row[6]  # This is the JSON string from the DB
                attributes = None
                if attributes_model:
                    # Step 1: Convert JSON string to dictionary
                    attributes_json = json.loads(raw_json)  # First decode
                    attributes_dict = json.loads(attributes_json)  # Second decode
                    # Step 2: Validate the dictionary with the Pydantic model
                    attributes = attributes_model.model_validate(attributes_dict)
                else:
                    attributes = json.loads(attributes_json)
                player = Player(
                    uid=row[0],
                    name=row[1],
                    age=row[2],
                    nationalities=json.loads(row[3]),
                    team=row[4],
                    price=row[5],
                    attributes=attributes,
                    position=row[7],
                    current_ability=row[8],
                    stats=json.loads(row[9]),
                    form=row[10],
                )
                players.append(player)
        except sqlite3.Error as error:
            LOGGER.error("Error fetching players from players table: %s", error)
    return players


def fetch_player_by_id(player_id: str, attributes_model=Attributes):
    """
    Fetch a single player from the PlayerPool table by their unique ID.

    :param player_id: The unique ID of the player to fetch.
    :param db_path: Path to the SQLite database file.
    :param attributes_model: Pydantic model class for attributes deserialization.
    :return: A dictionary representing the player or None if not found.
    """

    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            # Fetch the player by ID
            cursor.execute("SELECT * FROM PlayerPool WHERE id = ?", (player_id,))
            row = cursor.fetchone()

            if not row:
                conn.close()
                return None  # Player not found

            raw_json = row[6]  # This is the JSON string from the DB
            attributes = None
            if attributes_model:
                # Step 1: Convert JSON string to dictionary
                attributes_json = json.loads(raw_json)  # First decode
                attributes_dict = json.loads(attributes_json)  # Second decode
                # Step 2: Validate the dictionary with the Pydantic model
                attributes = attributes_model.model_validate(attributes_dict)
            else:
                attributes = json.loads(attributes_json)
            # Convert the row to a dictionary
            player = Player(
                uid=row[0],
                name=row[1],
                age=row[2],
                nationalities=json.loads(row[3]),
                team=row[4],
                price=row[5],
                attributes=attributes,  # Pydantic model or dict
                position=row[7],
                current_ability=row[8],
                stats=json.loads(row[9]),
                form=row[10],
            )
        except sqlite3.Error as error:
            LOGGER.error("Error fetching player from players table via id: %s", error)
    return player


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
    # create_tables_for_new_season(new_season_id)
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


# def save_teams_to_season_table(teams, season_id):
#     """
#     Saves the given teams to a season-specific table.

#     Args:
#         teams (list): List of Team objects to be saved.
#         season_id (int): The ID of the season.
#     """
#     season_table = f"teams_season{season_id}"
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(
#             f"""
#             CREATE TABLE IF NOT EXISTS {season_table} (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 0,
#                 variable_name TEXT UNIQUE,
#                 name TEXT UNIQUE,
#                 offense REAL,
#                 defense REAL,
#                 points INTEGER DEFAULT 0,
#                 wins INTEGER DEFAULT 0,
#                 draws INTEGER DEFAULT 0,
#                 losses INTEGER DEFAULT 0,
#                 goals_scored INTEGER DEFAULT 0,
#                 goals_conceded INTEGER DEFAULT 0,
#                 budget INTEGER,
#                 form TEXT,
#                 fixtures_played TEXT,
#                 roster TEXT
#             )
#             """
#         )
#         for team in teams:
#             cursor.execute(
#                 f"""
#                 INSERT OR IGNORE INTO {season_table} (
#                     variable_name,
#                     name,
#                     offense,
#                     defense,
#                     points,
#                     wins,
#                     draws,
#                     losses,
#                     goals_scored,
#                     goals_conceded,
#                     budget,
#                     form,
#                     fixtures_played,
#                     roster
#                 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                 """,
#                 (
#                     team.variable_name,
#                     team.name,
#                     team.offense,
#                     team.defense,
#                     team.points,
#                     team.wins,
#                     team.draws,
#                     team.losses,
#                     team.goals_scored,
#                     team.goals_against,
#                     team.budget,
#                     json.dumps(team.form),
#                     json.dumps(team.fixtures_played),
#                     json.dumps(team.roster),
#                 ),
#             )
#         conn.commit()


# def update_teams_in_season_table(teams, season_id):
#     """
#     Updates the given teams in a season-specific table.
#     If the team already exists, it updates the record.
#     Args:
#         teams (list): List of Team objects to be updated.
#         season_id (int): The ID of the season.
#     """
#     season_table = f"teams_season{season_id}"
#     with get_db_connection() as conn:
#         cursor = conn.cursor()

#         for team in teams:
#             cursor.execute(
#                 f"""
#                 REPLACE INTO {season_table} (
#                     variable_name,
#                     name,
#                     offense,
#                     defense,
#                     points,
#                     wins,
#                     draws,
#                     losses,
#                     goals_scored,
#                     goals_conceded,
#                     budget,
#                     form,
#                     fixtures_played,
#                     roster
#                 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                 """,
#                 (
#                     team.variable_name,
#                     team.name,
#                     team.offense,
#                     team.defense,
#                     team.points,
#                     team.wins,
#                     team.draws,
#                     team.losses,
#                     team.goals_scored,
#                     team.goals_against,
#                     team.budget,
#                     json.dumps(team.form),
#                     json.dumps(team.fixtures_played),
#                     json.dumps([player.to_dict() for player in team.roster]),
#                 ),
#             )
#         conn.commit()


# def fetch_teams_from_season_table(season_id):
#     """
#     Fetches all teams from a specific season's table.

#     Args:
#         season_id (int): The ID of the season.

#     Returns:
#         list: List of Team objects.
#     """
#     season_table = f"teams_season{season_id}"
#     teams = []
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute(f"SELECT * FROM {season_table}")
#             for row in cursor.fetchall():
#                 team = Team(
#                     variable_name=row[1],
#                     name=row[2],
#                     offense=row[3],
#                     defense=row[4],
#                     points=row[5],
#                     wins=row[6],
#                     draws=row[7],
#                     losses=row[8],
#                     goals_scored=row[9],
#                     goals_against=row[10],
#                     budget=row[11],
#                 )
#                 team.form = json.loads(row[12])
#                 team.fixtures_played = json.loads(row[13])
#                 team.roster = json.loads(row[14])
#                 teams.append(team)
#         except sqlite3.Error as error:
#             LOGGER.error("Error fetching teams from teams table: %s", error)
#     return teams


# def insert_into_player_pool(player):
#     """
#     Insert a player into the PlayerPool table in SQLite3.

#     :param player: Player object to be inserted.
#     :param db_path: Path to the SQLite database file.
#     """

#     # Prepare player data for insertion
#     player_data = (
#         player.uid,
#         player.name,
#         player.age,
#         json.dumps(player.nationalities),  # Store nationalities as JSON
#         player.pot_ability,
#         "" if player.team is None else json.dumps(player.team),
#         player.price,
#         json.dumps(player.attributes.json()),  # Store attributes as JSON
#         player.position,
#         player.current_ability,
#         json.dumps(player.stats),  # Store stats as JSON
#         player.form,
#     )
#     with get_db_connection() as conn:
#         # Insert data into the table
#         cursor = conn.cursor()
#         cursor.execute(
#             """
#         INSERT INTO PlayerPool (
#             id, name, age, nationalities, potential_ability, team, price,
#             attributes, position, current_ability, stats, form
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """,
#             player_data,
#         )

#         conn.commit()


# def update_players_team(changed_players):
#     """
#     Update the team attribute for each player in the PlayerPool table.

#     Args:
#         changed_players (list of Player): List of Player objects with updated team data.
#     """
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         try:
#             for player in changed_players:
#                 cursor.execute(
#                     """
#                     UPDATE PlayerPool
#                     SET team = ?
#                     WHERE id = ?
#                     """,
#                     (json.dumps(player.team.to_dict()) if player.team else "", player.uid)
#                 )
#             conn.commit()
#         except sqlite3.Error as error:
#             LOGGER.error("Error updating team for players in PlayerPool: %s", error)


# def fetch_players_from_pool(attributes_model=Attributes):
#     """
#     Fetch all players from the PlayerPool table in SQLite3.

#     :param db_path: Path to the SQLite database file.
#     :return: List of player records as dictionaries.
#     """
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         try:

#             # Fetch all rows from the table
#             cursor.execute("SELECT * FROM PlayerPool")
#             rows = cursor.fetchall()
#             # Convert rows to a list of dictionaries
#             players = []
#             for row in rows:
#                 raw_json = row[7]  # This is the JSON string from the DB
#                 attributes = None
#                 if attributes_model:
#                     # Step 1: Convert JSON string to dictionary
#                     attributes_json = json.loads(raw_json)  # First decode
#                     attributes_dict = json.loads(attributes_json)  # Second decode
#                     # Step 2: Validate the dictionary with the Pydantic model
#                     attributes = attributes_model.model_validate(attributes_dict)
#                 else:
#                     attributes = json.loads(attributes_json)
#                 player = Player(
#                     uid=row[0],
#                     name=row[1],
#                     age=row[2],
#                     nationalities=json.loads(row[3]),
#                     pot_ability=row[4],
#                     team=None if row[5] == "" else json.loads(row[5]),
#                     price=row[6],
#                     attributes=attributes,
#                     position=row[8],
#                     current_ability=row[9],
#                     stats=json.loads(row[10]),
#                     form=row[11],
#                 )
#                 players.append(player)
#         except sqlite3.Error as error:
#             LOGGER.error("Error fetching players from players table: %s", error)
#     return players


# def fetch_player_by_id(player_id: str, attributes_model=Attributes):
#     """
#     Fetch a single player from the PlayerPool table by their unique ID.

#     :param player_id: The unique ID of the player to fetch.
#     :param db_path: Path to the SQLite database file.
#     :param attributes_model: Pydantic model class for attributes deserialization.
#     :return: A dictionary representing the player or None if not found.
#     """

#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         try:
#             # Fetch the player by ID
#             cursor.execute("SELECT * FROM PlayerPool WHERE id = ?", (player_id,))
#             row = cursor.fetchone()

#             if not row:
#                 conn.close()
#                 return None  # Player not found

#             raw_json = row[7]  # This is the JSON string from the DB
#             attributes = None
#             if attributes_model:
#                 # Step 1: Convert JSON string to dictionary
#                 attributes_json = json.loads(raw_json)  # First decode
#                 attributes_dict = json.loads(attributes_json)  # Second decode
#                 # Step 2: Validate the dictionary with the Pydantic model
#                 attributes = attributes_model.model_validate(attributes_dict)
#             else:
#                 attributes = json.loads(attributes_json)
#             # Convert the row to a dictionary
#             player = Player(
#                 uid=row[0],
#                 name=row[1],
#                 age=row[2],
#                 nationalities=json.loads(row[3]),
#                 pot_ability=row[4],
#                 team=None if row[5] == "" else json.loads(row[5]),
#                 price=row[6],
#                 attributes=attributes,  # Pydantic model or dict
#                 position=row[8],
#                 current_ability=row[9],
#                 stats=json.loads(row[10]),
#                 form=row[11],
#             )
#         except sqlite3.Error as error:
#             LOGGER.error("Error fetching player from players table via id: %s", error)
#     return player


# def save_league_history_to_season_table(snapshot, season_id):
#     """
#     Saves league history (gameweeks) to a season-specific table.

#     Args:
#         snapshot (dict): The league history to save.
#         season_id (int): The ID of the season.
#     """
#     season_table = f"gameweeks_season{season_id}"
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute(
#                 f"""
#                 CREATE TABLE IF NOT EXISTS {season_table} (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     data TEXT NOT NULL
#                 )
#                 """
#             )
#             cursor.execute(
#                 f"INSERT INTO {season_table} (data) VALUES (?)",
#                 (json.dumps(snapshot),),
#             )
#             conn.commit()
#         except sqlite3.Error as error:
#             LOGGER.error("Error saving league history: %s", error)


# def fetch_league_history_from_season_table(season_id):
#     """
#     Fetches league history (gameweeks) from a season-specific table.

#     Args:
#         season_id (int): The ID of the season.

#     Returns:
#         list: List of gameweeks (deserialized JSON).
#     """
#     season_table = f"gameweeks_season{season_id}"
#     gameweeks = []
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute(f"SELECT * FROM {season_table}")
#             for row in cursor.fetchall():
#                 gameweeks.append(json.loads(row[1]))
#         except sqlite3.Error as error:
#             LOGGER.error("Error fetching league history: %s", error)
#     return gameweeks


# def create_tables_for_new_season(season_id):
#     """
#     Creates the tables for teams and gameweeks for a new season.

#     Args:
#         season_id (int): The ID of the new season.
#     """
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(
#             f"""
#             CREATE TABLE IF NOT EXISTS teams_season{season_id} (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 variable_name TEXT UNIQUE,
#                 name TEXT UNIQUE,
#                 offense REAL,
#                 defense REAL,
#                 points INTEGER DEFAULT 0,
#                 wins INTEGER DEFAULT 0,
#                 draws INTEGER DEFAULT 0,
#                 losses INTEGER DEFAULT 0,
#                 goals_scored INTEGER DEFAULT 0,
#                 goals_conceded INTEGER DEFAULT 0,
#                 budget INTEGER,
#                 form TEXT,
#                 fixtures_played TEXT,
#                 roster TEXT
#             )
#             """
#         )
#         cursor.execute(
#             f"""
#             CREATE TABLE IF NOT EXISTS gameweeks_season{season_id} (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 data TEXT NOT NULL
#             )
#             """
#         )
#         conn.commit()


# def update_offense_defense_ratings_for_new_season(current_season_id, new_season_id):
#     """
#     Updating offense and defense based on performace on previous years"""
#     # Fetch teams from the current season
#     current_teams = fetch_teams_from_season_table(current_season_id)

#     # Fetch max goals scored and min goals conceded in the current season
#     max_goals_scored = max(team.goals_scored for team in current_teams)
#     min_goals_conceded = min(team.goals_against for team in current_teams)
#     new_teams = []
#     for team in current_teams:
#         # Calculate the new offense rating
#         calculated_offense_rating = round(
#             (team.goals_scored / max_goals_scored) * 99, 2
#         )
#         new_offense_rating = (team.offense + calculated_offense_rating) / 2

#         # Calculate the new defense rating
#         calculated_defense_rating = (min_goals_conceded / team.goals_against) * 99
#         new_defense_rating = (team.defense + calculated_defense_rating) / 2
#         new_team = Team(
#             team.variable_name,
#             team.name,
#             new_offense_rating,
#             new_defense_rating,
#             budget=team.budget,
#         )
#         new_teams.append(new_team)
#         save_teams_to_season_table(new_teams, new_season_id)


def wipe_season_data():
    """
    Deletes all season-specific data but retains the structure.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            # max_season_id = fetch_season_id()
            # for season_id in range(1, max_season_id + 1):
            #     cursor.execute(f"DROP TABLE IF EXISTS teams_season{season_id}")
            #     cursor.execute(f"DROP TABLE IF EXISTS gameweeks_season{season_id}")
            cursor.execute("DROP TABLE IF EXISTS PlayerPool")
            cursor.execute("DROP TABLE IF EXISTS seasons")
            cursor.execute("DROP TABLE IF EXISTS teams")
            cursor.execute("DROP TABLE IF EXISTS leagues")
            conn.commit()
            LOGGER.info("Season-specific data wiped successfully.")
        except sqlite3.Error as error:
            LOGGER.error("Error wiping season data: %s", error)
