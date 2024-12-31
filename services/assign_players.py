# import random

# from classes.Player import Player
# from classes.Team import Team
from db.store import (
    fetch_players_from_pool,
    fetch_season_id,
    fetch_teams_from_season_table,
)

# Define the required positions and their counts
required_positions = {
    "GK": 2,
    "CB": 2,
    "FB": 2,
    "DM": 1,
    "HM": 1,
    "CAM": 1,
    "Winger": 2,
    "ST": 1,
}


# Function to assign players to teams
def assign_players_to_teams():
    """Assign players to teams based on required positions."""
    season_id = fetch_season_id()
    # Fetch teams from the season table
    teams = fetch_teams_from_season_table(season_id)

    # Fetch all players
    players = fetch_players_from_pool()
    available_players = [player for player in players if player.team_id is None]
    for team in teams:
        team_players = []
        position_counts = {pos: 0 for pos in required_positions}

        for player in available_players:
            if len(team_players) >= 25:
                break

            if position_counts[player.position] < required_positions.get(
                player.position, 0
            ):
                team_players.append(player)
                position_counts[player.position] += 1
                player.team_id = team.id

        if len(team_players) < 25:
            print(f"Not enough players to fill team {team.name}")
            continue

        team.players = team_players
        session.add(team)
        session.commit()


if __name__ == "__main__":
    assign_players_to_teams()
    print("Players have been assigned to teams.")
