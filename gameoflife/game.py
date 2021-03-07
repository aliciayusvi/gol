#TWepilepsy
import pygame
import time
from typing import List

def draw_grid(screen, nx: int, ny: int):
    line_color = foreground_color
    width = screen.get_width()
    height = screen.get_height()
    # draw border
    (x1, y1) = (0, 0)
    (x2, y2) = (width - 1, height - 1)
    pygame.draw.rect(screen, line_color, (x1, y1, x2, y2), width=1)
    
    # draw horizontal lines
    cell_height = (width - 2) / ny
    for i in range(ny - 1):
        y = cell_height * (i + 1)
        pygame.draw.line(screen, line_color, (0, y), (width - 1, y))

    # draw vertical lines
    cell_width = (height - 2) / nx
    for j in range(nx - 1):
        x = cell_width * (j + 1)
        pygame.draw.line(screen, line_color, (x, 0), (x, height - 1))

def draw_cells(screen, board: List[List[int]]):
    cell_color = foreground_color
    rows = len(board)
    cols = len(board[0])
    cell_width = (screen.get_width()-2) // cols
    cell_height = (screen.get_height()-2) // rows
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == 1:
                x = j * cell_width + 1
                y = i * cell_height + 1
                pygame.draw.rect(screen, cell_color, (x, y, cell_width, cell_height))

def update(current_board):
    next_board = new_board(nx, ny)
    for i in range(ny):
        for j in range(nx):
            neighbors = [
                current_board[(i + k) % ny][(j + l) % nx]
                for k in range(-1, 2)
                for l in range(-1, 2)
            ]
            current_state = board[i][j]
            alive_neighbors = sum(neighbors) - current_state
            if current_state == 1 and alive_neighbors not in [2, 3]:
                next_board[i][j] = 0
            elif current_state == 0 and alive_neighbors == 3:
                next_board[i][j] = 1
            else:
                next_board[i][j] = current_state
    return next_board

def new_board(nx: int, ny: int) -> List[List[int]]:
    return [[0 for _ in range(nx)] for _ in range(ny)]

pygame.init()

width = 802
height = 802
nx = 20 # columns
ny = 20 # rows
cell_width = (width - 2) / nx
cell_height = (height - 2) / ny
active_color = (255, 255, 255)
inactive_color = (160, 160, 160)
background_color = (0, 0, 255)  # blue in RGB
foreground_color = active_color

board = new_board(nx, ny)

screen = pygame.display.set_mode((width, height))
screen.fill(background_color)
draw_grid(screen, nx, ny)
draw_cells(screen, board)
pygame.display.update()

# Game loop

keep_playing = True
is_paused = True
foreground_color = inactive_color
while keep_playing:
    # process events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            keep_playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                keep_playing = False
            if event.key == pygame.K_SPACE:
                is_paused = not is_paused
                foreground_color = inactive_color if is_paused else active_color
            if event.key == pygame.K_r:
                board = new_board(nx, ny)
        mouse_click = pygame.mouse.get_pressed()
        if sum(mouse_click) > 0:
            x, y = pygame.mouse.get_pos()
            if (x < 1 or x > width - 1) or (y < 1 or y > height - 1):
                continue
            i = int((y - 1) // cell_height)
            j = int((x - 1) // cell_width)
            board[i][j] = 1 - board[i][j]

    # update gamestate
    if not is_paused:
        board = update(board)
    # render
    screen.fill(background_color)
    draw_grid(screen, nx, ny)
    draw_cells(screen, board)
    pygame.display.update()
    # wait  
    time.sleep(0.1)
