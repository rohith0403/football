from classes.Team import Team
from db.store import insert_team


def initialize_teams():
    """
    Initialize teams
    """
    teams = [
        Team("Liverpool", "Premier League"),
        Team("Chelsea", "Premier League"),
        Team("Arsenal", "Premier League"),
        Team("Nottingham Forest", "Premier League"),
        Team("Manchester City", "Premier League"),
        Team("AFC Bournemouth", "Premier League"),
        Team("Aston Villa", "Premier League"),
        Team("Fulham", "Premier League"),
        Team("Brighton & Hove Albion", "Premier League"),
        Team("Tottenham Hotspur", "Premier League"),
        Team("Brentford", "Premier League"),
        Team("Newcastle United", "Premier League"),
        Team("Manchester United", "Premier League"),
        Team("West Ham United", "Premier League"),
        Team("Crystal Palace", "Premier League"),
        Team("Everton", "Premier League"),
        Team("Luton Town", "Premier League"),
        Team("Ipswich Town", "Premier League"),
        Team("Wolverhampton Wanderers", "Premier League"),
        Team("Southampton", "Premier League"),
    ]

    for team in teams:
        insert_team(team)
