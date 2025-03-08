import random

import numpy as np
from scipy.stats import poisson

from classes.Team import Team

# from db.store import save_league_history_to_season_table, update_teams_in_season_table


class League:
    """
    Represents a football league with teams, fixtures, and results.

    Attributes:
        teams (list): List of Team objects in the league.
        league_table (list): Sorted list of teams in the league table.
        fixtures (list): List of scheduled fixtures.
    """

    def __init__(self, name, country, tier, teams=None):
        """
        Initializes the League with a list of teams.

        Args:
            teams (list): List of Team objects.
        """
        self.name = name
        self.country = country
        self.tier = tier
        self.teams = teams if teams else []
        # self.league_table = sorted(teams, key=lambda team: team.name)
        self.fixtures = self.create_fixtures()

    def simulate_match(self, team_a: Team, team_b: Team, season_id: int):
        """Simulate a match between two teams and display the results."""
        team_a_offense, team_a_defense = team_a.calculate_team_strength()
        team_b_offense, team_b_defense = team_b.calculate_team_strength()

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

        for team in [team_a, team_b]:
            for player in team.players:
                if player.role == "Goalkeeper":
                    player.saves += random.randint(1, 5)  # Random saves for goalkeepers
                    player.rating += player.saves * 0.1

        # Update team_a stats
        team_a.stats[season_id - 1][f"season {season_id}"].goals_scored += goals_a
        team_a.stats[season_id - 1][f"season {season_id}"].goals_against += goals_b
        team_a.stats[season_id - 1][f"season {season_id}"].goal_difference += (
            goals_a - goals_b
        )
        team_a.update_matches_played("H", team_b.name, goals_a, goals_b)
        # Update team_b stats
        team_b.stats[season_id - 1][f"season {season_id}"].goals_scored += goals_b
        team_b.stats[season_id - 1][f"season {season_id}"].goals_against += goals_a
        team_b.stats[season_id - 1][f"season {season_id}"].goal_difference += (
            goals_b - goals_a
        )
        team_b.update_matches_played("A", team_a.name, goals_b, goals_a)

        for team in [team_a, team_b]:
            self.normalize_ratings(team.get_players())

    def normalize_ratings(self, players):
        """Assign ratings to players based on the team's and player performance."""
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

    def generate_fixtures(self):
        """
        Generates a round-robin schedule for the league.

        Returns:
            list: List of fixtures.
        """
        random.shuffle(self.teams)
        num_teams = len(self.teams)
        schedule = []

        for _ in range(num_teams - 1):
            matches = [
                (self.teams[i], self.teams[num_teams - 1 - i])
                for i in range(num_teams // 2)
            ]
            schedule.append(matches)
            self.teams = [self.teams[0]] + self.teams[-1:] + self.teams[1:-1]

        return schedule + [list(reversed(round_matches)) for round_matches in schedule]

    def balance_home_away(self, schedule):
        """
        Balances home and away matches in the schedule.

        Args:
            schedule (list): Raw schedule.

        Returns:
            list: Balanced schedule.
        """
        return [
            (
                round_matches
                if i % 2 == 0
                else [(away, home) for home, away in round_matches]
            )
            for i, round_matches in enumerate(schedule)
        ]

    def create_fixtures(self):
        """
        Creates a balanced fixture schedule.

        Returns:
            list: Balanced fixtures.
        """
        raw_schedule = self.generate_fixtures()
        return self.balance_home_away(raw_schedule)

    def play_game_week(self, season_id):
        """
        Plays a single game week and updates league history.

        Args:
            season_id (int): The ID of the current season.
        """
        game_week_fixtures = self.fixtures.pop(0)
        for home, away in game_week_fixtures:
            # self.play_match(home, away)
            self.simulate_match(home, away, season_id)

        # league_snapshot = [team.to_dict() for team in self.teams]
        # save_league_history_to_season_table(league_snapshot, season_id)

    def run_season(self, season_id):
        """
        Runs the full league season, playing all fixtures.

        Args:
            season_id (int): The ID of the current season.
        """
        while self.fixtures:
            self.play_game_week(season_id)
        self.allot_prize_money()
        # update_teams_in_season_table(self.teams, season_id)

    def allot_prize_money(self):
        """
        Allot prize money after each season
        """
        (self.teams).sort(key=lambda team: team.points, reverse=True)
        (self.teams)[0].budget += 100
        (self.teams)[1].budget += 80
        (self.teams)[2].budget += 70
        (self.teams)[3].budget += 60
        (self.teams)[4].budget += 50
        (self.teams)[5].budget += 50
        (self.teams)[6].budget += 50
        (self.teams)[7].budget += 50
        (self.teams)[8].budget += 50
        (self.teams)[9].budget += 50
        (self.teams)[10].budget += 40
        (self.teams)[11].budget += 40
        (self.teams)[12].budget += 40
        (self.teams)[13].budget += 40
        (self.teams)[14].budget += 30
        (self.teams)[15].budget += 30
        (self.teams)[16].budget += 30
        (self.teams)[17].budget += 30

    # def display_results(self, team_a, team_b, events):
    #     """Display the match results and player performances."""
    #     print(
    #         f"Final Score: {team_a.name} {team_a.score} - {team_b.score} {team_b.name}"
    #     )
    #     print(f"xG: {team_a.name}: {team_a.xg:.2f}, {team_b.name}: {team_b.xg:.2f}\n")

    #     for team in [team_a, team_b]:
    #         print(f"Team: {team.name}")
    #         man_of_the_match = max(team.players, key=lambda p: p.rating)
    #         print(
    #             f"  Man of the Match: {man_of_the_match.name} ({man_of_the_match.role}) - Rating: {man_of_the_match.rating:.2f}"
    #         )
    #         for player in team.players:
    #             print(
    #                 f"  {player.name} ({player.role}) - Rating: {player.rating:.2f}, Shots: {player.shots}, Assists: {player.assists}, Saves: {player.saves if player.role == 'Goalkeeper' else 'N/A'}"
    #             )
    #     print("\nMatch Events:")
    #     for event in events:
    #         print(f"Minute {event[0]}: {event[1]}")
