import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Run Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
gravity = 0.5
game_speed = 5
score = 0
high_score = 0
level = 1
is_night = False

# Load and resize images
try:
    dino_image = pygame.image.load("D:/72 projects of python/Chrome-Dino-game/dino.png")
    dino_image = pygame.transform.scale(dino_image, (50, 50))  # Resize dino image

    background_day = pygame.image.load("D:/72 projects of python/Chrome-Dino-game/background_day.png")
    background_day = pygame.transform.scale(background_day, (WIDTH, HEIGHT))  # Scale background to screen size

    background_night = pygame.image.load("D:/72 projects of python/Chrome-Dino-game/background_night.png")
    background_night = pygame.transform.scale(background_night, (WIDTH, HEIGHT))  # Scale background to screen size

    obstacle_image = pygame.image.load("D:/72 projects of python/Chrome-Dino-game/cactus.png")
    obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))  # Resize obstacle image
except pygame.error as e:
    print("Error loading images:", e)
    pygame.quit()
    sys.exit()


# Dino character
class Dino:
    def __init__(self):
        self.image = dino_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 80, HEIGHT - self.rect.height - 10
        self.jump_speed = -15
        self.is_jumping = False
        self.velocity_y = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = self.jump_speed

    def update(self):
        self.velocity_y += gravity
        self.rect.y += self.velocity_y
        if self.rect.y >= HEIGHT - self.rect.height - 10:
            self.rect.y = HEIGHT - self.rect.height - 10
            self.is_jumping = False

    def draw(self):
        screen.blit(self.image, self.rect)

# Obstacles
class Obstacle:
    def __init__(self):
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 200  # Start obstacle further away
        self.rect.y = HEIGHT - self.rect.height - 10

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            self.rect.x = WIDTH + random.randint(200, 400)  # Randomize re-entry position

    def draw(self):
        screen.blit(self.image, self.rect)

# Game Functions
def draw_background():
    screen.blit(background_night if is_night else background_day, (0, 0))

def display_score():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {int(score)}", True, BLACK)
    screen.blit(text, (WIDTH - 120, 20))

# Main Game Function
def main():
    global game_speed, score, high_score, is_night, level
    clock = pygame.time.Clock()
    running = True

    while True:
        # Reset game variables
        game_speed = 5
        score = 0
        level = 1
        is_night = False

        # Create new instances for each game run
        dino = Dino()
        obstacle = Obstacle()

        # Game loop
        while running:
            screen.fill(WHITE)
            draw_background()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        dino.jump()

            # Update and draw Dino
            dino.update()
            dino.draw()

            # Update and draw Obstacle
            obstacle.update()
            obstacle.draw()

            # Collision detection
            if dino.rect.colliderect(obstacle.rect):
                print("Collision detected! Game over.")
                pygame.time.delay(2000)  # Delay for 2 seconds
                break  # Break to reset the game after a collision

            # Update score and levels
            score += 0.1
            if int(score) % 100 == 0:  # Every 100 points, speed and level up
                game_speed += 1
                level += 1
                is_night = not is_night  # Toggle night mode for visual interest

            # Display score
            display_score()

            pygame.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    main()
