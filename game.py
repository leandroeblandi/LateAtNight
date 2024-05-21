import pygame
import sys
import random

# Constants
WIDTH = 600
HEIGHT = 600
PLAYER_SIZE = 5
ROOM_COLOR = (0, 0, 0)
PLAYER_COLOR = (255, 255, 255)
SWITCH_COLOR = (255, 255, 0)  # Yellow
PATH_COLOR = (100, 100, 100)   # Gray for the path
TOY_COLOR = (255, 0, 0)        # Red for toys
HIGHLIGHT_COLOR = (0, 255, 0)  # Green for highlighted toys
INITIAL_NUM_TOYS = 10  # Initial number of toys to scatter
MOVE_SPEED = 0.3  # Movement speed of the player (slower)
PAUSE_TIME = 5  # Time to pause after reaching the switch (in seconds)

# Difficulty settings
DIFFICULTIES = {
    'easy': {'speed': MOVE_SPEED * 2 / 3, 'toys_per_level': 5},
    'medium': {'speed': MOVE_SPEED, 'toys_per_level': 10},
    'hard': {'speed': MOVE_SPEED * 1.25, 'toys_per_level': 15}
}

# Initialize Pygame
pygame.init()

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Late at Night")  # Change the game name

# Font for the counters
font = pygame.font.SysFont(None, 24)
menu_font = pygame.font.SysFont(None, 36)

# Generate random positions for toys
def generate_toys(num_toys):
    toys = []
    for _ in range(num_toys):
        toy_x = random.randint(10, WIDTH - 10)
        toy_y = random.randint(10, HEIGHT - 10)
        toys.append((toy_x, toy_y))
    return toys

# Show the menu and get difficulty choice
def show_menu():
    menu_options = ['Easy', 'Medium', 'Hard']
    selected_option = 0

    # Title and introduction text
    title_text = menu_font.render("Late At Night", True, (255, 255, 255))
    intro_text_line1 = "Welcome to 'Late At Night', a mysterious journey"
    intro_text_line2 = "through darkness... Use arrow keys to navigate."
    intro_text1 = font.render(intro_text_line1, True, (255, 255, 255))
    intro_text2 = font.render(intro_text_line2, True, (255, 255, 255))
    instructions_text = font.render("Reach the switch to move on and avoid the hidden toys.", True, (255, 255, 255))

    # Calculate the total height of the text to ensure it fits within the window
    total_text_height = title_text.get_height() + intro_text1.get_height() + intro_text2.get_height() + instructions_text.get_height() + 50  # Add 50 for padding

    while True:
        window.fill(ROOM_COLOR)
        # Render and display title and introduction text
        window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4 - total_text_height // 2))
        window.blit(intro_text1, (WIDTH // 2 - intro_text1.get_width() // 2, HEIGHT // 4 - total_text_height // 2 + title_text.get_height()))
        window.blit(intro_text2, (WIDTH // 2 - intro_text2.get_width() // 2, HEIGHT // 4 - total_text_height // 2 + title_text.get_height() + intro_text1.get_height()))
        window.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 4 - total_text_height // 2 + title_text.get_height() + intro_text1.get_height() + intro_text2.get_height()))

        # Render difficulty options below the introduction text
        for idx, option in enumerate(menu_options):
            color = (255, 255, 255) if idx == selected_option else (100, 100, 100)
            option_text = menu_font.render(option, True, color)
            window.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 4 + total_text_height // 2 + idx * 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    return menu_options[selected_option].lower()

# Main game loop
def main():
    global MOVE_SPEED, INITIAL_NUM_TOYS

    difficulty = show_menu()
    MOVE_SPEED = DIFFICULTIES[difficulty]['speed']
    toys_per_level = DIFFICULTIES[difficulty]['toys_per_level']

    # Initialize counters
    level_counter = 1
    total_toys_stepped_counter = 0
    toys_stepped_counter_this_level = 0

    # Initialize toys and toys_stepped_on
    toys = generate_toys(INITIAL_NUM_TOYS)
    toys_stepped_on = set()

    while True:
        # Store the starting point of the current level
        level_starting_point = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        # Check if starting point coincides with any toy point
        while any(level_starting_point == toy for toy in toys):
            level_starting_point = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        initial_level_starting_point = level_starting_point

        # Random position for the switch along the borders of the window
        switch_side = random.choice(["top", "bottom", "left", "right"])
        if switch_side == "top":
            switch_x = random.randint(0, WIDTH - 20)
            switch_y = 0
            SWITCH_WIDTH = 20
            SWITCH_HEIGHT = 5
        elif switch_side == "bottom":
            switch_x = random.randint(0, WIDTH - 20)
            switch_y = HEIGHT - 5
            SWITCH_WIDTH = 20
            SWITCH_HEIGHT = 5
        elif switch_side == "left":
            switch_x = 0
            switch_y = random.randint(0, HEIGHT - 20)
            SWITCH_WIDTH = 5
            SWITCH_HEIGHT = 20
        else:
            switch_x = WIDTH - 5
            switch_y = random.randint(0, HEIGHT - 20)
            SWITCH_WIDTH = 5
            SWITCH_HEIGHT = 20

        # List to store the path
        path = []

        # Dictionary to store the state of movement keys
        movement_keys = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False}

        # Flag to track if the player has reached the switch
        reached_switch = False

        # Main game loop
        while True:
            window.fill(ROOM_COLOR)  # Fill the window with room color

            # Draw the player
            pygame.draw.circle(window, PLAYER_COLOR, (int(level_starting_point[0]), int(level_starting_point[1])), PLAYER_SIZE)

            # Draw the switch
            pygame.draw.rect(window, SWITCH_COLOR, (switch_x, switch_y, SWITCH_WIDTH, SWITCH_HEIGHT))

            # Draw the path
            for point in path:
                pygame.draw.circle(window, PATH_COLOR, (int(point[0]), int(point[1])), PLAYER_SIZE // 2)

            # Draw the toys
            if reached_switch:
                for toy in toys:
                    toy_x, toy_y = toy
                    if toy in toys_stepped_on:
                        pygame.draw.circle(window, HIGHLIGHT_COLOR, (toy_x, toy_y), 3)
                    else:
                        pygame.draw.circle(window, TOY_COLOR, (toy_x, toy_y), 3)
            else:
                for toy in toys_stepped_on:
                    pygame.draw.circle(window, HIGHLIGHT_COLOR, toy, 3)

            # Draw the counters
            counters_text = font.render("Level: " + str(level_counter) + " | Total: " + str(total_toys_stepped_counter) + " | This Level: " + str(toys_stepped_counter_this_level) + " | Difficulty: " + difficulty.capitalize(), True, (255, 255, 255))
            window.blit(counters_text, (10, 10))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Check for Esc key press
                        main()  # Go back to the menu
                    if not reached_switch:
                        if event.key in movement_keys:
                            movement_keys[event.key] = True
                elif event.type == pygame.KEYUP:
                    if event.key in movement_keys:
                        movement_keys[event.key] = False

            # Move the player based on the state of movement keys
            if not reached_switch:
                if movement_keys[pygame.K_LEFT]:
                    level_starting_point = (max(0, level_starting_point[0] - MOVE_SPEED), level_starting_point[1])
                if movement_keys[pygame.K_RIGHT]:
                    level_starting_point = (min(WIDTH, level_starting_point[0] + MOVE_SPEED), level_starting_point[1])
                if movement_keys[pygame.K_UP]:
                    level_starting_point = (level_starting_point[0], max(0, level_starting_point[1] - MOVE_SPEED))
                if movement_keys[pygame.K_DOWN]:
                    level_starting_point = (level_starting_point[0], min(HEIGHT, level_starting_point[1] + MOVE_SPEED))

                # Append the current player position to the path
                path.append(level_starting_point)

                # Check if the player has stepped on a toy
                for toy in toys:
                    toy_x, toy_y = toy
                    if level_starting_point[0] - 3 <= toy_x <= level_starting_point[0] + 3 and level_starting_point[1] - 3 <= toy_y <= level_starting_point[1] + 3:
                        toys_stepped_on.add(toy)
                        total_toys_stepped_counter += 1
                        toys_stepped_counter_this_level += 1
                        level_starting_point = initial_level_starting_point  # Reset player's position to initial starting point

                # Check if the player has reached the switch
                if switch_x <= level_starting_point[0] <= switch_x + SWITCH_WIDTH and switch_y <= level_starting_point[1] <= switch_y + SWITCH_HEIGHT:
                    reached_switch = True
                    level_counter += 1
                    toys_stepped_counter_this_level = 0

                    # When the switch is reached, make all toys visible
                    for toy in toys:
                        if toy in toys_stepped_on:
                            pygame.draw.circle(window, HIGHLIGHT_COLOR, (toy[0], toy[1]), 3)
                        else:
                            pygame.draw.circle(window, TOY_COLOR, (toy[0], toy[1]), 3)
                    pygame.display.update()

                    pygame.time.delay(PAUSE_TIME * 1000)

                    # Generate new toys for the next level
                    toys = generate_toys(INITIAL_NUM_TOYS + toys_per_level * (level_counter - 1))
                    toys_stepped_on = set()  # Reset the stepped on toys
                    path = []  # Reset the path
                    break  # Exit the inner loop to start a new level

            # Update the display
            pygame.display.update()

if __name__ == "__main__":
    main()
