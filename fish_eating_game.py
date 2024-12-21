import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Colors
COLORS = [
    (255, 179, 186),  # #ffb3ba
    (255, 223, 186),  # #ffdfba
    (255, 255, 186),  # #ffffba
    (186, 255, 201),  # #baffc9
    (186, 225, 255),  # #bae1ff
]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Create the screen (scalable to fullscreen)
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Fish Eating Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Font for displaying score and level
font = pygame.font.Font(None, 36)

# Load sound for level completion
level_up_sound = pygame.mixer.Sound("level_up.wav")

# Fish class
class Fish(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.size = size
        self.speed = 5

    def grow(self):
        self.size += 5
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

# Small fish class
class SmallFish(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.color = color

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
    target_color = COLORS[0]

    # Generate small fish with non-overlapping logic
    def spawn_small_fish():
        small_fish_group.empty()
        all_sprites.empty()
        all_sprites.add(player)
        for _ in range(level * 5):
            while True:
                x = random.randint(50, WIDTH - 50)
                y = random.randint(50, HEIGHT - 50)
                size = random.randint(10, player.size - 5)
                color = random.choice(COLORS)

                # Create a new fish and check overlap
                small_fish = SmallFish(x, y, size, color)
                if not any(fish.rect.colliderect(small_fish.rect) for fish in small_fish_group):
                    small_fish_group.add(small_fish)
                    all_sprites.add(small_fish)
                    break

    spawn_small_fish()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Exit fullscreen
                    pygame.quit()
                    sys.exit()

        # Update player
        player.update()

        # Check collisions
        for fish in small_fish_group:
            if player.rect.colliderect(fish.rect):
                if fish.color == target_color:
                    small_fish_group.remove(fish)
                    all_sprites.remove(fish)
                    score += 1
                    player.grow()
                else:
                    # Reset the level if the wrong color is touched
                    spawn_small_fish()
                    score = max(score - level, 0)
                    break

        # Check if all target fish are eaten
        if all(fish.color != target_color for fish in small_fish_group):
            level += 1
            if level <= 5:
                target_color = COLORS[0]  # Eat all fish for levels 1-5
            else:
                target_color = random.choice(COLORS)  # Choose a specific color for higher levels
            spawn_small_fish()
            level_up_sound.play()  # Play level-up sound

        # Clear screen
        screen.fill(WHITE)

        # Draw all sprites
        all_sprites.draw(screen)

        # Display score and level
        score_text = font.render(f"Score: {score}", True, BLACK)
        level_text = font.render(f"Level: {level}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

        # Draw target color block
        target_block = pygame.Surface((50, 50))
        target_block.fill(target_color)
        screen.blit(target_block, (10, 90))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
