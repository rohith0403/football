import random

from db.store import (
    fetch_players_from_pool,
    fetch_season_id,
    fetch_teams_from_season_table,
    update_players_team,
    update_teams_in_season_table,
)


def initialize_players_to_teams():
    """Raddomly assign players to teams"""
    required_positions = {
        'GK': 2,
        'CB': 2,
        'FB': 2,
        'DM': 1,
        'HM': 1,
        'CAM': 1,
        'Winger': 2,
        'ST': 1
    }
    current_season_id = fetch_season_id()
    players = fetch_players_from_pool()
    teams = fetch_teams_from_season_table(current_season_id)
    assigned_players = []
    for team in teams:
        if len(team.roster) < 25:
            for player in players:
                if player.team is None:
                    if len(team.roster) >= 25:
                        break
                    if required_positions.get(player.position, 0) > 0:
                        team.buy_player(player, 0)
                        player.assign_team(team)
                        required_positions[player.position] -= 1
                    assigned_players.append(player)
 
            # Fill remaining spots with any position
            while len(team.roster) < 25:
                player = players[random.randint(0, len(players) - 1)]
                if player.team is None:
                    team.buy_player(player, 0)
                    player.assign_team(team)
                    assigned_players.append(player)

    update_teams_in_season_table(teams, current_season_id)
    update_players_team(assigned_players)