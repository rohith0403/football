"""Team class"""


class Team:
    """
    Team class
    """

    def __init__(
        self,
        name,
        league,
        budget=2500,
        stats=None,
        current_form=None,
        roster=None,
    ):
        """
        Initialize a team with a name, ability, and recent form.

        :param name: str, the name of the team
        :param ability: int, the ability of the team (1-100)
        :param form: list[str], the recent form of the team (e.g., ['W', 'D', 'L', 'W', 'L'])
        """
        self.name = name
        self.league = league
        self.budget = budget
        self.current_form = current_form if current_form else []
        self.stats = stats if stats else {}  # dict with stats
        self.roster = roster if roster else []
        self.team_ability = self.calculate_ability()

    def calculate_ability(self):
        """
        Calculate the team's ability based on stats.

        Returns:
            float: The team's ability.
        """
        return 0.0

    # def form_factor(self):
    #     """
    #     Calculate the influence of form on the team's performance.
    #     A good form (more 'W') increases the team's strength.

    #     Returns:
    #         float: A multiplier for the team's performance.
    #     """
    #     if not self.form:
    #         return 1.0  # Neutral factor if no form data exists

    #     # Calculate form score: +2 for 'W', -1 for 'L', 0 for 'D'
    #     form_score = sum(
    #         2 if result == "W" else -1 if result == "L" else 0 for result in self.form
    #     )

    #     # Normalize form factor: range ~ [0.9, 1.2]
    #     return 1 + 0.01 * form_score

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
