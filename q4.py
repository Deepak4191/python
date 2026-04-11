import pygame
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("F1 Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
BLUE = (0, 100, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()
FPS = 60

# Player
player_width = 50
player_height = 100
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 20
player_speed = 7

# Enemy
enemy_width = 50
enemy_height = 100
enemy_x = random.randint(0, WIDTH - enemy_width)
enemy_y = -enemy_height
enemy_speed = 6

# Road animation
road_offset = 0

# Distance system (finish line)
distance = 0
finish_distance = 3000  # game ends after this

# Font
font = pygame.font.SysFont(None, 36)

# Draw car (simple F1 style)
def draw_car(x, y, color):
    # Body
    pygame.draw.rect(screen, color, (x + 10, y, 30, 80))
    
    # Nose
    pygame.draw.polygon(screen, color, [
        (x + 25, y - 20),
        (x + 15, y),
        (x + 35, y)
    ])

    # Rear wing
    pygame.draw.rect(screen, color, (x + 5, y + 80, 40, 10))

    # Wheels
    pygame.draw.rect(screen, BLACK, (x, y + 10, 10, 20))
    pygame.draw.rect(screen, BLACK, (x + 40, y + 10, 10, 20))
    pygame.draw.rect(screen, BLACK, (x, y + 50, 10, 20))
    pygame.draw.rect(screen, BLACK, (x + 40, y + 50, 10, 20))

# Game loop
running = True
game_over = False
win = False

while running:
    screen.fill(GRAY)

    # Animate road (movement illusion)
    road_offset += enemy_speed
    if road_offset >= 40:
        road_offset = 0

    for i in range(-40, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 5, i + road_offset, 10, 20))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:

        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Move enemy
        enemy_y += enemy_speed

        if enemy_y > HEIGHT:
            enemy_y = -enemy_height
            enemy_x = random.randint(0, WIDTH - enemy_width)

        # Distance increases (instead of endless play)
        distance += enemy_speed

        # Collision
        if (player_x < enemy_x + enemy_width and
            player_x + player_width > enemy_x and
            player_y < enemy_y + enemy_height and
            player_y + player_height > enemy_y):
            game_over = True

        # Check finish line
        if distance >= finish_distance:
            game_over = True
            win = True

    # Draw cars
    draw_car(player_x, player_y, BLUE)
    draw_car(enemy_x, enemy_y, RED)

    # Draw finish line (when near end)
    if finish_distance - distance < HEIGHT:
        finish_y = finish_distance - distance
        for i in range(0, WIDTH, 40):
            pygame.draw.rect(screen, WHITE, (i, finish_y, 20, 10))

    # UI
    dist_text = font.render(f"Distance: {int(distance)}", True, WHITE)
    screen.blit(dist_text, (10, 10))

    if game_over:
        if win:
            msg = "YOU WIN!"
        else:
            msg = "CRASH! GAME OVER"

        text = font.render(msg, True, YELLOW)
        screen.blit(text, (WIDTH//2 - 100, HEIGHT//2))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()