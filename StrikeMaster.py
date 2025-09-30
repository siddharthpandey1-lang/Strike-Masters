import pygame
import random
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 3840, 2160  # 4K resolution
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Epic Football Game")
clock = pygame.time.Clock()

# Ball setup
ball_radius = 30
ball_color = (255, 255, 255)
ball_pos = [WIDTH // 2, HEIGHT - 200]

# Goal setup
goal_width, goal_height = 400, 50
goal_x = WIDTH // 2 - goal_width // 2
goal_y = 100
goal_color = (255, 255, 255)

# Particle setup
particles = []
goal_scored = False
font = pygame.font.SysFont("Arial", 120)

def trigger_particles(x, y):
    for _ in range(100):
        particles.append({
            "pos": [x, y],
            "vel": [random.uniform(-10, 10), random.uniform(-10, 10)],
            "color": [random.randint(100, 255) for _ in range(3)],
            "life": random.randint(30, 60),
            "size": random.randint(5, 15)
        })

def draw_particles():
    for p in particles:
        pygame.draw.circle(screen, p["color"], (int(p["pos"][0]), int(p["pos"][1])), p["size"])
        p["pos"][0] += p["vel"][0]
        p["pos"][1] += p["vel"][1]
        p["life"] -= 1
    particles[:] = [p for p in particles if p["life"] > 0]

def draw_goal():
    pygame.draw.rect(screen, goal_color, (goal_x, goal_y, goal_width, goal_height))

def draw_ball():
    pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)

def check_goal():
    global goal_scored
    if (goal_x < ball_pos[0] < goal_x + goal_width and
        ball_pos[1] - ball_radius < goal_y + goal_height and not goal_scored):
        goal_scored = True
        trigger_particles(*ball_pos)

def draw_text():
    if goal_scored:
        text = font.render("GOAL!", True, (255, 255, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

# Game loop
while True:
    screen.fill((11, 61, 145))  # Deep blue background
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ball_pos = list(pygame.mouse.get_pos())
    draw_goal()
    draw_ball()
    check_goal()
    draw_particles()
    draw_text()

    pygame.display.flip()
    # Draw goalposts
    post_width = 30
    post_height = 200
    post_color = (200, 200, 200)
    # Left post
    pygame.draw.rect(screen, post_color, (goal_x - post_width, goal_y - post_height + goal_height, post_width, post_height))
    # Right post
    pygame.draw.rect(screen, post_color, (goal_x + goal_width, goal_y - post_height + goal_height, post_width, post_height))
    # Crossbar
    crossbar_height = 20
    pygame.draw.rect(screen, post_color, (goal_x - post_width, goal_y - post_height + goal_height, goal_width + 2 * post_width, crossbar_height))

    clock.tick(120) # 120 FPS