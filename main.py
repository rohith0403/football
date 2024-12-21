import json

import pandas as pd
import streamlit as st

from classes.League import League
from classes.Team import Team
from db.store import create_tables, fetch_league_table, fetch_teams_from_db, wipe_db
from setup_db import initalize_teams


# Function to refresh the database
def refresh_tables():
    wipe_db()
    create_tables()
    initalize_teams()


# Initialize Streamlit app
st.title("Football League Simulation")

# Add "Refresh DB" button
if st.button("Refresh DB"):
    refresh_tables()
    st.session_state.clear()  # Clear session state to reset the app
    st.success("Database refreshed successfully. Reload the page to reinitialize.")

# Fetch teams only after the DB is refreshed
teams = fetch_teams_from_db()

# Initialize League only once
if "league" not in st.session_state:
    st.session_state.league = League(teams)

# Run season button (this will only run once when clicked)
if "season_run" not in st.session_state:
    st.session_state.season_run = False

if st.button("Run Full Season") and not st.session_state.season_run:
    st.session_state.league.run_season()  # Run the season and store results in session state
    st.session_state.season_run = True  # Mark the season as run to prevent rerun

# Display the final league table as an interactive table
if st.session_state.season_run:
    st.subheader("Final League Table")
    all_tables = fetch_league_table()
    # Add a slider to select the game week
    total_gameweeks = len(all_tables)
    gameweek_slider = st.slider(
        "Select Game Week",
        min_value=1,
        max_value=total_gameweeks,
        value=total_gameweeks,
        step=1,
        format="Game Week %d",
    )

    # Get the selected game week snapshot
    selected_week_snapshot = all_tables[gameweek_slider - 1]  # Slider is 1-indexed

    # Prepare the data for the league table
    league_table_df = {
        "Team": [],
        "Points": [],
        "Wins": [],
        "Draws": [],
        "Losses": [],
        "Goals Scored": [],
        "Goals Conceded": [],
        "Form": [],
        # "Last Fixture": [],
    }
    for team in selected_week_snapshot:
        league_table_df["Team"].append(team["name"])
        league_table_df["Points"].append(team["points"])
        league_table_df["Wins"].append(team["wins"])
        league_table_df["Draws"].append(team["draws"])
        league_table_df["Losses"].append(team["losses"])
        league_table_df["Goals Scored"].append(team["goals_scored"])
        league_table_df["Goals Conceded"].append(team["goals_against"])
        league_table_df["Form"].append(team["form"])
        # league_table_df["Last Fixture"].append(team.return_recent_fixture())

    league_table_df = pd.DataFrame(league_table_df)

    # Display the league table for the selected game week
    st.dataframe(league_table_df, use_container_width=True)

else:
    st.write("Click 'Run Full Season' to start the simulation.")
