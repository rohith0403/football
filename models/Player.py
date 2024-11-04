class Player:
    def __init__(self, name, role, current_ability, club):
        self.name = name
        self.role = role
        self.current_ability = current_ability
        self.club = club
        self.set_attributes()

    def set_attributes(self):
        if self.role == "Defender":
            self.shooting = int(self.current_ability * 0.1)
            self.passing = int(self.current_ability * 0.3)
            self.dribbling = int(self.current_ability * 0.2)
            self.defending = int(self.current_ability * 0.4)
        if self.role == "Midfielder":
            self.shooting = int(self.current_ability * 0.2)
            self.passing = int(self.current_ability * 0.3)
            self.dribbling = int(self.current_ability * 0.3)
            self.defending = int(self.current_ability * 0.2)
        if self.role == "Attacker":
            self.shooting = int(self.current_ability * 0.5)
            self.passing = int(self.current_ability * 0.2)
            self.dribbling = int(self.current_ability * 0.2)
            self.defending = int(self.current_ability * 0.1)

    def set_club(self, club):
        self.club = club

    def let_go(self):
        self.club = ""
