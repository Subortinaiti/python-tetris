import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 5
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
SELECTED_COLOR = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid Selector")

# Function to draw grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

# Function to get grid coordinates from mouse position
def get_grid_pos(mouse_pos):
    x, y = mouse_pos
    grid_x = x // CELL_SIZE
    grid_y = y // CELL_SIZE
    return grid_x, grid_y

# Main loop
selected_squares = set()
running = True
while running:
    screen.fill(WHITE)
    draw_grid()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click to select/deselect square
                mouse_pos = pygame.mouse.get_pos()
                grid_pos = get_grid_pos(mouse_pos)
                if grid_pos in selected_squares:
                    selected_squares.remove(grid_pos)
                else:
                    selected_squares.add(grid_pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Print selected squares
                print(",")
                print([list(sus) for sus in selected_squares])

    # Highlight selected squares
    for pos in selected_squares:
        rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, SELECTED_COLOR, rect)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
