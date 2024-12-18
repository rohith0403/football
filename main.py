import streamlit as st
from classes.Team import Team
from classes.League import League

liverpool = Team('Liverpool', 82.9, 99.0)
chelsea = Team('Chelsea', 99.0, 67.7)
arsenal = Team('Arsenal', 77.6, 85.8)
nottingham_forest = Team('Nottingham Forest', 56.2, 67.7)
manchester_city = Team('Manchester City', 74.9, 56.0)
afc_bournemouth = Team('AFC Bournemouth', 64.2, 61.3)
aston_villa = Team('Aston Villa', 64.2, 51.5)
fulham = Team('Fulham', 64.2, 58.5)
brighton = Team('Brighton & Hove Albion', 69.6, 51.5)
tottenham_hotspur = Team('Tottenham Hotspur', 96.3, 67.7)
brentford = Team('Brentford', 85.6, 42.9)
newcastle_united = Team('Newcastle United', 61.5, 61.3)
manchester_united = Team('Manchester United', 56.2, 67.7)
west_ham_united = Team('West Ham United', 56.2, 44.4)
crystal_palace = Team('Crystal Palace', 45.5, 61.3)
everton = Team('Everton', 37.5, 61.3)
luton_town = Team('Luton Town', 32.1, 64.4)
ipswich_town = Team('Ipswich Town', 40.1, 46.0)
wolverhampton_wanderers = Team('Wolverhampton Wanderers', 37.5, 44.4)
southampton = Team('Southampton', 26.8, 35.8)


teams = [
liverpool,
chelsea,
arsenal,
nottingham_forest,
manchester_city,
afc_bournemouth,
aston_villa,
fulham,
brighton,
tottenham_hotspur,
brentford,
newcastle_united,
manchester_united,
west_ham_united,
crystal_palace,
everton,
luton_town,
ipswich_town,
wolverhampton_wanderers,
southampton,
]


# Initialize Streamlit app
st.title("Football League Simulation")

# Initialize League only once
if 'league' not in st.session_state:
    st.session_state.league = League(teams)

# Run season button (this will only run once when clicked)
if 'season_run' not in st.session_state:
    st.session_state.season_run = False

if st.button("Run Full Season") and not st.session_state.season_run:
    st.session_state.league.run_season()  # Run the season and store results in session state
    st.session_state.season_run = True  # Mark the season as run to prevent rerun

# Display the final league table as an interactive table
if st.session_state.season_run:
    st.subheader("Final League Table")
    
    # Add a slider to select the game week
    total_gameweeks = len(st.session_state.league.history)
    gameweek_slider = st.slider(
        "Select Game Week",
        min_value=1,
        max_value=total_gameweeks,
        value=total_gameweeks,
        step=1,
        format="Game Week %d"
    )

    # Get the selected game week snapshot
    selected_week_snapshot = st.session_state.league.history[gameweek_slider - 1]  # Slider is 1-indexed

    # Prepare the data for the league table
    league_table_df = {
        "Team": [],
        "Points": [],
        "Goals Scored": [],
        "Goals Conceded": [],
        "Last Five": []
    }

    for team, stats in selected_week_snapshot.items():
        league_table_df["Team"].append(team.name)
        league_table_df["Points"].append(stats["points"])
        league_table_df["Goals Scored"].append(stats["goals_scored"])
        league_table_df["Goals Conceded"].append(stats["goals_conceded"])
        league_table_df["Last Five"].append(team.last_five)

    # Display the league table for the selected game week
    st.dataframe(league_table_df)

else:
    st.write("Click 'Run Full Season' to start the simulation.")