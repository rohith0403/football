"""Team class"""

import importlib
import random


class Team:
    """
    Team class
    """

    def __init__(
        self,
        name,
        league,
        budget=100,
        current_form=None,
        roster=None,
        manager="",
        formation=None,
    ):
        """
        Initialize a team
        """
        self.name = name
        self.league = league
        self.budget = budget
        self.current_form = current_form if current_form else []
        self.stats = self.initialize_stats(1)
        self.roster = roster if roster is not None else []
        self.manager = manager
        self.formation = formation
        self.matches_played = {}
        self.offense, self.defense = self.calculate_team_strength()

    def get_players(self):
        """Get players from roster"""
        store = importlib.import_module("db.store")
        players = [store.fetch_player_by_id(player_id) for player_id in self.roster]
        return players

    def get_random_player(self, position=None):
        """Get a random player from the team"""
        players = self.get_players()
        if position:
            candidates = [p for p in players if p.position == position]
            return random.choice(candidates)
        return random.choice(players)

    def calculate_team_strength(self):
        """Calculate offense and defence of the team from player attributes"""
        players = self.get_players()
        offense = (
            sum(
                player.attributes.technical.Finishing
                for player in players
                if player.position != "GK"
            )
            + 0.6
            * sum(
                player.attributes.technical.Passing
                for player in players
                if player.position != "GK"
            )
            + 0.3
            * sum(
                player.attributes.technical.Long_Shots
                for player in players
                if player.position != "GK"
            )
            + 0.4
            * sum(
                player.attributes.technical.Heading
                for player in players
                if player.position != "GK"
            )
            + 0.4
            * sum(
                player.attributes.technical.Crossing
                for player in players
                if player.position != "GK"
            )
            + 0.4
            * sum(
                player.attributes.technical.Dribbling
                for player in players
                if player.position != "GK"
            )
            / len(players)
        )
        defense = (
            sum(
                player.attributes.technical.Tackling
                for player in players
                if player.position != "GK"
            )
            + 0.6
            * sum(
                player.attributes.technical.Marking
                for player in players
                if player.position != "GK"
            )
            + 0.4
            * sum(
                player.attributes.technical.Heading
                for player in players
                if player.position != "GK"
            )
            + 0.4
            * sum(
                player.attributes.mental.Composure
                for player in players
                if player.position != "GK"
            )
            / len(players)
        )

        # form_factor = sum(team.current_form) / len(team.current_form)
        # return offense * (form_factor / 10), defense * (form_factor / 10)
        form_factor = self.form_factor()
        return offense * form_factor, defense * form_factor

    def form_factor(self):
        """
        Calculate the influence of form on the team's performance.
        A good form (more 'W') increases the team's strength.

        Returns:
            float: A multiplier for the team's performance.
        """
        if not self.current_form:
            return 1.0  # Neutral factor if no form data exists

        # Calculate form score: +2 for 'W', -1 for 'L', 0 for 'D'
        form_score = sum(
            2 if result == "W" else -1 if result == "L" else 0
            for result in self.current_form
        )

        # Normalize form factor: range ~ [0.9, 1.2]
        return 1 + 0.01 * form_score

    def initialize_stats(self, season_id):
        """Initialize stats for the team"""
        return [
            {
                f"season {season_id}": {
                    "matches_played": 0,
                    "points": 0,
                    "wins": 0,
                    "draws": 0,
                    "losses": 0,
                    "goals_scored": 0,
                    "goals_against": 0,
                    "goal_difference": 0,
                }
            }
        ]

    def update_matches_played(self, h_or_a, opponent, scored, against):
        """Update matches played for the team"""
        if opponent in self.matches_played:
            self.matches_played[opponent].append([h_or_a, opponent, scored, against])

    def get_form_against_team(self, opponent):
        """Get form against a particular team"""
        form_against_team = []
        if opponent in self.matches_played:
            if len(self.matches_played[opponent]) > 5:
                for fixture in self.matches_played[opponent][-5:]:
                    if fixture[2] > fixture[3]:
                        form_against_team.append("W")
                    elif fixture[2] < fixture[3]:
                        form_against_team.append("L")
                    else:
                        form_against_team.append("D")
            else:
                for fixture in self.matches_played[opponent]:
                    if fixture[2] > fixture[3]:
                        form_against_team.append("W")
                    elif fixture[2] < fixture[3]:
                        form_against_team.append("L")
                    else:
                        form_against_team.append("D")

    # def add_match_result(self, result):
    #     """
    #     Adds match result to form
    #     """
    #     self.form.append(result)
    #     if len(self.form) > 5:
    #         self.form = self.form[1:]

    # def add_fixture(self, scored, against, opponent, place):
    #     """
    #     Add played fixtures to fixtures played
    #     """
    #     self.fixtures_played.append([scored, against, opponent, place])

    # def return_recent_fixture(self):
    #     """
    #     Return the most recent fixture's result as a formatted string.

    #     :return: str, formatted recent fixture or a message if no fixtures played
    #     """
    #     if not self.fixtures_played:
    #         return f"No fixtures played for {self.name} yet."

    #     scored, against, opponent, place = self.fixtures_played[-1]
    #     if place == "H":
    #         return f"{self.name}   {scored}  -  {against}   {opponent}"
    #     elif place == "A":
    #         return f"{opponent}   {against}  -  {scored}   {self.name}"

    # def assign_player(self, player):
    #     """Called when a player is assigned to this team"""
    #     self.roster.append(player)

    # def buy_player(self, player, price):
    #     """Buying a player"""
    #     if player.team:
    #         selling_team = player.team
    #         selling_team.budget += price
    #     self.budget -= price
    #     self.assign_player(player)

    # def sell_player(self, player, price):
    #     """Selling a player"""
    #     if player.team:
    #         selling_team = player.team
    #         selling_team.budget += price
    #     self.budget -= price
    #     self.assign_player(player)

    # def to_dict(self):
    #     """Convert self to dict object"""
    #     return {
    #         "name": self.name,
    #         "points": self.points,
    #         "wins": self.wins,
    #         "draws": self.draws,
    #         "losses": self.losses,
    #         "goals_scored": self.goals_scored,
    #         "goals_against": self.goals_against,
    #         "goal_difference": self.goals_scored - self.goals_against,
    #         "form": self.form,
    #         "fixtures_played": self.fixtures_played,
    #         "budget": self.budget,
    #     }
