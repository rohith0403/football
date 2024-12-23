from classes.Team import Team
from db.store import create_new_season, save_teams_to_season_table


def initialize_teams():
    """
    Initialize teams
    """
    teams = [
        Team("liverpool", "Liverpool", 82.9, 99.0),
        Team("chelsea", "Chelsea", 99.0, 67.7),
        Team("arsenal", "Arsenal", 77.6, 85.8),
        Team("nottingham_forest", "Nottingham Forest", 56.2, 67.7),
        Team("manchester_city", "Manchester City", 74.9, 56.0),
        Team("afc_bournemouth", "AFC Bournemouth", 64.2, 61.3),
        Team("aston_villa", "Aston Villa", 64.2, 51.5),
        Team("fulham", "Fulham", 64.2, 58.5),
        Team("brighton", "Brighton & Hove Albion", 69.6, 51.5),
        Team("tottenham_hotspur", "Tottenham Hotspur", 96.3, 67.7),
        Team("brentford", "Brentford", 85.6, 42.9),
        Team("newcastle_united", "Newcastle United", 61.5, 61.3),
        Team("manchester_united", "Manchester United", 56.2, 67.7),
        Team("west_ham_united", "West Ham United", 56.2, 44.4),
        Team("crystal_palace", "Crystal Palace", 45.5, 61.3),
        Team("everton", "Everton", 37.5, 61.3),
        Team("luton_town", "Luton Town", 32.1, 64.4),
        Team("ipswich_town", "Ipswich Town", 40.1, 46.0),
        Team("wolverhampton_wanderers", "Wolverhampton Wanderers", 37.5, 44.4),
        Team("southampton", "Southampton", 26.8, 35.8),
    ]

    # Create a new season and get the season ID
    season_id = create_new_season()

    # Save teams to the season-specific table
    save_teams_to_season_table(teams, season_id)

    print(
        f"Teams have been successfully stored in the database for season {season_id}."
    )


# Example usage
if __name__ == "__main__":
    initialize_teams()
