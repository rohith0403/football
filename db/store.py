import json
import sqlite3

from classes.Team import Team


# Create a function to return a connection
def get_db_connection():
    """Returns a new SQLite connection for each thread."""
    return sqlite3.connect("league_simulation.db", check_same_thread=False)


# Function to create tables if they don't exist
def create_tables():
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Create the 'teams' table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                variable_name TEXT UNIQUE,
                name TEXT UNIQUE,
                offense REAL,
                defense REAL,
                points INTEGER,
                wins INTEGER,
                draws INTEGER,
                losses INTEGER,
                goals_scored INTEGER,
                goals_conceded INTEGER,
                form TEXT,
                fixtures_played TEXT
            )
            """
        )

        # Create the 'gameweeks' table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS gameweeks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL -- JSON serialized list of dicts
            )
            """
        )

        # Commit changes to the database
        conn.commit()


# Save teams to the database
def save_teams_to_db(teams):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for team in teams:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO teams (
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
                        form,
                        fixtures_played
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                        json.dumps(team.form),
                        json.dumps(team.fixtures_played),  # Serialize fixtures_played
                    ),
                )
            conn.commit()
    except Exception as e:
        print(f"Error saving teams to the database: {e}")


# Fetch teams from the database and return a list of Team instances
def fetch_teams_from_db():
    teams = []
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teams")
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
                )
                # Deserialize fixtures_played
                team.form = json.loads(row[11])
                team.fixtures_played = json.loads(row[12])
                teams.append(team)
    except Exception as e:
        print(f"Error fetching teams from the database: {e}")
    return teams


# Save league history to the database
def save_league_history_to_db(snapshot):
    history_json = json.dumps(snapshot)  # Serialize history to JSON
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO gameweeks (data)
                VALUES (?)
                """,
                (history_json,),
            )
            conn.commit()
    except Exception as e:
        print(f"Error saving league history to the database: {e}")


# Fetch the league table from the database
def fetch_league_table():
    """Fetch all rows from the gameweeks table and deserialize JSON fields."""
    all_gameweeks = []
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gameweeks")
            for tables in cursor.fetchall():
                gameweek = json.loads(tables[1])  # Deserialize the list of dicts
                all_gameweeks.append(gameweek)
    except Exception as e:
        print(f"Error fetching league table from the database: {e}")
    return all_gameweeks


def wipe_db():
    """Wipe all tables in the database to reset it."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Drop tables if they exist
            cursor.execute("DROP TABLE IF EXISTS teams")
            cursor.execute("DROP TABLE IF EXISTS gameweeks")

            # Commit changes
            conn.commit()
            print("Database wiped successfully.")
    except Exception as e:
        print(f"Error wiping the database: {e}")
