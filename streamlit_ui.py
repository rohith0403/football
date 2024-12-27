import pandas as pd
import streamlit as st
from PIL import Image

from classes.League import League
from db.store import (
    create_new_season,
    create_tables,
    fetch_league_history_from_season_table,
    fetch_season_id,
    fetch_teams_from_season_table,
    update_offense_defense_ratings_for_new_season,
    wipe_season_data,
)
from generators.team_generator import initialize_teams


# Function to refresh the database
def initialize_db():
    wipe_season_data()
    create_tables()


# Function to handle button clicks based on image
def image_button(image_path, label):
    img = Image.open(image_path)
    img = img.resize((50, 50))
    st.sidebar.image(img, caption=label)


# Add the sidebar
with st.sidebar:
    st.title("Menu")

    # Custom buttons with PNG images
    league_button = image_button("icons/league.png", "League")
    team_button = image_button("icons/teams.png", "Team")
    player_button = image_button("icons/players.png", "Player")

    if league_button:
        st.write("Home Button Pressed")
    elif team_button:
        st.write("Settings Button Pressed")
    elif player_button:
        st.write("Stats Button Pressed")

st.title("Football League Simulation")

col1, col2, col3 = st.columns(3)


# Add "Refresh DB" button
with col1:
    if st.button("Initialize DB"):
        initialize_db()
        st.session_state.clear()  # Clear session state to reset the app
        st.success("Database Initialized.")

# Add "Generate New season" button
with col2:
    if st.button("Generate new season"):
        create_new_season()
        new_season_id = fetch_season_id()
        if new_season_id == 1:
            initialize_teams(new_season_id)
        else:
            update_offense_defense_ratings_for_new_season(
                new_season_id - 1, new_season_id
            )
        st.success("Generated a new season.")

        # Reinitialize the League object after generating a new season
        teams = fetch_teams_from_season_table(new_season_id)
        st.session_state.league = League(
            teams
        )  # Reinitialize the league for the new season

        # Reset season_run flag
        st.session_state.season_run = False
        st.session_state.show_run_season_button = (
            True  # Show the Run Season button again
        )


current_season_id = fetch_season_id()

# Fetch teams only after the DB is refreshed
teams = fetch_teams_from_season_table(current_season_id)

# Initialize League only once
if "league" not in st.session_state:
    st.session_state.league = League(teams)

# Initialize show_run_season_button in session state
if "show_run_season_button" not in st.session_state:
    st.session_state.show_run_season_button = True

# Run season button (this will only run once when clicked)
if "season_run" not in st.session_state:
    st.session_state.season_run = False

# Run season button (visible only when show_run_season_button is True)
with col3:
    if st.session_state.show_run_season_button:
        if (
            st.button(f"Run Season {current_season_id}")
            and not st.session_state.season_run
        ):
            st.session_state.league.run_season(
                current_season_id
            )  # Run the season and store results in session state
            st.session_state.season_run = (
                True  # Mark the season as run to prevent rerun
            )
            st.session_state.show_run_season_button = (
                False  # Hide the Run Season button
            )

# Display the final league table as an interactive table
if st.session_state.season_run:
    st.subheader("League Table")

    season_options = [f"Season {i+1}" for i in range(current_season_id)]

    # Dropdown to select the season
    selected_season = st.selectbox(
        "Select Season",
        options=season_options,
        index=current_season_id - 1,  # Default to the latest season
    )

    # Get the selected season's index
    selected_season_index = season_options.index(selected_season) + 1

    # Get the selected season's data
    selected_season_data = fetch_league_history_from_season_table(selected_season_index)

    # Add a slider to select the game week
    TOTAL_GAMEWEEKS = len(selected_season_data)
    gameweek_slider = st.slider(
        "Select Game Week",
        min_value=1,
        max_value=TOTAL_GAMEWEEKS,
        value=TOTAL_GAMEWEEKS,
        step=1,
        format="Game Week %d",
    )

    # Get the selected game week snapshot
    selected_week_snapshot = selected_season_data[gameweek_slider - 1]

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
        "Budget": [],
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
        league_table_df["Budget"].append(team["budget"])
        # league_table_df["Last Fixture"].append(team.return_recent_fixture())

    league_table_df = pd.DataFrame(league_table_df)

    league_table_df = league_table_df.sort_values(
        by="Points", ascending=False
    ).reset_index(drop=True)

    # Display the league table for the selected game week
    st.dataframe(league_table_df, use_container_width=True)

else:
    st.write("Click 'Run Season' to start the simulation.")
