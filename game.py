import pygame
import sys
import random
import math
# Initialize Pygame
pygame.init()

# Constants
PITCH_LENGTH = 1000  # Representing approx. 100 meters
PITCH_WIDTH = 600    # Representing approx. 64 meters
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BALL_RADIUS = 10
PLAYER_RADIUS = 15
PASS_SPEED = 5  # Speed of the ball passing
PLAYER_SPEED = 2  # Speed of movement

# Goal area dimensions (scaled)
GOAL_AREA_WIDTH = int(5.5 * PITCH_LENGTH / 100)  # ~5.5 meters
GOAL_AREA_HEIGHT = int(18.32 * PITCH_WIDTH / 64)  # ~18.32 meters
# Penalty area dimensions (scaled)
PENALTY_AREA_WIDTH = int(16.5 * PITCH_LENGTH / 100)  # ~16.5 meters
PENALTY_AREA_HEIGHT = int(40.3 * PITCH_WIDTH / 64)    # ~40.3 meters

class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.target_position = position
        self.team = None  # This will be assigned later

    def move_toward_target(self):
        # Calculate the direction and distance to target
        dx = self.target_position[0] - self.position[0]
        dy = self.target_position[1] - self.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        # Only move if target is further than one step away
        if distance > PLAYER_SPEED:
            # Calculate movement step
            step_x = dx / distance * PLAYER_SPEED
            step_y = dy / distance * PLAYER_SPEED
            # Update player position
            self.position = (self.position[0] + step_x, self.position[1] + step_y)

class FootballGame:
    def __init__(self):
        self.team_A = [Player(f"A1", (50, PITCH_WIDTH // 2)),  # Goalkeeper
                       Player(f"A2", (PENALTY_AREA_WIDTH + 50, PITCH_WIDTH // 2 - 50)),  # Defender
                       Player(f"A3", (PENALTY_AREA_WIDTH + 50, PITCH_WIDTH // 2 + 50)),  # Defender
                       Player(f"A4", (300, PITCH_WIDTH // 2 - 25)),  # Midfielder
                       Player(f"A5", (300, PITCH_WIDTH // 2 + 25)),  # Midfielder
                       Player(f"A6", (500, PITCH_WIDTH // 2 - 50)),  # Attacker
                       Player(f"A7", (500, PITCH_WIDTH // 2))]      # Attacker

        self.team_B = [Player(f"B1", (PITCH_LENGTH - 50, PITCH_WIDTH // 2)),  # Goalkeeper
                       Player(f"B2", (PITCH_LENGTH - PENALTY_AREA_WIDTH - 50, PITCH_WIDTH // 2 - 50)),  # Defender
                       Player(f"B3", (PITCH_LENGTH - PENALTY_AREA_WIDTH - 50, PITCH_WIDTH // 2 + 50)),  # Defender
                       Player(f"B4", (700, PITCH_WIDTH // 2 - 25)),  # Midfielder
                       Player(f"B5", (700, PITCH_WIDTH // 2 + 25)),  # Midfielder
                       Player(f"B6", (600, PITCH_WIDTH // 2 - 50)),  # Attacker
                       Player(f"B7", (600, PITCH_WIDTH // 2))]      # Attacker

        self.ball_position = (50, PITCH_WIDTH // 2)  # Start in front of A1
        self.target_position = self.team_A[1].position  # Target position for the pass
        self.setup_teams()
        self.screen = pygame.display.set_mode((PITCH_LENGTH, PITCH_WIDTH))
        pygame.display.set_caption('Football Game')

        # Start the passing animation
        self.pass_in_progress = True
        self.pass_progress = 0

    def setup_teams(self):
        for player in self.team_A:
            player.team = 'A'
        for player in self.team_B:
            player.team = 'B'

    TEAM_A_GOAL_LEFT = (0, (PITCH_WIDTH - GOAL_AREA_HEIGHT) // 2)
    TEAM_A_GOAL_RIGHT = (0, (PITCH_WIDTH + GOAL_AREA_HEIGHT) // 2)
    TEAM_B_GOAL_LEFT = (PITCH_LENGTH, (PITCH_WIDTH - GOAL_AREA_HEIGHT) // 2)
    TEAM_B_GOAL_RIGHT = (PITCH_LENGTH, (PITCH_WIDTH + GOAL_AREA_HEIGHT) // 2)

    # Function to calculate xG based on position and target goal area
    def calculate_xg(self, player_position, team):
        if team == 'A':  # If Team A is shooting, target Team B's goal
            goal_left = self.TEAM_B_GOAL_LEFT
            goal_right = self.TEAM_B_GOAL_RIGHT
        else:  # Team B is shooting, target Team A's goal
            goal_left = self.TEAM_A_GOAL_LEFT
            goal_right = self.TEAM_A_GOAL_RIGHT

        # Calculate distances to both goalposts
        distance_left = math.sqrt((player_position[0] - goal_left[0]) ** 2 + (player_position[1] - goal_left[1]) ** 2)
        distance_right = math.sqrt((player_position[0] - goal_right[0]) ** 2 + (player_position[1] - goal_right[1]) ** 2)

        # Calculate the angle between player and the goalposts
        angle_to_goal = math.atan2(goal_right[1] - player_position[1], goal_right[0] - player_position[0]) - \
                        math.atan2(goal_left[1] - player_position[1], goal_left[0] - player_position[0])
        angle_to_goal = abs(angle_to_goal)  # Ensure positive angle

        # Convert to degrees if needed
        angle_to_goal_deg = math.degrees(angle_to_goal)

        # Calculate base xG using inverse distance and angle as factors
        xg_from_distance = 1 / (0.1 * (distance_left + distance_right) + 1)  # Adjusted for scaling
        xg_from_angle = angle_to_goal_deg / 120  # Normalize by 120 degrees max angle

        # Final xG, constrained to stay below 50% shot accuracy limit
        xg = min(xg_from_distance * xg_from_angle, 0.5)
        return xg
    
    def attempt_shot(self, player):
        """Simulate a shot attempt and calculate xG."""
        if player.team == 'A':
            xg = self.calculate_xg(player.position, 'A')
        else:
            xg = self.calculate_xg(player.position, 'B')

        # Decide if the shot is a goal based on xG
        if random.random() < xg:
            print(f"GOAL by {player.name} with xG: {xg:.2f}")
        else:
            print(f"Shot missed by {player.name} with xG: {xg:.2f}")

    def display_field(self):
        # Fill background
        self.screen.fill(GREEN)

        # Draw center line
        pygame.draw.line(self.screen, WHITE, (PITCH_LENGTH // 2, 0), (PITCH_LENGTH // 2, PITCH_WIDTH), 2)

        # Draw penalty areas (only outlines)
        pygame.draw.rect(self.screen, GREEN, (0, (PITCH_WIDTH - PENALTY_AREA_HEIGHT) // 2, PENALTY_AREA_WIDTH, PENALTY_AREA_HEIGHT))  # Team A penalty area
        pygame.draw.rect(self.screen, GREEN, (PITCH_LENGTH - PENALTY_AREA_WIDTH, (PITCH_WIDTH - PENALTY_AREA_HEIGHT) // 2, PENALTY_AREA_WIDTH, PENALTY_AREA_HEIGHT))  # Team B penalty area
        pygame.draw.rect(self.screen, WHITE, (0, (PITCH_WIDTH - PENALTY_AREA_HEIGHT) // 2, PENALTY_AREA_WIDTH, PENALTY_AREA_HEIGHT), 2)  # Team A penalty area outline
        pygame.draw.rect(self.screen, WHITE, (PITCH_LENGTH - PENALTY_AREA_WIDTH, (PITCH_WIDTH - PENALTY_AREA_HEIGHT) // 2, PENALTY_AREA_WIDTH, PENALTY_AREA_HEIGHT), 2)  # Team B penalty area outline

        # Draw goal areas (only outlines)
        pygame.draw.rect(self.screen, GREEN, (0, (PITCH_WIDTH - GOAL_AREA_HEIGHT) // 2, GOAL_AREA_WIDTH, GOAL_AREA_HEIGHT))  # Team A goal area
        pygame.draw.rect(self.screen, GREEN, (PITCH_LENGTH - GOAL_AREA_WIDTH, (PITCH_WIDTH - GOAL_AREA_HEIGHT) // 2, GOAL_AREA_WIDTH, GOAL_AREA_HEIGHT))  # Team B goal area
        pygame.draw.rect(self.screen, WHITE, (0, (PITCH_WIDTH - GOAL_AREA_HEIGHT) // 2, GOAL_AREA_WIDTH, GOAL_AREA_HEIGHT), 2)  # Team A goal area outline
        pygame.draw.rect(self.screen, WHITE, (PITCH_LENGTH - GOAL_AREA_WIDTH, (PITCH_WIDTH - GOAL_AREA_HEIGHT) // 2, GOAL_AREA_WIDTH, GOAL_AREA_HEIGHT), 2)  # Team B goal area outline
        
        # Draw penalty spots
        pygame.draw.circle(self.screen, WHITE, (int(7 * PITCH_LENGTH / 100), PITCH_WIDTH // 2), 5)  # Team A penalty spot
        pygame.draw.circle(self.screen, WHITE, (int(PITCH_LENGTH - 7 * PITCH_LENGTH / 100), PITCH_WIDTH // 2), 5)  # Team B penalty spot

        # Draw goal areas (outlines only)
        pygame.draw.rect(self.screen, WHITE, (0, (PITCH_WIDTH - GOAL_AREA_HEIGHT) // 2, GOAL_AREA_WIDTH, GOAL_AREA_HEIGHT), 2)
        pygame.draw.rect(self.screen, WHITE, (PITCH_LENGTH - GOAL_AREA_WIDTH, (PITCH_WIDTH - GOAL_AREA_HEIGHT) // 2, GOAL_AREA_WIDTH, GOAL_AREA_HEIGHT), 2)

        # Draw players for Team A
        for player in self.team_A:
            pygame.draw.circle(self.screen, BLUE, player.position, PLAYER_RADIUS)
            self.render_text(player.name, player.position[0], player.position[1])

        # Draw players for Team B
        for player in self.team_B:
            pygame.draw.circle(self.screen, RED, player.position, PLAYER_RADIUS)
            self.render_text(player.name, player.position[0], player.position[1])

        # Draw the ball
        pygame.draw.circle(self.screen, YELLOW, self.ball_position, BALL_RADIUS)

        pygame.display.flip()  # Update the display

    def render_text(self, text, x, y):
        font = pygame.font.Font(None, 24)
        text_surface = font.render(text, True, WHITE)
        self.screen.blit(text_surface, (x - PLAYER_RADIUS, y - PLAYER_RADIUS - 20))  # Position text above player

    def pass_ball(self, passer, receiver):
        if self.pass_in_progress:
            # Calculate the distance to move the ball
            dx = receiver.position[0] - self.ball_position[0]
            dy = receiver.position[1] - self.ball_position[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5

            # Normalize the direction vector
            if distance > 0:
                dx /= distance
                dy /= distance

                # Update ball position
                self.ball_position = (self.ball_position[0] + dx * PASS_SPEED, self.ball_position[1] + dy * PASS_SPEED)

                # Check if the ball has reached the receiver's position
                if distance < PASS_SPEED:
                    self.ball_position = receiver.position
                    self.pass_in_progress = False
                    print(f"{passer.name} passes the ball to {receiver.name}.")

    def run(self):
        # Set up fixed team assignments
        for player in self.team_A:
            player.team = 'A'
        for player in self.team_B:
            player.team = 'B'

        # Main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Move players towards their target positions
            for player in self.team_A + self.team_B:
                player.move_toward_target()

            # Display field with updated player positions
            self.display_field()
            pygame.time.delay(100)  # Frame rate control


# Run the game
game = FootballGame()
game.run()

'''
on the ball : 
    if(attempt shot){
    attempt_shot
    }
    else{
    if(not_being_defended)
     move_forward()
    else:
        pass_to_open_player() - priority : player  closest to the goal
    }
'''