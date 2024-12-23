import random

import numpy as np

from db.store import save_league_history_to_season_table, update_teams_in_season_table


def team_to_dict(team):
    """
    Converts a Team object to a dictionary representation.

    Args:
        team (Team): A team object.

    Returns:
        dict: A dictionary containing team attributes.
    """
    return {
        "name": team.name,
        "points": team.points,
        "wins": team.wins,
        "draws": team.draws,
        "losses": team.losses,
        "goals_scored": team.goals_scored,
        "goals_against": team.goals_against,
        "goal_difference": team.goals_scored - team.goals_against,
        "form": team.form,
        "fixtures_played": team.fixtures_played,
        "budget": team.budget,
    }


class League:
    """
    Represents a football league with teams, fixtures, and results.

    Attributes:
        teams (list): List of Team objects in the league.
        league_table (list): Sorted list of teams in the league table.
        fixtures (list): List of scheduled fixtures.
    """

    def __init__(self, teams):
        """
        Initializes the League with a list of teams.

        Args:
            teams (list): List of Team objects.
        """
        self.teams = teams
        self.league_table = sorted(teams, key=lambda team: team.name)
        self.fixtures = self.create_fixtures()

    @staticmethod
    def calculate_adjusted_means(
        team_a, team_b, base_home_mean=1.7, base_away_mean=1.2, max_mean=3.0
    ):
        """
        Calculates adjusted mean goals for home and away teams.

        Args:
            team_a (Team): Home team.
            team_b (Team): Away team.
            base_home_mean (float): Base mean for home goals.
            base_away_mean (float): Base mean for away goals.
            max_mean (float): Maximum allowed mean value.

        Returns:
            tuple: Adjusted means for home and away goals.
        """
        home_vs_away = team_a.offense - team_b.defense
        away_vs_home = team_b.offense - team_a.defense

        home_factor = max(0.1, 1 + np.tanh(0.03 * home_vs_away))
        away_factor = max(0.1, 1 + np.tanh(0.03 * away_vs_home))

        closeness = max(
            0.5,
            1
            - 0.02 * abs(team_a.offense - team_b.offense)
            - 0.02 * abs(team_a.defense - team_b.defense),
        )

        home_mean = min(max_mean, base_home_mean * home_factor * closeness)
        away_mean = min(max_mean, base_away_mean * away_factor * closeness)

        return home_mean, away_mean

    def predict_outcome(self, team_a, team_b):
        """
        Predicts the match outcome between two teams.

        Args:
            team_a (Team): Home team.
            team_b (Team): Away team.

        Returns:
            tuple: Predicted goals for home and away teams.
        """
        home_mean, away_mean = self.calculate_adjusted_means(team_a, team_b)
        return np.random.poisson(home_mean), np.random.poisson(away_mean)

    def play_match(self, team1, team2):
        """
        Plays a match between two teams and updates their stats.

        Args:
            team1 (Team): First team (home).
            team2 (Team): Second team (away).
        """
        goals_team1, goals_team2 = self.predict_outcome(team1, team2)

        # Update team stats
        team1.goals_scored += goals_team1
        team1.goals_against += goals_team2
        team2.goals_scored += goals_team2
        team2.goals_against += goals_team1

        # Assign points
        if goals_team1 > goals_team2:  # Team1 wins
            team1.points += 3
            team1.add_match_result("W")
            team2.add_match_result("L")
            team1.wins += 1
            team2.losses += 1
        elif goals_team1 < goals_team2:  # Team2 wins
            team2.points += 3
            team1.add_match_result("L")
            team2.add_match_result("W")
            team1.losses += 1
            team2.wins += 1
        else:  # Draw
            team1.points += 1
            team2.points += 1
            team1.add_match_result("D")
            team2.add_match_result("D")
            team1.draws += 1
            team2.draws += 1

        team1.add_fixture(goals_team1, goals_team2, team2.name, "H")
        team2.add_fixture(goals_team2, goals_team1, team1.name, "A")

    def generate_fixtures(self):
        """
        Generates a round-robin schedule for the league.

        Returns:
            list: List of fixtures.
        """
        random.shuffle(self.teams)
        num_teams = len(self.teams)
        schedule = []

        for round_num in range(num_teams - 1):
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
            self.play_match(home, away)

        league_snapshot = [team_to_dict(team) for team in self.teams]
        save_league_history_to_season_table(league_snapshot, season_id)

    def run_season(self, season_id):
        """
        Runs the full league season, playing all fixtures.

        Args:
            season_id (int): The ID of the current season.
        """
        while self.fixtures:
            self.play_game_week(season_id)
        self.allot_prize_money()
        update_teams_in_season_table(self.teams, season_id)

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
