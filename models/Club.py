class Club:
    def __init__(self, name, manager, players):
        self.name = name
        self.manager = manager
        self.players = players

    def get_overall_ability(self):
        current_ability = 0
        for player in self.players:
            current_ability += player.current_ability
        return current_ability

    def pick_player(self, player):
        self.players.append(player)
        player.set_club(self.name)
