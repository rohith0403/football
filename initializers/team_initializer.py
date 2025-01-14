from classes.Team import Team
from db.store import insert_player, insert_team
from initializers.player_initializer import generate_player


def generate_roster():
    """
    Generate a roster of 25 players with specific positions.
    """
    roster = []

    # Generate required players for each position
    positions = {
        "Goalkeeper (GK)": 2,
        "Center Back (CB)": 2,
        "Full Back (FB)": 2,
        "Defensive Midfielder (DM)": 1,
        "Holding Midfielder": 1,
        "Attacking Midfielder (CAM)": 1,
        "Winger": 2,
        "Striker": 1,
    }

    # Generate players for each required position
    for position, count in positions.items():
        for _ in range(count):
            player = generate_player()
            player.position = position
            roster.append(player)

    # Generate remaining players to fill the roster to 25
    while len(roster) < 25:
        player = generate_player()
        roster.append(player)

    return roster


def initialize_premier_league():
    """
    Initialize teams
    """
    team_names = [
        "Liverpool",
        "Chelsea",
        "Arsenal",
        "Nottingham Forest",
        "Manchester City",
        "AFC Bournemouth",
        "Aston Villa",
        "Fulham",
        "Brighton & Hove Albion",
        "Tottenham Hotspur",
        "Brentford",
        "Newcastle United",
        "Manchester United",
        "West Ham United",
        "Crystal Palace",
        "Everton",
        "Luton Town",
        "Ipswich Town",
        "Wolverhampton Wanderers",
        "Southampton",
    ]
    league_name = "Premier League"

    for team_name in team_names:
        roster = generate_roster()
        uid_list = []
        for player in roster:
            player.team = team_name
            player.league = league_name
            uid_list.append(player.uid)
            insert_player(player)
        team = Team(team_name, league_name, roster=uid_list)
        team.calculate_ability(roster)
        insert_team(team)
