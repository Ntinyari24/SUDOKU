import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
WINDOW_SIZE = 600
GRID_SIZE = 9
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
WHITE = (255, 255, 255)
PINK = (255, 182, 193)
BLACK = (0, 0, 0)
clock = pygame.time.Clock()


# Validate cell value
def validvalue(grid, row, col, num):
    if grid[row][col] != 0:  # Check if the cell is empty
        return False
    for x in range(9):
        if grid[row][x] == num or grid[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    return True

# Generate a dynamic Sudoku grid
def generate_sudoku():
    grid = [[0 for _ in range(9)] for _ in range(9)]

    def fill_grid():
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for value in numbers:
                        if validvalue(grid, i, j, value):
                            grid[i][j] = value
                            if fill_grid():
                                return True
                            grid[i][j] = 0
                    return False
        return True

    fill_grid()
    return grid



def remove_numbers(grid, difficulty=40):
    def has_unique_solution(grid):
        """Check if the grid has exactly one solution."""
        solutions = 0

        def solve():
            nonlocal solutions
            for i in range(9):
                for j in range(9):
                    if grid[i][j] == 0:
                        for num in range(1, 10):
                            if validvalue(grid, i, j, num):
                                grid[i][j] = num
                                solve()
                                grid[i][j] = 0
                        return
            solutions += 1

        solve()
        return solutions == 1

    removed = 0
    while removed < difficulty:
        i, j = random.randint(0, 8), random.randint(0, 8)
        if grid[i][j] != 0:
            backup = grid[i][j]
            grid[i][j] = 0
            if not has_unique_solution(grid):
                grid[i][j] = backup  # Restore if multiple solutions exist
            else:
                removed += 1
    return grid

# Drawing functions
def drawlines(win):
    for i in range(10):
        width = 4 if i % 3 == 0 else 1
        pygame.draw.line(win, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), width)
        pygame.draw.line(win, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), width)

def draw_numbers(window, grid):
    font = pygame.font.Font(None, 40)
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                text = font.render(str(grid[i][j]), True, BLACK)
                window.blit(text, (j * CELL_SIZE + 15, i * CELL_SIZE + 10))


def highlightbox(window, x, y):
    pygame.draw.rect(window, WHITE, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)



# Initialize game
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Sudoku by HAPUCH")
running = True
grid = remove_numbers(generate_sudoku())
value, x, y = 0, 0, 0

while running:
    window.fill(PINK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x, y = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
        elif event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_9:
                value = event.key - pygame.K_0
                if validvalue(grid, x, y, value):
                    grid[x][y] = value

    # Draw grid and numbers
    drawlines(window)
    draw_numbers(window, grid)
    highlightbox(window,x,y)
    pygame.display.update()

pygame.quit()
   



                                                                    