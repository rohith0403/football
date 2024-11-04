class Club:
    def __init__(self, name, players=[]):
        self.name = name
        self.players = players

    def get_overall_ability(self):
        current_ability = 0
        for player in self.players:
            current_ability += player.current_ability
        return current_ability

    def pick_player(self, player):
        self.players.append(player)


Man_City = Club("Man City")
Arsenal = Club("Arsenal")
Liverpool = Club("Liverpool")
Chelsea = Club("Chelsea")
Man_United = Club("Man United")
Spurs = Club("Spurs")
