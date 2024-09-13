'''
Snake Pygame Version 1.0
Anthony Andujar
9/13/2024
'''

import pygame
import random

# Initialize pygame
pygame.init()

# Define colors
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set window dimensions and border width
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BORDER_WIDTH = 20

# Define game settings
SNAKE_SPEED_NORMAL = 10
SNAKE_SPEED_HARD = 20

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# High scores for different difficulties
high_scores = {"normal": 0, "hard": 0}

# Custom class for snake head and body with old_x and old_y
class SnakeSegment(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.old_x = x
        self.old_y = y

# Define the snake and world objects
class World:
    def __init__(self, difficulty):
        self.snake_head = self.create_head()
        self.snake_body = []
        self.snake_speed = SNAKE_SPEED_NORMAL if difficulty == "normal" else SNAKE_SPEED_HARD
        self.snake_direction = ""
        self.foods = []
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.timer = self.font.render(f"Score: {self.score}", True, WHITE)
        self.difficulty = difficulty
    
    def create_head(self):
        return SnakeSegment(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 15, 15)

    def create_body(self):
        return SnakeSegment(0, 0, 15, 15)

# Draw the border wall around the screen
def draw_border():
    pygame.draw.rect(screen, WHITE, (0, 0, WINDOW_WIDTH, BORDER_WIDTH))  # Top border
    pygame.draw.rect(screen, WHITE, (0, 0, BORDER_WIDTH, WINDOW_HEIGHT))  # Left border
    pygame.draw.rect(screen, WHITE, (0, WINDOW_HEIGHT - BORDER_WIDTH, WINDOW_WIDTH, BORDER_WIDTH))  # Bottom border
    pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH - BORDER_WIDTH, 0, BORDER_WIDTH, WINDOW_HEIGHT))  # Right border

# Create food as a rectangle
def create_food():
    return pygame.Rect(random.randint(BORDER_WIDTH, WINDOW_WIDTH - 30 - BORDER_WIDTH), 
                       random.randint(BORDER_WIDTH, WINDOW_HEIGHT - 30 - BORDER_WIDTH), 
                       10, 10)

# Generate food at random intervals
def generate_food(world):
    if random.randint(1, 50) == 25:
        world.foods.append(create_food())

# Draw food on the screen
def draw_food(world):
    for food in world.foods:
        pygame.draw.rect(screen, RED, food)

# Check if the snake has eaten the food
def eat_food(world):
    eaten_food = []
    for food in world.foods:
        if world.snake_head.colliderect(food):
            eaten_food.append(food)
            world.snake_body.append(world.create_body())
            world.score += 10  # Increase score
    world.foods = [food for food in world.foods if food not in eaten_food]

# Update the score display
def update_score(world):
    world.timer = world.font.render(f"Score: {world.score}", True, WHITE)

# Check for wall collisions
def wall_collision(world):
    return (world.snake_head.x < BORDER_WIDTH or world.snake_head.x > WINDOW_WIDTH - BORDER_WIDTH or
            world.snake_head.y < BORDER_WIDTH or world.snake_head.y > WINDOW_HEIGHT - BORDER_WIDTH)

# Check if the snake collides with itself
def body_collision(world):
    for body in world.snake_body[3:]:
        if world.snake_head.colliderect(body):
            return True
    return False


# Display game over message centered on the screen
def game_over_message(world):
    game_over_text = world.font.render(f"GAME OVER! Final Score: {world.score}", True, WHITE)
    
    # Get the dimensions of the text
    text_rect = game_over_text.get_rect()
    
    # Center the text on the screen
    text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
    
    # Blit the text to the screen at the centered position
    screen.blit(game_over_text, text_rect)

    # Display high score for the current difficulty
    high_score = high_scores[world.difficulty]
    high_score_text = world.font.render(f"High Score ({world.difficulty.capitalize()}): {high_score}", True, WHITE)
    high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 10))  # Adjusted vertical position
    screen.blit(high_score_text, high_score_rect)


# Display difficulty selection screen
def difficulty_selection():
    global screen
    font = pygame.font.Font(None, 48)
    title_font = pygame.font.Font(None, 72)
    difficulty = ""
    while difficulty == "":
        screen.fill(BLACK)
        
        # Render the title
        title_text = title_font.render("PySnake", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        screen.blit(title_text, title_rect)
        
        # Render difficulty options
        title_text = font.render("Select Difficulty", True, WHITE)
        normal_text = font.render("Press 1 for Normal", True, WHITE)
        hard_text = font.render("Press 2 for Hard", True, WHITE)

        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, WINDOW_HEIGHT // 2 - title_text.get_height() // 2 - 30))
        screen.blit(normal_text, (WINDOW_WIDTH // 2 - normal_text.get_width() // 2, WINDOW_HEIGHT // 2 - normal_text.get_height() // 2 + 10))
        screen.blit(hard_text, (WINDOW_WIDTH // 2 - hard_text.get_width() // 2, WINDOW_HEIGHT // 2 - hard_text.get_height() // 2 + 50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = "normal"
                elif event.key == pygame.K_2:
                    difficulty = "hard"
        
        pygame.display.flip()
        clock.tick(15)
    
    return difficulty


# Move the snake based on its direction
def move_snake(world):
    world.snake_head.old_x, world.snake_head.old_y = world.snake_head.x, world.snake_head.y
    if world.snake_direction == "up":
        world.snake_head.y -= world.snake_speed
    elif world.snake_direction == "down":
        world.snake_head.y += world.snake_speed
    elif world.snake_direction == "left":
        world.snake_head.x -= world.snake_speed
    elif world.snake_direction == "right":
        world.snake_head.x += world.snake_speed

# Sync snake body with the head movement
def sync_snake(world):
    bodies = 0
    for body in world.snake_body:
        if bodies == 0:
            followed_object = world.snake_head
            body.old_x, body.old_y = body.x, body.y
            body.x, body.y = followed_object.old_x, followed_object.old_y
        else:
            followed_object = world.snake_body[bodies-1]
            body.old_x, body.old_y = body.x, body.y
            body.x, body.y = followed_object.old_x, followed_object.old_y
        bodies += 1

# Handle user input for snake direction
def direct_snake(world, event):
    if event.key == pygame.K_UP and world.snake_direction != "down":
        world.snake_direction = "up"
    elif event.key == pygame.K_DOWN and world.snake_direction != "up":
        world.snake_direction = "down"
    elif event.key == pygame.K_LEFT and world.snake_direction != "right":
        world.snake_direction = "left"
    elif event.key == pygame.K_RIGHT and world.snake_direction != "left":
        world.snake_direction = "right"

# Draw the snake on the screen
def draw_snake(world):
    pygame.draw.rect(screen, GREEN, world.snake_head)
    for segment in world.snake_body:
        pygame.draw.rect(screen, GREEN, segment)

# Main game loop
def game_loop():
    global screen  # Declare screen as global
    difficulty = difficulty_selection()  # Get difficulty choice
    world = World(difficulty)
    running = True
    game_over = False
    is_fullscreen = False

    while running:
        screen.fill(BLACK)
        draw_border()  # Draw the border wall
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Exit the game with ESC
                    running = False
                if event.key == pygame.K_F11:  # Toggle full screen with F11
                    if is_fullscreen:
                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Windowed mode
                    else:
                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)  # Full screen
                    is_fullscreen = not is_fullscreen
                elif event.key == pygame.K_r and game_over:  # Retry the game with R
                    game_loop()  # Restart the game
                    return  # Exit the current loop to restart the game
                else:
                    direct_snake(world, event)
        
        if not game_over:
            move_snake(world)
            sync_snake(world)
            generate_food(world)
            eat_food(world)
            update_score(world)

            draw_snake(world)
            draw_food(world)
            screen.blit(world.timer, (20, 20))

            if wall_collision(world) or body_collision(world):
                game_over = True
                # Update high score
                if world.score > high_scores[world.difficulty]:
                    high_scores[world.difficulty] = world.score
        else:
            game_over_message(world)
            retry_text = world.font.render("Press R to Retry", True, WHITE)
            screen.blit(retry_text, (WINDOW_WIDTH // 2 - retry_text.get_width() // 2, WINDOW_HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(15)  # FPS

if __name__ == "__main__":
    while True:
        game_loop()
