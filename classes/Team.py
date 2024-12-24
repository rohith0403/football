class Team:
    """
    Team class
    """

    def __init__(
        self,
        variable_name,
        name,
        offense,
        defense,
        points=0,
        wins=0,
        draws=0,
        losses=0,
        goals_scored=0,
        goals_against=0,
        form=[],
        fixtures_played=[],
        budget=100,
    ):
        """
        Initialize a team with a name, ability, and recent form.

        :param name: str, the name of the team
        :param ability: int, the ability of the team (1-100)
        :param form: list[str], the recent form of the team (e.g., ['W', 'D', 'L', 'W', 'L'])
        """
        self.variable_name = variable_name
        self.name = name
        self.offense = offense
        self.defense = defense
        self.form = form
        self.points = points
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.goals_scored = goals_scored
        self.goals_against = goals_against
        self.fixtures_played = fixtures_played
        self.budget = budget

    def __repr__(self):
        return f"Team(name={self.name}, offense={self.offense}, defense = {self.defense}, form={self.form})"

    def form_factor(self):
        """
        Calculate the influence of form on the team's performance.
        A good form (more 'W') increases the team's strength.

        Returns:
            float: A multiplier for the team's performance.
        """
        if not self.form:
            return 1.0  # Neutral factor if no form data exists

        # Calculate form score: +2 for 'W', -1 for 'L', 0 for 'D'
        form_score = sum(
            2 if result == "W" else -1 if result == "L" else 0 for result in self.form
        )

        # Normalize form factor: range ~ [0.9, 1.2]
        return 1 + 0.01 * form_score

    def add_match_result(self, result):
        """
        Adds match result to form
        """
        self.form.append(result)
        if len(self.form) > 5:
            self.form = self.form[1:]

    def add_fixture(self, scored, against, opponent, place):
        """
        Add played fixtures to fixtures played
        """
        self.fixtures_played.append([scored, against, opponent, place])

    def return_recent_fixture(self):
        """
        Return the most recent fixture's result as a formatted string.

        :return: str, formatted recent fixture or a message if no fixtures played
        """
        if not self.fixtures_played:
            return f"No fixtures played for {self.name} yet."

        scored, against, opponent, place = self.fixtures_played[-1]
        if place == "H":
            return f"{self.name}   {scored}  -  {against}   {opponent}"
        elif place == "A":
            return f"{opponent}   {against}  -  {scored}   {self.name}"
