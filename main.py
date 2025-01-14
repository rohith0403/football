import pandas as pd
import streamlit as st

# from classes.League import League
from db.store import (  # create_new_season,; fetch_league_history_from_season_table,; fetch_player_by_id,; fetch_players_from_pool,; fetch_season_id,; fetch_teams_from_season_table,; update_offense_defense_ratings_for_new_season,; wipe_season_data,
    create_tables,
    fetch_all_players,
    fetch_all_teams,
    wipe_season_data,
)
from initializers.league_initializer import initialize_league
from initializers.team_initializer import initialize_premier_league

# from generators.player_generator import add_players_to_pool
# from generators.team_generator import initialize_teams
# from services.assign_players import initialize_players_to_teams


# Function to refresh the database
def initialize_db():
    """Initialize Database"""
    wipe_season_data()
    create_tables()
    initialize_league()
    initialize_premier_league()


st.title("Football Simulation")


col1, col2 = st.columns(2)

# Add "Refresh DB" button
with col1:
    if st.button("Initialize DB"):
        initialize_db()
        st.session_state.clear()  # Clear session state to reset the app
        st.success("Database Initialized.")

# # Add "Generate New season" button
# with col2:
#     if st.button("Generate new season"):
#         create_new_season()
#         new_season_id = fetch_season_id()
#         if new_season_id == 1:
#             initialize_teams(new_season_id)
#             add_players_to_pool()
#             initialize_players_to_teams()
#         else:
#             update_offense_defense_ratings_for_new_season(
#                 new_season_id - 1, new_season_id
#             )
#         st.success("Generated a new season.")

#         # Reinitialize the League object after generating a new season
#         teams = fetch_teams_from_season_table(new_season_id)
#         st.session_state.league = League(
#             teams
#         )  # Reinitialize the league for the new season

#         # Reset season_run flag
#         st.session_state.season_run = False
#         st.session_state.show_run_season_button = (
#             True  # Show the Run Season button again
#         )

# Tabs for navigation
tabs = st.tabs(["League", "Players", "Teams"])

with tabs[0]:  # League tab
    st.header("League Simulation")


#     current_season_id = fetch_season_id()

#     # Fetch teams only after the DB is refreshed
#     teams = fetch_teams_from_season_table(current_season_id)

#     # Initialize League only once
#     if "league" not in st.session_state:
#         st.session_state.league = League(teams)

#     # Initialize show_run_season_button in session state
#     if "show_run_season_button" not in st.session_state:
#         st.session_state.show_run_season_button = True

#     # Run season button (this will only run once when clicked)
#     if "season_run" not in st.session_state:
#         st.session_state.season_run = False

#     # Run season button (visible only when show_run_season_button is True)
#     if st.session_state.show_run_season_button:
#         if (
#             st.button(f"Run Season {current_season_id}")
#             and not st.session_state.season_run
#         ):
#             st.session_state.league.run_season(
#                 current_season_id
#             )  # Run the season and store results in session state
#             st.session_state.season_run = (
#                 True  # Mark the season as run to prevent rerun
#             )
#             st.session_state.show_run_season_button = (
#                 False  # Hide the Run Season button
#             )

#     # Display the final league table as an interactive table
#     if st.session_state.season_run:
#         st.subheader("League Table")

#         season_options = [f"Season {i+1}" for i in range(current_season_id)]

#         # Dropdown to select the season
#         selected_season = st.selectbox(
#             "Select Season",
#             options=season_options,
#             index=current_season_id - 1,  # Default to the latest season
#         )

#         # Get the selected season's index
#         selected_season_index = season_options.index(selected_season) + 1

#         # Get the selected season's data
#         selected_season_data = fetch_league_history_from_season_table(
#             selected_season_index
#         )

#         # Add a slider to select the game week
#         TOTAL_GAMEWEEKS = len(selected_season_data)
#         gameweek_slider = st.slider(
#             "Select Game Week",
#             min_value=1,
#             max_value=TOTAL_GAMEWEEKS,
#             value=TOTAL_GAMEWEEKS,
#             step=1,
#             format="Game Week %d",
#         )

#         # Get the selected game week snapshot
#         selected_week_snapshot = selected_season_data[gameweek_slider - 1]

#         # Prepare the data for the league table
#         league_table_df = {
#             "Team": [],
#             "Points": [],
#             "Wins": [],
#             "Draws": [],
#             "Losses": [],
#             "Goals Scored": [],
#             "Goals Conceded": [],
#             "Form": [],
#             "Budget": [],
#         }
#         for team in selected_week_snapshot:
#             league_table_df["Team"].append(team["name"])
#             league_table_df["Points"].append(team["points"])
#             league_table_df["Wins"].append(team["wins"])
#             league_table_df["Draws"].append(team["draws"])
#             league_table_df["Losses"].append(team["losses"])
#             league_table_df["Goals Scored"].append(team["goals_scored"])
#             league_table_df["Goals Conceded"].append(team["goals_against"])
#             league_table_df["Form"].append(team["form"])
#             league_table_df["Budget"].append(team["budget"])

#         league_table_df = pd.DataFrame(league_table_df)

#         league_table_df = league_table_df.sort_values(
#             by="Points", ascending=False
#         ).reset_index(drop=True)

#         # Display the league table for the selected game week
#         st.dataframe(league_table_df, use_container_width=True)

#     else:
#         st.write("Click 'Run Season' to start the simulation.")

with tabs[1]:  # Player tab
    st.header("Player Management")

    players = fetch_all_players()

    #     if "players_generated" not in st.session_state:
    #         st.session_state.players_generated = False

    #     if "selected_player" not in st.session_state:
    #         st.session_state.selected_player = None

    #     if st.button("Generate Players"):
    #         add_players_to_pool()
    #         st.session_state.players_generated = True
    #         st.success("Players generated successfully!")

    if len(players) > 0:
        # if st.session_state.players_generated:
        #     players = fetch_players_from_pool()
        player_table_df = {
            "ID": [],
            "Name": [],
            "Age": [],
            "Nationality": [],
            "Current Ability": [],
            "Position": [],
            "Team": [],
            "Form": [],
            "Stats": [],
            "Price": [],
        }
        for player in players:
            player_table_df["ID"].append(player.uid)
            player_table_df["Name"].append(player.name)
            player_table_df["Age"].append(player.age)
            player_table_df["Nationality"].append(player.nationalities)
            player_table_df["Current Ability"].append(player.current_ability)
            player_table_df["Position"].append(player.position)
            player_table_df["Team"].append(player.team)
            player_table_df["Form"].append(player.form)
            player_table_df["Stats"].append(player.stats)
            player_table_df["Price"].append(player.price)

        player_table_df = pd.DataFrame(player_table_df)

        # Display the league table for the selected game week
        st.dataframe(player_table_df, use_container_width=True)

#         col1, col2, col3 = st.columns(3)

#         with col1:
#             selected_column = st.selectbox(
#                 "Select a column to filter", player_table_df.columns
#             )

#         with col2:
#             # Text field to input search value
#             search_value = st.text_input("Enter search value")

#         with col3:
#             # Search button
#             if st.button("Search"):
#                 filtered_players = player_table_df[
#                     player_table_df[selected_column]
#                     .astype(str)
#                     .str.contains(search_value, case=False, na=False)
#                 ]
#                 selected_player = fetch_player_by_id(filtered_players["ID"].tolist()[0])
#                 st.session_state.selected_player = selected_player

#         if st.session_state.selected_player:
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.subheader("Technical Attributes")
#                 st.dataframe(
#                     st.session_state.selected_player.attributes.technical.model_dump()
#                 )

#             with col2:
#                 st.subheader("Mental Attributes")
#                 st.dataframe(
#                     st.session_state.selected_player.attributes.mental.model_dump()
#                 )
#             with col3:
#                 st.subheader("Physical Attributes")
#                 st.dataframe(
#                     st.session_state.selected_player.attributes.physical.model_dump()
#                 )
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.subheader("Gk Attributes")
#                 st.dataframe(
#                     st.session_state.selected_player.attributes.gk.model_dump()
#                 )
#             with col2:
#                 st.subheader("Intrinsic Attributes")
#                 st.dataframe(
#                     st.session_state.selected_player.attributes.intrinsic.model_dump()
#                 )
#         else:
#             st.warning("No players match your search criteria.")

with tabs[2]:  # Teams tab
    st.header("Team Management")
    teams = fetch_all_teams()

    if len(teams) > 0:
        team_table_df = {
            "Name": [],
            "League": [],
            "Budget": [],
            "Form": [],
            "Team Ability": [],
        }
        for team in teams:
            team_table_df["Name"].append(team.name)
            team_table_df["League"].append(team.league)
            team_table_df["Form"].append(team.current_form)
            team_table_df["Budget"].append(team.budget)
            team_table_df["Team Ability"].append(team.team_ability)

        team_table_df = pd.DataFrame(team_table_df)

        # Display the league table for the selected game week
        st.dataframe(team_table_df, use_container_width=True)
    else:
        st.warning("No teams found in the database.")
