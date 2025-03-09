import random

import numpy as np
from scipy.stats import poisson


class Player:
    def __init__(self, name, role, overall_ability, recent_form=None):
        self.name = name
        self.role = role
        self.overall_ability = overall_ability  # Ratings between 1 and 10
        self.shooting = overall_ability * random.uniform(0.7, 1.0)
        self.passing = overall_ability * random.uniform(0.7, 1.0)
        self.dribbling = overall_ability * random.uniform(0.7, 1.0)
        self.defending = overall_ability * random.uniform(0.5, 0.9)
        self.goalkeeping = (
            overall_ability * random.uniform(0.4, 0.8) if role == "Goalkeeper" else 0
        )
        self.recent_form = (
            recent_form if recent_form else [random.randint(5, 10) for _ in range(5)]
        )
        self.rating = 0
        self.shots = 0
        self.saves = 0
        self.assists = 0


class Team:
    def __init__(self, name, players, current_form=None):
        self.name = name
        self.players = players
        self.score = 0
        self.xg = 0
        self.current_form = (
            current_form if current_form else [random.randint(5, 10) for _ in range(5)]
        )

    def get_random_player(self, role=None):
        if role:
            candidates = [p for p in self.players if p.role == role]
            return random.choice(candidates)
        return random.choice(self.players)


def calculate_team_strength(team):
    offense = sum(
        player.shooting for player in team.players if player.role != "Goalkeeper"
    ) / len(team.players)
    defense = sum(
        player.defending for player in team.players if player.role != "Goalkeeper"
    ) / len(team.players)
    form_factor = sum(team.current_form) / len(team.current_form)
    return offense * (form_factor / 10), defense * (form_factor / 10)


def normalize_ratings(players):
    min_rating = 1
    max_rating = 5

    base_ratings = [player.rating for player in players]
    min_base = min(base_ratings)
    max_base = max(base_ratings)

    for player in players:
        if max_base - min_base > 0:
            player.rating = min_rating + (player.rating - min_base) * (
                max_rating - min_rating
            ) / (max_base - min_base)
        else:
            player.rating = (min_rating + max_rating) / 2


def simulate_match(team_a, team_b, duration=90):
    events = []
    team_a_offense, team_a_defense = calculate_team_strength(team_a)
    team_b_offense, team_b_defense = calculate_team_strength(team_b)

    # Bivariate Poisson distribution to simulate goals
    lambda_a = max(0.1, team_a_offense - team_b_defense)
    lambda_b = max(0.1, team_b_offense - team_a_defense)

    goals_a = poisson.rvs(mu=lambda_a)
    goals_b = poisson.rvs(mu=lambda_b)

    team_a.score = goals_a
    team_b.score = goals_b

    # Simulate shots and xG contributions
    total_shots_a = random.randint(goals_a + 1, goals_a + 10)
    total_shots_b = random.randint(goals_b + 1, goals_b + 10)

    for _ in range(total_shots_a):
        xg_contribution = random.uniform(0.01, 0.99)
        team_a.xg += xg_contribution
        shooter = team_a.get_random_player()
        shooter.rating += xg_contribution * 0.1
        shooter.shots += 1

    for _ in range(total_shots_b):
        xg_contribution = random.uniform(0.01, 0.99)
        team_b.xg += xg_contribution
        shooter = team_b.get_random_player()
        shooter.rating += xg_contribution * 0.1
        shooter.shots += 1

    for _ in range(goals_a):
        scorer = team_a.get_random_player()
        assister = team_a.get_random_player()
        while assister == scorer:
            assister = team_a.get_random_player()
        scorer.rating += random.uniform(0.3, 0.5)
        scorer.shots += 1
        assister.assists += 1
        assister.rating += random.uniform(0.1, 0.3)
        for player in team_a.players:
            if player != scorer:
                player.rating += 0.1  # Increment for team effort
        events.append(
            (
                random.randint(1, duration),
                f"GOAL! {scorer.name} scored for {team_a.name}. Assist by {assister.name}.",
            )
        )

    for _ in range(goals_b):
        scorer = team_b.get_random_player()
        assister = team_b.get_random_player()
        while assister == scorer:
            assister = team_b.get_random_player()
        scorer.rating += random.uniform(0.3, 0.5)
        scorer.shots += 1
        assister.assists += 1
        assister.rating += random.uniform(0.1, 0.3)
        for player in team_b.players:
            if player != scorer:
                player.rating += 0.1
        events.append(
            (
                random.randint(1, duration),
                f"GOAL! {scorer.name} scored for {team_b.name}. Assist by {assister.name}.",
            )
        )

    for team in [team_a, team_b]:
        for player in team.players:
            if player.role == "Goalkeeper":
                player.saves += random.randint(1, 5)  # Random saves for goalkeepers
                player.rating += player.saves * 0.1

    for team in [team_a, team_b]:
        normalize_ratings(team.players)

    return sorted(events, key=lambda x: x[0])


def display_results(team_a, team_b, events):
    print(f"Final Score: {team_a.name} {team_a.score} - {team_b.score} {team_b.name}")
    print(f"xG: {team_a.name}: {team_a.xg:.2f}, {team_b.name}: {team_b.xg:.2f}\n")

    for team in [team_a, team_b]:
        print(f"Team: {team.name}")
        man_of_the_match = max(team.players, key=lambda p: p.rating)
        print(
            f"  Man of the Match: {man_of_the_match.name} ({man_of_the_match.role}) - Rating: {man_of_the_match.rating:.2f}"
        )
        for player in team.players:
            print(
                f"  {player.name} ({player.role}) - Rating: {player.rating:.2f}, Shots: {player.shots}, Assists: {player.assists}, Saves: {player.saves if player.role == 'Goalkeeper' else 'N/A'}"
            )
    print("\nMatch Events:")
    for event in events:
        print(f"Minute {event[0]}: {event[1]}")


# Example Usage
players_team_a = [
    Player(
        f"Player {i+1}",
        "Attacker" if i < 3 else "Midfielder" if i < 8 else "Defender",
        random.randint(1, 10),
    )
    for i in range(10)
]
players_team_b = [
    Player(
        f"Player {i+1}",
        "Attacker" if i < 3 else "Midfielder" if i < 8 else "Defender",
        random.randint(1, 10),
    )
    for i in range(10)
]

players_team_a.append(Player("Goalkeeper A", "Goalkeeper", 8))
players_team_b.append(Player("Goalkeeper B", "Goalkeeper", 8))

team_a = Team("Team A", players_team_a)
team_b = Team("Team B", players_team_b)

events = simulate_match(team_a, team_b)
display_results(team_a, team_b, events)
