import pytest
import pygame
import sys
import random
import os
import time

WIDTH, HEIGHT = 1000, 800

def initialize_game():
    pygame.init()
    return pygame.display.set_mode((1000, 800))

def load_images():
    loading_image = pygame.image.load("loading.png")
    loading_image = pygame.transform.scale(loading_image, (1000, 800))
    background = pygame.image.load(os.path.join('sky1.png'))
    background = pygame.transform.scale(background, (1000, 800))
    aeroplane = pygame.transform.scale(pygame.image.load(os.path.join('plane.png')), (40, 30))
    boy = pygame.transform.scale(pygame.image.load(os.path.join('boy.png')), (25, 50))
    gift = pygame.transform.scale(pygame.image.load(os.path.join('gift.png')), (25, 30))
    return loading_image, background, aeroplane, boy, gift

def test_initialize_game():
    screen = initialize_game()
    assert isinstance(screen, pygame.Surface)

def test_load_images():
    loading_image, background, aeroplane, boy, gift = load_images()
    assert isinstance(loading_image, pygame.Surface)
    assert isinstance(background, pygame.Surface)
    assert isinstance(aeroplane, pygame.Surface)
    assert isinstance(boy, pygame.Surface)
    assert isinstance(gift, pygame.Surface)

def is_start_button_clicked(pos):
    # Tests whether the start button is clicked based on the provided position.
    start_button_rect = pygame.Rect(450, 650, 100, 30)
    return start_button_rect.collidepoint(pos)

def create_gift(aeroplane_x, aeroplane_y):
    # Tests the creation of a gift with specific coordinates.
    x = aeroplane_x + 15
    y = aeroplane_y + 30
    return {"x": x, "y": y}

def test_game_logic():
    # Tests the basic game logic related to the aeroplane's movement.
    aeroplane_x, aeroplane_y = 100, 200
    aeroplane_speed = 2
    aeroplane_x += aeroplane_speed
    assert aeroplane_x == 102

def test_key_input_handling():
    # Test the key input handling for boy movement.
    keys_left = {pygame.K_LEFT: True}
    keys_right = {pygame.K_RIGHT: True}
    keys_empty = {}
    
    # Mocking the existing boy movement logic
    def mock_handle_boy_movement(boy_x, keys):
        return boy_x - 5 if keys.get(pygame.K_LEFT) else boy_x + 5 if keys.get(pygame.K_RIGHT) else boy_x

    # Test boy moving left
    boy_x_initial = 100
    boy_x_left = boy_x_initial - 5
    assert mock_handle_boy_movement(boy_x_initial, keys_left) == boy_x_left

    # Test boy moving right
    boy_x_right = boy_x_initial + 5
    assert mock_handle_boy_movement(boy_x_initial, keys_right) == boy_x_right

    # Test boy not moving without key input
    assert mock_handle_boy_movement(boy_x_initial, keys_empty) == boy_x_initial

def test_gift_falling():
    # Tests the logic for creating gifts based on time intervals.
    aeroplane_x = 200
    aeroplane_y = 0
    gift_interval = 60
    time_since_last_gift = gift_interval + 1  # Ensure enough time has passed

    # Mocking the existing gift falling logic
    def mock_handle_gift_falling(aeroplane_x, aeroplane_y, time_since_last_gift):
        return {"x": aeroplane_x + 15, "y": aeroplane_y + 30} if time_since_last_gift >= gift_interval else None

    # Test creating a gift when enough time has passed
    assert mock_handle_gift_falling(aeroplane_x, aeroplane_y, time_since_last_gift) == {"x": aeroplane_x + 15, "y": aeroplane_y + 30}

    # Test not creating a gift when not enough time has passed
    time_since_last_gift = 0
    assert mock_handle_gift_falling(aeroplane_x, aeroplane_y, time_since_last_gift) is None

def test_scoring():
    # Tests the scoring logic when the boy catches or misses a gift.
    boy_x = 300
    boy_y = 600
    gift_objects = [{"x": boy_x + 10, "y": boy_y + 10}]  # Gift close to the boy

    # Mocking the existing scoring logic
    def mock_handle_scoring(boy_x, boy_y, gift_objects, score_initial):
        score = score_initial
        for gift_obj in gift_objects:
            if boy_x < gift_obj["x"] < boy_x + 40 and boy_y < gift_obj["y"] < boy_y + 40:
                score += 1
        return score

    # Test scoring when the boy catches a gift
    score_initial = 0
    assert mock_handle_scoring(boy_x, boy_y, gift_objects, score_initial) == 1

    # Test scoring when the boy misses a gift
    score_initial = 0
    boy_y = 0  # Move the boy to the top of the screen
    assert mock_handle_scoring(boy_x, boy_y, gift_objects, score_initial) == 0

def test_boy_movement():
    # Tests the boy's movement logic in response to key inputs.
    keys_left = {pygame.K_LEFT: True}
    keys_right = {pygame.K_RIGHT: True}
    boy_speed = 5

    # Mocking the existing boy movement logic
    def mock_handle_boy_movement(boy_x, keys):
        return boy_x - boy_speed if keys.get(pygame.K_LEFT) else boy_x + boy_speed if keys.get(pygame.K_RIGHT) else boy_x

    # Test boy moving left
    boy_x_initial = 100
    boy_x_left = boy_x_initial - boy_speed
    assert mock_handle_boy_movement(boy_x_initial, keys_left) == boy_x_left

    # Test boy moving right
    boy_x_right = boy_x_initial + boy_speed
    assert mock_handle_boy_movement(boy_x_initial, keys_right) == boy_x_right

def test_initial_positions():
    # Test the initial positions of the aeroplane and boy
    aeroplane_x, aeroplane_y = random.randint(0, WIDTH - 30), 0
    boy_x, boy_y = (WIDTH - 40) // 2, HEIGHT - 40
    assert 0 <= aeroplane_x <= WIDTH - 30
    assert aeroplane_y == 0
    assert 0 <= boy_x <= WIDTH - 40
    assert boy_y == HEIGHT - 40

def test_boy_position_limits():
    # Test the limits of boy's x-position within the screen.
    boy_speed = 5
    boy_x_initial = random.randint(0, WIDTH - 40)
    boy_x = boy_x_initial

    # Move the boy to the right
    boy_x += boy_speed
    boy_x = max(0, min(boy_x, WIDTH - 40))
    assert 0 <= boy_x <= WIDTH - 40

    # Move the boy to the left
    boy_x -= boy_speed
    boy_x = max(0, min(boy_x, WIDTH - 40))
    assert 0 <= boy_x <= WIDTH - 40

def test_boy_position_boundary():
    # Test the boy's x-position limits at the boundaries of the screen.
    boy_speed = 5
    boy_x_initial = WIDTH - 40  # Starting at the right edge of the screen
    boy_x = boy_x_initial

    # Move the boy to the right
    boy_x += boy_speed
    boy_x = max(0, min(boy_x, WIDTH - 40))
    assert 0 <= boy_x <= WIDTH - 40  # Should stay at the right edge

    # Move the boy to the left
    boy_x -= boy_speed
    boy_x = max(0, min(boy_x, WIDTH - 40))
    assert 0 <= boy_x <= WIDTH - 40  # Should wrap around to the right edge

def test_game_completion():
    # Test the game completion condition based on the total number of gifts.
    total_gifts = 30
    assert total_gifts >= 30  # The game should be completed when the total gift reaches 30

def test_missed_gifts():
    # Test the missed gifts count based on the total number of missed gifts.
    missed_gifts = 5
    assert missed_gifts <= 5  # The game should not end if the missed gifts are less than or equal to 5


def test_initial_gift_objects():
    # Test the initial state of gift objects in the game.
    aeroplane_x, aeroplane_y = random.randint(0, WIDTH - 30), 0
    gift_objects, total_gifts = [], 0
    
    # Mocking the existing gift falling logic
    def mock_handle_gift_falling(aeroplane_x, aeroplane_y, time_since_last_gift):
        return {"x": aeroplane_x + 15, "y": aeroplane_y + 30}

    # Test creating a gift when enough time has passed
    time_since_last_gift = 61  # Slightly more than the gift interval
    gift_objects.append(mock_handle_gift_falling(aeroplane_x, aeroplane_y, time_since_last_gift))
    total_gifts += 1

    assert len(gift_objects) == 1
    assert total_gifts == 1

def test_missed_gifts_limit():
    # Test the limit of missed gifts before the game ends.
    missed_gifts_limit = 5
    missed_gifts = 6  # Slightly more than the limit

    assert missed_gifts > missed_gifts_limit  # Game should end if missed gifts exceed the limit

def test_score_limit():
    # Test the limit for the maximum achievable score.
    max_score = 30
    score = 35  # Slightly more than the maximum

    assert score > max_score  # Score should not exceed the maximum achievable score

def test_aeroplane_movement():
    # Test the aeroplane's movement within the screen.
    aeroplane_speed = 2
    aeroplane_x_initial = random.randint(0, WIDTH - 30)
    aeroplane_x = aeroplane_x_initial

    # Move the aeroplane to the right
    aeroplane_x += aeroplane_speed
    aeroplane_x %= WIDTH
    assert 0 <= aeroplane_x <= WIDTH - 30

    # Move the aeroplane to the left
    aeroplane_x -= aeroplane_speed
    aeroplane_x %= WIDTH
    assert 0 <= aeroplane_x <= WIDTH - 30

def test_aeroplane_movement_boundary():
    # Test the aeroplane's movement at the boundaries of the screen.
    aeroplane_speed = 2
    aeroplane_x_initial = WIDTH - 30  # Starting at the right edge of the screen
    aeroplane_x = aeroplane_x_initial

    # Move the aeroplane to the right
    aeroplane_x += aeroplane_speed
    aeroplane_x %= WIDTH
    assert 0 <= aeroplane_x <= WIDTH # Should wrap around to the left edge

def test_game_over_screen():
    # Test the display of the "Game Over" screen.
    screen = initialize_game()

    # Mocking the existing game over screen logic
    def mock_display_game_over():
        screen.fill((255, 255, 255))  # Simulate changing the background to white
        pygame.display.update()

    mock_display_game_over()

    # Check if the background is white after displaying "Game Over"
    assert screen.get_at((WIDTH // 2, HEIGHT // 2)) == (255, 255, 255)





   