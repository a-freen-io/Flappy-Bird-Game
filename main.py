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
GAP_SIZE = int(3 * FPS)
PIPE_SPEED = 5
GAP_BETWEEN_PIPES = int(4 * FPS)

# Load and resize images
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
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()
        if is_bottom:
            self.rect.topleft = (x, HEIGHT - height)
        else:
            self.rect.topleft = (x, 0) 

    def update(self):
        self.rect.x -= PIPE_SPEED

# Create a ground class
class Ground(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = ground_image
        self.rect = self.image.get_rect() 
        self.rect.topleft = (0, y)

    def update(self):
        self.rect.x -= PIPE_SPEED

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

# --- NEW VARIABLES FOR LOGIC ---
running = True
game_active = True       # Keeps track if we are playing or dead
game_over_start_time = 0 # Keeps track of when we died

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Only jump if game is active
            if game_active:
                bird.jump()

    # --- UPDATES (Only move things if game is active) ---
    if game_active:
        all_sprites.update()

        # Check for collisions
        if pygame.sprite.spritecollide(bird, pipes, False):
            game_active = False # Stop the movement
            game_over_start_time = pygame.time.get_ticks() # Record the exact time we died

        # Generate new pipes
        if all_sprites.sprites()[-1].rect.right < WIDTH - GAP_SIZE:
            top_pipe_height = random.randint(50, min(HEIGHT // 2 - GAP_SIZE // 2, int(HEIGHT * 0.75)))
            bottom_pipe_height = HEIGHT - top_pipe_height - GAP_BETWEEN_PIPES
            new_top_pipe = Pipe(WIDTH, top_pipe_height, is_bottom=False)
            new_bottom_pipe = Pipe(WIDTH, bottom_pipe_height)
            pipes.add(new_top_pipe, new_bottom_pipe)
            all_sprites.add(new_top_pipe, new_bottom_pipe)
            score += 1

        # Remove off-screen pipes
        for sprite in all_sprites:
            if isinstance(sprite, Pipe) or isinstance(sprite, Ground):
                if sprite.rect.right < 0:
                    sprite.kill()

    # --- DRAWING ---
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    # Display the score  
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # --- GAME OVER LOGIC ---
    if not game_active:
        # 1. Draw the Game Over Image
        screen.blit(game_over_image, game_over_rect)
        
        # 2. Check if 10 seconds (10000ms) have passed
        current_time = pygame.time.get_ticks()
        if current_time - game_over_start_time > 10000:
            running = False # Quit the game after 10 seconds

    pygame.display.flip()   
    clock.tick(FPS)

pygame.quit()
sys.exit()