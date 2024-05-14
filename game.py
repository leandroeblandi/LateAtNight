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
NUM_TOYS = 10  # Initial number of toys to scatter
MOVE_SPEED = 0.3  # Movement speed of the player (slower)
PAUSE_TIME = 5  # Time to pause after reaching the switch (in seconds) - halved

# Initialize Pygame
pygame.init()

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Late at Night")  # Change the game name

# Font for the counters
font = pygame.font.SysFont(None, 24)

# Initialize counters
level_counter = 1
total_toys_stepped_counter = 0
toys_stepped_counter_this_level = 0

# Generate random positions for toys
def generate_toys():
    toys = []
    for _ in range(NUM_TOYS):
        toy_x = random.randint(0, WIDTH)
        toy_y = random.randint(0, HEIGHT)
        toys.append((toy_x, toy_y))
    return toys

toys = generate_toys()

# Set up a set to keep track of which toys have been stepped on
toys_stepped_on = set()

# Main game loop
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
        switch_x = random.randint(0, WIDTH - 20)  # Adjusted width for top border - halved
        switch_y = 0
        SWITCH_WIDTH = 20  # Halved
        SWITCH_HEIGHT = 5   # Halved
    elif switch_side == "bottom":
        switch_x = random.randint(0, WIDTH - 20)  # Adjusted width for bottom border - halved
        switch_y = HEIGHT - 5   # Halved
        SWITCH_WIDTH = 20  # Halved
        SWITCH_HEIGHT = 5   # Halved
    elif switch_side == "left":
        switch_x = 0
        switch_y = random.randint(0, HEIGHT - 20)  # Adjusted height for left border - halved
        SWITCH_WIDTH = 5    # Halved
        SWITCH_HEIGHT = 20  # Halved
    else:
        switch_x = WIDTH - 5   # Halved
        switch_y = random.randint(0, HEIGHT - 20)  # Adjusted height for right border - halved
        SWITCH_WIDTH = 5    # Halved
        SWITCH_HEIGHT = 20  # Halved

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
        pygame.draw.circle(window, PLAYER_COLOR, level_starting_point, PLAYER_SIZE)

        # Draw the switch
        pygame.draw.rect(window, SWITCH_COLOR, (switch_x, switch_y, SWITCH_WIDTH, SWITCH_HEIGHT))

        # Draw the path
        for point in path:
            pygame.draw.circle(window, PATH_COLOR, point, PLAYER_SIZE // 2)

        # Draw the toys and highlight those stepped on
        for toy in toys:
            toy_x, toy_y = toy
            if reached_switch:
                if toy in toys_stepped_on:
                    pygame.draw.circle(window, HIGHLIGHT_COLOR, (toy_x, toy_y), 3)
                else:
                    pygame.draw.circle(window, TOY_COLOR, (toy_x, toy_y), 3)
            else:
                if toy in toys_stepped_on:  # Check if toy is stepped on
                    pygame.draw.circle(window, HIGHLIGHT_COLOR, (toy_x, toy_y), 3)
                else:
                    pygame.draw.circle(window, ROOM_COLOR, (toy_x, toy_y), 3)  # Hide unstepped toys

        # Draw the counters
        level_counter_text = font.render("Level: " + str(level_counter), True, (255, 255, 255))
        window.blit(level_counter_text, (WIDTH - 120, 20))
        
        total_toys_stepped_counter_text = font.render("Total Toys Stepped On: " + str(total_toys_stepped_counter), True, (255, 255, 255))
        window.blit(total_toys_stepped_counter_text, (WIDTH - 220, 50))

        toys_stepped_counter_this_level_text = font.render("Toys Stepped On This Level: " + str(toys_stepped_counter_this_level), True, (255, 255, 255))
        window.blit(toys_stepped_counter_this_level_text, (WIDTH - 250, 80))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
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

        # Update the path with the player's current position
        path.append(level_starting_point)

        # Check if player reached the switch
        if not reached_switch and \
                level_starting_point[0] >= switch_x and level_starting_point[0] <= switch_x + SWITCH_WIDTH \
                and level_starting_point[1] >= switch_y and level_starting_point[1] <= switch_y + SWITCH_HEIGHT:
            # Player reached the switch
            reached_switch = True
            NUM_TOYS += 10  # Increase the number of toys by 10
            level_counter += 1  # Increase level counter
            total_toys_stepped_counter += toys_stepped_counter_this_level  # Update total toys stepped counter
            toys_stepped_counter_this_level = 0  # Reset toys stepped counter for this level
            for toy in toys:
                if toy in toys_stepped_on:  # Only add already stepped on toys to the set
                    toys_stepped_on.add(toy)
            
            # Make all invisible toys visible for 10 seconds
            pygame.display.update()
            for _ in range(int(PAUSE_TIME * 1000 / 100)):  # Divide by 100 to reduce the pause time
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                for toy in toys:
                    toy_x, toy_y = toy
                    if toy in toys_stepped_on:
                        pygame.draw.circle(window, HIGHLIGHT_COLOR, (toy_x, toy_y), 3)
                    else:
                        pygame.draw.circle(window, TOY_COLOR, (toy_x, toy_y), 3)
                pygame.display.update()
                pygame.time.wait(100)  # Wait for 100 milliseconds

            # Reset the game settings
            toys = generate_toys()  # Generate new toys
            break  # Exit the inner game loop to restart with new settings

        # Check if player steps on a toy
        for toy in toys:
            toy_x, toy_y = toy
            if level_starting_point[0] >= toy_x - PLAYER_SIZE and level_starting_point[0] <= toy_x + PLAYER_SIZE \
                    and level_starting_point[1] >= toy_y - PLAYER_SIZE and level_starting_point[1] <= toy_y + PLAYER_SIZE:
                # Player stepped on a toy
                # Mark the toy as stepped on
                toys_stepped_on.add(toy)
                # Increment toys stepped on counters
                toys_stepped_counter_this_level += 1
                total_toys_stepped_counter += 1
                # Reset player position to the starting point of the level
                level_starting_point = initial_level_starting_point
                # Remove the last position from the path
                path = path[:-1]

        # Update the display
        pygame.display.update()
