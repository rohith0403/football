import copy
import numpy as np
import random


class League:
    def __init__(self, teams):
        self.teams = teams  # List of team names
        self.league_table = {team: {"points": 0, "goals_scored": 0, "goals_conceded": 0} for team in teams}
        self.history = []  # To store league table snapshots after each game week
        self.fixtures = self.create_fixtures()
    def calculate_adjusted_means(self,teamA, teamB, base_home_mean=1.7, base_away_mean=1.2, max_mean=3.0):
        # Calculate offense-defense differences
        home_offense_vs_away_defense = teamA.offense - teamB.defense
        away_offense_vs_home_defense = teamB.offense - teamA.defense
        
        # Nonlinear scaling for offense-defense difference
        home_scaling_factor = max(0.1, 1 + np.tanh(0.03 * home_offense_vs_away_defense))
        away_scaling_factor = max(0.1, 1 + np.tanh(0.03 * away_offense_vs_home_defense))
        
        # Closeness factor to reduce scoring for evenly matched teams
        closeness_factor = max(0.5, 1 - 0.02 * abs(teamA.offense - teamB.offense) - 0.02 * abs(teamA.defense - teamB.defense))
        
        # Adjust means with closeness and cap the maximum mean
        adjusted_home_mean = min(max_mean, max(0, base_home_mean * home_scaling_factor * closeness_factor))
        adjusted_away_mean = min(max_mean, max(0, base_away_mean * away_scaling_factor * closeness_factor))
        
        return adjusted_home_mean, adjusted_away_mean


    def predict_outcome(self, teamA, teamB):
        home_mean, away_mean = self.calculate_adjusted_means(teamA, teamB)
        home_goals = np.random.poisson(home_mean)
        away_goals = np.random.poisson(away_mean)
        if home_goals > away_goals:
            return [home_goals, away_goals]
        elif home_goals < away_goals:
            return [home_goals, away_goals]
        else:
            return [home_goals, away_goals]


    # Update scoreboard
    def play_match(self, team1, team2):
        """Simulate a match and return results (goals and points)."""
        goals_team1, goals_team2 = self.predict_outcome(team1, team2)

        # # Update goals scored and conceded
        # self.league_table[team1]["goals_scored"] += goals_team1
        # self.league_table[team1]["goals_conceded"] += goals_team2
        # self.league_table[team2]["goals_scored"] += goals_team2
        # self.league_table[team2]["goals_conceded"] += goals_team1

        team1.goals_for += goals_team1
        team1.goals_against += goals_team2
        team2.goals_for += goals_team2
        team2.goals_against += goals_team1

        # Assign points
        if goals_team1 > goals_team2:  # Team1 wins
            # self.league_table[team1]["points"] += 3
            team1.points += 3   
            team1.add_match_result('W')
            team2.add_match_result('L')
        elif goals_team1 < goals_team2:  # Team2 wins
            # self.league_table[team2]["points"] += 3
            team2.points += 3   
            team1.add_match_result('L')
            team2.add_match_result('W')
        else:  # Draw
            # self.league_table[team1]["points"] += 1
            # self.league_table[team2]["points"] += 1
            team1.points += 1   
            team2.points += 1
            team1.add_match_result('D')
            team2.add_match_result('D')

        team1.add_fixture(goals_team1, goals_team2, team2.name, 'H')
        team2.add_fixture(goals_team2, goals_team1, team1.name, 'A')
        self.update_league_table(team1)
        self.update_league_table(team2)

    def update_league_table(self, team):
        """Update the league table with current points and goal statistics."""
        self.league_table[team] = {
            "points": team.points,
            "goals_scored": team.goals_for,
            "goals_conceded": team.goals_against
    }

    def generate_fixtures(self):
        """
        Generate a round-robin schedule for a given list of teams,
        ensuring each team plays every other team twice (home and away).

        Returns:
            list: A list where each round contains the match fixtures.
        """
        random.shuffle(self.teams)  # Shuffle teams for random fixture generation
        num_teams = len(self.teams)
        schedule = []

        # Generate home and away fixtures by pairing teams
        for round_num in range(num_teams - 1):
            round_matches = []
            for i in range(num_teams // 2):
                home = self.teams[i]
                away = self.teams[num_teams - 1 - i]
                round_matches.append((home, away))
            schedule.append(round_matches)
            # Rotate teams to create the next round's matches
            self.teams = [self.teams[0]] + [self.teams[-1]] + self.teams[1:-1]

        # Duplicate the schedule to create home and away fixtures
        return schedule + [list(reversed(round)) for round in schedule]

    def balance_home_away(self, schedule):
        """
        Balances home and away fixtures for fairness.

        Args:
            schedule (list): List of rounds with fixtures.

        Returns:
            list: Balanced schedule with alternating home and away games.
        """
        balanced_schedule = []
        for i, round_matches in enumerate(schedule):
            if i % 2 == 0:
                balanced_schedule.append(round_matches)
            else:
                # Swap home and away teams for alternating rounds
                balanced_schedule.append([(away, home) for home, away in round_matches])
        return balanced_schedule
    
    def create_fixtures(self):
        # Generate initial schedule
        raw_schedule = self.generate_fixtures()

        # Balance home and away fixtures
        final_schedule = self.balance_home_away(raw_schedule)
        return final_schedule

    def play_game_week(self):
        """Simulate one game week."""
        game_week_fixtures = self.fixtures[0]  # The first round's fixtures
        for match in game_week_fixtures:
            self.play_match(*match)
        # Remove the fixtures that were played
        self.fixtures = self.fixtures[1:]

        # Store a snapshot of the league table
        self.history.append(copy.deepcopy(self.league_table))

    def run_season(self):
        """Run a full season."""
        while self.fixtures:
            self.play_game_week()
    
    def get_league_history(self):
        """Return the league table snapshots after each game week."""
        return self.history
    