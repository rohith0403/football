class Club:
    def __init__(self, name, manager, players):
        self.name = name  
        self.manager = manager
        self.players = players

    def __str__(self):
        return self.name  # Display player name
