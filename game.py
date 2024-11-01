import pygame
import sys

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
        self.team = None  # This will be assigned later

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
                       Player(f"B2", (PITCH_LENGTH- PENALTY_AREA_WIDTH - 50, PITCH_WIDTH // 2 - 50)),  # Defender
                       Player(f"B3", (PITCH_LENGTH - PENALTY_AREA_WIDTH- 50, PITCH_WIDTH // 2 + 50)),  # Defender
                       Player(f"B4", (700, PITCH_WIDTH // 2 - 25)),  # Midfielder
                       Player(f"B5", (700, PITCH_WIDTH // 2 + 25)),  # Midfielder
                       Player(f"B6", (600, PITCH_WIDTH // 2 - 50)),  # Attacker
                       Player(f"B7", (600, PITCH_WIDTH // 2))]      # Attacker

        self.ball_position = (PITCH_LENGTH // 2, PITCH_WIDTH // 2)  # Start in the middle
        self.setup_teams()
        self.screen = pygame.display.set_mode((PITCH_LENGTH, PITCH_WIDTH))
        pygame.display.set_caption('Football Game')

    def setup_teams(self):
        for player in self.team_A:
            player.team = 'A'
        for player in self.team_B:
            player.team = 'B'

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

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_field()
            pygame.time.delay(100)  # Frame rate control

# Run the game
game = FootballGame()
game.run()
