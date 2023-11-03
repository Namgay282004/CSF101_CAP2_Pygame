import pygame
import sys
import random
import os
import time

try:
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 1000, 800

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    font_size = 24
    missed_gifts = 0

    # Create the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Airplane Game")

    # Load the loading image
    loading_image = pygame.image.load("loading.png")
    loading_image = pygame.transform.scale(loading_image, (WIDTH, HEIGHT))

    # Main game loop for loading
    in_loading = True
    loading_start_time = time.time()

    while in_loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        elapsed_time = time.time() - loading_start_time
        if elapsed_time >= 3:
            in_loading = False

        screen.blit(loading_image, (0, 0))  # Display the loading image
        pygame.display.update()

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

    # Create a new font object with the desired font size
    font = pygame.font.Font(None, font_size)

    # Function to display instructions at the center of the screen
    def display_instructions_center():
        instructions = [
            "Instructions:",
            "1. Use the Left and Right arrow keys to move the boy left and right.",
            "2. Collect the falling gifts to increase your score.",
            "3. You have to collect 30 gifts to win the game.",
            "4. Avoid missing gifts, as missing too many will result in a Game Over.",
            "5. Press 'ESC' to quit the game at any time."
        ]

        y_position = (HEIGHT - len(instructions) * 30) // 2
        for line in instructions:
            instruction_text = font.render(line, True, BLACK)
            text_rect = instruction_text.get_rect(left=(WIDTH // 4), top=y_position)
            screen.blit(instruction_text, text_rect)
            y_position += font_size + 6

        return y_position  # Return the y-position after displaying instructions

    # Get the y-position after displaying instructions
    start_button_y = display_instructions_center() + 30  # Add some spacing

    # Create the "START" button at the new position
    start_button = font.render("START", True, BLACK)
    start_button_rect = start_button.get_rect(topleft=(450, 650))

    # Function to check if the "START" button is clicked
    def is_start_button_clicked(pos):
        return start_button_rect.collidepoint(pos)

    # Main game loop
    game_started = False

    while not game_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_started = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if is_start_button_clicked(event.pos):
                    game_started = True

        screen.blit(background, (0, 0))  # Set the background image
        display_instructions_center()
        screen.blit(start_button, start_button_rect)
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
            elif gift_obj["y"] >= HEIGHT:  # Check if the gift has gone off the screen
                missed_gifts += 1
        gift_objects = [gift_obj for gift_obj in gift_objects if gift_obj["y"] < HEIGHT]

        if total_gifts >= 30:
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
        missed_gifts_text = font.render(f"Missed Gifts: {missed_gifts}", True, BLACK)  # Display missed gifts
        screen.blit(score_text, (10, 10))
        screen.blit(missed_gifts_text, (10, 10 + font_size + 6))  # Adjust vertical position

        pygame.display.update()
        clock.tick(60)

    # Change the background to white for the Game Over screen
    screen.fill(WHITE)
    pygame.display.update()

    # Display "Game Over" and "You have scored" at the center
    game_over_text = font.render("Game Over", True, RED)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 18))
    score_text = font.render(f"You have scored {score} points", True, BLACK)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 18))

    # Change the background to white for the Game Over screen
    screen.fill(WHITE)
    pygame.display.update()

    # Display "Game Over" and "You have scored" at the center
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    pygame.display.update()
    time.sleep(4)  # Display "Game Over" for 4 seconds

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Quit Pygame
    pygame.quit()
    sys.exit()

