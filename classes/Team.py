class Team:
    def __init__(self, name, offense, defense):
        """
        Initialize a team with a name, ability, and recent form.

        :param name: str, the name of the team
        :param ability: int, the ability of the team (1-100)
        :param last_five: list[str], the recent form of the team (e.g., ['W', 'D', 'L', 'W', 'L'])
        """
        self.name = name
        self.offense = offense
        self.defense = defense
        self.last_five = []
        self.games_played = 0
        self.points = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0

    def __repr__(self):
        return f"Team(name={self.name}, offense={self.offense}, defense = {self.defense}, last_five={self.last_five})"
    
    def add_match_result(self, result):
        self.last_five.append(result)
        if len(self.last_five) > 5:
            self.last_five = self.last_five[1:]