import random

class Player:
    def __init__(self, name, role, shooting, passing, dribbling, defending):
        self.name = name  # Player's name
        self.role = role  # Player's role (e.g., attacker, midfielder, defender, goalkeeper)
        self.shooting = shooting  # Shooting skill (0 to 1)
        self.passing = passing  # Passing skill (0 to 1)
        self.dribbling = dribbling  # Dribbling skill (0 to 1)
        self.defending = defending  # Defending skill (0 to 1)
        self.position = [random.uniform(50, 1050), random.uniform(50, 650)]  # Initial random position

    def move(self):
        # Example logic for moving the player (can be customized)
        self.position[0] += random.uniform(-5, 5)  # Move horizontally
        self.position[1] += random.uniform(-5, 5)  # Move vertically

        # Keep the player within the field boundaries
        self.position[0] = max(50, min(1050, self.position[0]))
        self.position[1] = max(50, min(650, self.position[1]))

    def shoot(self):
        # Determine if the shot is on target and if it results in a goal
        shot_on_target = random.random() < 0.5  # 50% chance of shot being on target
        goal_prob = self.shooting * random.uniform(0.01, 0.99)  # Probabilistic goal chance based on shooting skill
        is_goal = shot_on_target and (random.random() < goal_prob)

        return shot_on_target, is_goal

    def pass_ball(self):
        # Logic for passing the ball (can be customized)
        pass_success = random.random() < self.passing  # Success chance based on passing skill
        return pass_success

    def defend(self):
        # Logic for defending (can be customized)
        defend_success = random.random() < self.defending  # Success chance based on defending skill
        return defend_success

    def __str__(self):
        return self.name  # Display player name
