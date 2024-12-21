import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fish Eating Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Font for displaying score and level
font = pygame.font.Font(None, 36)

# Fish class
class Fish(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.size = size

    def grow(self):
        self.size += 5
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=self.rect.center)

# Small fish class
class SmallFish(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))

# Main game function
def main():
    # Initialize player fish
    player = Fish(WIDTH // 2, HEIGHT // 2, 30, BLUE)
    all_sprites = pygame.sprite.Group()
    small_fish_group = pygame.sprite.Group()
    all_sprites.add(player)

    # Initialize variables
    score = 0
    level = 1
    speed = 5

    # Generate small fish
    def spawn_small_fish():
        for _ in range(level * 5):
            x = random.randint(20, WIDTH - 20)
            y = random.randint(20, HEIGHT - 20)
            size = random.randint(10, player.size - 5)
            small_fish = SmallFish(x, y, size)
            small_fish_group.add(small_fish)
            all_sprites.add(small_fish)

    spawn_small_fish()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.rect.y -= speed
        if keys[pygame.K_DOWN]:
            player.rect.y += speed
        if keys[pygame.K_LEFT]:
            player.rect.x -= speed
        if keys[pygame.K_RIGHT]:
            player.rect.x += speed

        # Check collisions
        for fish in small_fish_group:
            if player.rect.colliderect(fish.rect):
                if player.size > fish.rect.width:
                    small_fish_group.remove(fish)
                    all_sprites.remove(fish)
                    score += 1
                    player.grow()
                else:
                    running = False

        # Check if all small fish are eaten
        if len(small_fish_group) == 0:
            level += 1
            spawn_small_fish()

        # Clear screen
        screen.fill(WHITE)

        # Draw all sprites
        all_sprites.draw(screen)

        # Display score and level
        score_text = font.render(f"Score: {score}", True, BLACK)
        level_text = font.render(f"Level: {level}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
