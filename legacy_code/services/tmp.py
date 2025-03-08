import numpy as np


def calculate_goals_conceded_per_match(team, max_goals=4, min_goals=1.5):
    """
    Calculate the number of goals a team is likely to concede per match based on their defense.

    Args:
        team (Team): The team whose goals conceded are calculated.
        max_goals (float): Maximum goals a team could concede in an average match.
        min_goals (float): Minimum expected goals conceded per match to avoid very low totals.

    Returns:
        float: Adjusted expected goals conceded per match.
    """
    # Scaling based on defense rating:
    # - Teams with higher defense should concede fewer goals.
    # - Low defense (below 50) will concede more goals.
    # - High defense (above 75) will concede fewer goals.

    defense_rating = team.defense

    # Linear scaling of defense rating to goals conceded per match
    if defense_rating < 50:
        # Poor defense -> more goals conceded per match
        goals_conceded = 3.5 + (50 - defense_rating) * 0.07  # High goals conceded
    elif defense_rating > 75:
        # Strong defense -> fewer goals conceded per match
        goals_conceded = 1.5 + (100 - defense_rating) * 0.03  # Low goals conceded
    else:
        # Average defense -> moderate goals conceded per match
        goals_conceded = 2.5 + (75 - defense_rating) * 0.04  # Middle goals conceded

    # Constrain the value to a reasonable range
    goals_conceded = max(min_goals, min(max_goals, goals_conceded))

    return goals_conceded


def simulate_season(team, num_games=38):
    """
    Simulate the season for a team and calculate total goals conceded.

    Args:
        team (Team): The team whose season is being simulated.
        num_games (int): Number of games to simulate in a season.

    Returns:
        int: Total goals conceded by the team in the season.
    """
    total_goals_conceded = 0

    for _ in range(num_games):
        goals_conceded_per_match = calculate_goals_conceded_per_match(team)
        total_goals_conceded += np.random.poisson(goals_conceded_per_match)

    return total_goals_conceded


# Define Team class
class Team:
    def __init__(self, name, offense, defense):
        self.name = name
        self.offense = offense
        self.defense = defense


# Example teams
team1 = Team(name="Team A", offense=80, defense=90)  # Strong defense
team2 = Team(name="Team B", offense=75, defense=60)  # Average defense
team3 = Team(name="Team C", offense=70, defense=40)  # Weak defense

# Simulate season and print results
for team in [team1, team2, team3]:
    goals_conceded = simulate_season(team)
    print(f"{team.name} conceded {goals_conceded} goals in the season.")
