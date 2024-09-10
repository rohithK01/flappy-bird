import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game settings
GRAVITY = 0.5
FLAP_STRENGTH = -8
PIPE_SPEED = 3
PIPE_WIDTH = 70
GAP_HEIGHT = 150

# Create screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_image = pygame.image.load("bird.jpeg")
bird_image = pygame.transform.scale(bird_image, (50, 50))

# Define Bird class
class Bird:
    def __init__(self):
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (50, SCREEN_HEIGHT // 2)
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)

        # Prevent bird from falling out of screen
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Define Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, SCREEN_HEIGHT - GAP_HEIGHT - 100)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + GAP_HEIGHT, PIPE_WIDTH, SCREEN_HEIGHT - self.height - GAP_HEIGHT)

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

    def collide(self, bird):
        return self.top_rect.colliderect(bird.rect) or self.bottom_rect.colliderect(bird.rect)

# Main game loop
def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = []
    score = 0
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()

        if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.update()
            if pipe.collide(bird):
                running = False

        pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]

        screen.fill(WHITE)
        bird.draw(screen)

        for pipe in pipes:
            pipe.draw(screen)

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        clock.tick(60)

# Run the game
main()
pygame.quit()
