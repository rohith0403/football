import streamlit as st

from db.store import create_tables, wipe_season_data
from initializers.league_initializer import initialize_league
from initializers.team_initializer import initialize_premier_league

st.title("Football Simulation")


# Function to refresh the database
def initialize_db():
    """Initialize Database"""
    wipe_season_data()
    create_tables()
    initialize_league()
    initialize_premier_league()


if st.button("Initialize DB"):
    initialize_db()
    st.session_state.clear()  # Clear session state to reset the app
    st.success("Database Initialized.")
