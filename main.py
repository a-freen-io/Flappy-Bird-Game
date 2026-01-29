import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GROUND_HEIGHT = 100
FPS = 60
GRAVITY = 1
JUMP_SPEED = -15
PIPE_WIDTH = 90
GAP_SIZE = int(3 * FPS)  # 3-second gap
PIPE_SPEED = 5
GAP_BETWEEN_PIPES = int(4 * FPS)  # 4-second gap between top and bottom pipes

# Load and resize images
# (Assuming you have 'bird.png', 'background.jpeg', 'pipe.png', and 'ground.png' in your working directory)
bird_image = pygame.transform.scale(pygame.image.load('bird.png'), (70, 70))
background_image = pygame.transform.scale(pygame.image.load('background.jpeg'), (WIDTH, HEIGHT))
pipe_image = pygame.transform.scale(pygame.image.load('pipe.png'), (PIPE_WIDTH, HEIGHT))
ground_image = pygame.transform.scale(pygame.image.load('ground.png'), (WIDTH, GROUND_HEIGHT))
game_over_image = pygame.transform.scale(pygame.image.load('game_over.jpg'), (400, 100))

# Create a bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.velocity = 0

    def jump(self):
        self.velocity = JUMP_SPEED

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Keep the bird on the screen
        if self.rect.bottom > HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = HEIGHT - GROUND_HEIGHT
            self.velocity = 0

# Create a pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, height, is_bottom=True):
        super().__init__()
        self.is_bottom = is_bottom
        self.image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, height))
        if not is_bottom:
            self.image = pygame.transform.flip(self.image, False, True)  # Flip top pipes upside down
        self.rect = self.image.get_rect()

        if is_bottom:
            self.rect.topleft = (x, HEIGHT - height)
        else:
            self.rect.topleft = (x, 0) 

    def update(self):
        self.rect.x -= PIPE_SPEED  # Move the pipe to the left

# Create a ground class
class Ground(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = ground_image
        self.rect = self.image.get_rect() 
        self.rect.topleft = (0, y)

    def update(self):
        self.rect.x -= PIPE_SPEED  # Move the ground to the left

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Create sprite groups
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
grounds = pygame.sprite.Group()

# Create initial objects
bird = Bird()
all_sprites.add(bird)

# Create initial ground
ground = Ground(HEIGHT - GROUND_HEIGHT)
grounds.add(ground)
all_sprites.add(ground)

# Initialize score
score = 0
font = pygame.font.Font(None, 36)

# Load game over screen
game_over_rect = game_over_image.get_rect()
game_over_rect.center = (WIDTH // 2, HEIGHT // 2)

clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()

    # Update
    all_sprites.update()

    # Check for collisions
    if pygame.sprite.spritecollide(bird, pipes, False):
        running = False

    # Generate new pipes
    if all_sprites.sprites()[-1].rect.right < WIDTH - GAP_SIZE:
        # Randomize the height of the pipes within the screen bounds
        top_pipe_height = random.randint(50, min(HEIGHT // 2 - GAP_SIZE // 2, int(HEIGHT * 0.75)))
        bottom_pipe_height = HEIGHT - top_pipe_height - GAP_BETWEEN_PIPES

        new_top_pipe = Pipe(WIDTH, top_pipe_height, is_bottom=False)
        new_bottom_pipe = Pipe(WIDTH, bottom_pipe_height)

        pipes.add(new_top_pipe, new_bottom_pipe)
        all_sprites.add(new_top_pipe, new_bottom_pipe)

        # Increment score when the bird crosses a set of pipes
        score += 1

    # Remove off-screen pipes and grounds
    for sprite in all_sprites:
        if isinstance(sprite, Pipe) or isinstance(sprite, Ground):
            if sprite.rect.right < 0:
                sprite.kill()

    # Draw
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    # Display the score  
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Display game over screen when the game ends
    if not running:
        screen.blit(game_over_image, game_over_rect)

    pygame.display.flip()   

    clock.tick(FPS)

pygame.quit()
sys.exit()
