import pygame
import sys
import random
import os
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airplane Game")

# Load the loading image
loading_image = pygame.image.load("loading.png")
loading_image = pygame.transform.scale(loading_image, (WIDTH, HEIGHT))

# Load the background image
background = pygame.image.load(os.path.join('sky1.png'))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load other images and set initial positions
aeroplane = pygame.transform.scale(pygame.image.load(os.path.join('plane.png')), (40, 30))
boy = pygame.transform.scale(pygame.image.load(os.path.join('boy.png')), (25, 50))
gift = pygame.transform.scale(pygame.image.load(os.path.join('gift.png')), (25, 30))
aeroplane_x, aeroplane_y = random.randint(0, WIDTH - 30), 0
boy_x, boy_y = (WIDTH - 40) // 2, HEIGHT - 40
gift_objects, score = [], 0
font, clock = pygame.font.Font(None, 36), pygame.time.Clock()

# Function to create a new falling gift object
def create_gift():
    x = aeroplane_x + 15  # Start gifts at the middle of the aeroplane
    y = aeroplane_y + 30  # Start gift objects from the bottom of the aeroplane
    return {"x": x, "y": y}

# Display the loading image
loading_time = 2  # Time to display the loading image in seconds

start_time = time.time()
while time.time() - start_time < loading_time:
    screen.blit(loading_image, (0, 0))
    pygame.display.update()

# Main game loop
in_game = True
total_gifts = 0
aeroplane_speed = 2
boy_speed = 5
time_since_last_gift = 0
gift_interval = 60  # Set the interval for gift creation (in frames)

while in_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_game = False

    aeroplane_x += aeroplane_speed
    aeroplane_x = aeroplane_x % WIDTH

    time_since_last_gift += 1

    if aeroplane_y == 0 and time_since_last_gift >= gift_interval:
        gift_objects.append(create_gift())
        total_gifts += 1
        time_since_last_gift = 0  # Reset the timer

    for gift_obj in gift_objects[:]:
        gift_obj["y"] += 2
        if boy_x < gift_obj["x"] < boy_x + 40 and boy_y < gift_obj["y"] < boy_y + 40:
            gift_objects.remove(gift_obj)
            score += 1

    gift_objects = [gift_obj for gift_obj in gift_objects if gift_obj["y"] < HEIGHT]

    if total_gifts >= 50:
        in_game = False

    keys = pygame.key.get_pressed()
    boy_x -= boy_speed if keys[pygame.K_LEFT] else 0
    boy_x += boy_speed if keys[pygame.K_RIGHT] else 0
    boy_x = max(0, min(boy_x, WIDTH - 40))

    screen.blit(background, (0, 0))  # Set the background image
    screen.blit(aeroplane, (aeroplane_x, aeroplane_y))
    
    for gift_obj in gift_objects:
        screen.blit(gift, (gift_obj["x"], gift_obj["y"]))
    
    screen.blit(boy, (boy_x, boy_y))
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    pygame.display.update()
    clock.tick(60)

# Change the background to white for the Game Over screen
screen.fill(WHITE)
pygame.display.update()

# Display "Game Over" when the game ends
game_over_text = font.render("Game Over", True, RED)
screen.blit(game_over_text, (WIDTH // 2 - 70, HEIGHT // 2 - 18))
score_text = font.render(f"You have scored {score} points", True, BLACK)
screen.blit(score_text, (WIDTH // 2 - 190, HEIGHT // 2 + 18))
pygame.display.update()
time.sleep(4)  # Display "Game Over" for 4 seconds

# Quit Pygame
pygame.quit()
sys.exit()
