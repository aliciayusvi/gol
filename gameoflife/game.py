import pygame
import time
from typing import List

def draw_grid(screen, nx: int, ny: int):
    line_color = (255, 255, 255)
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
    cell_color = (255, 255, 255)
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


pygame.init()

width = 802
height = 802
nx = 20 # columns
ny = 20 # rows
cell_width = (width - 2) / nx
cell_height = (height - 2) / ny
background_color = (0, 0, 255)  # blue in RGB

board = [[0 for _ in range(nx)] for _ in range(ny)]

screen = pygame.display.set_mode((width, height))
screen.fill(background_color)
draw_grid(screen, nx, ny)
draw_cells(screen, board)
pygame.display.update()


# Game loop

keep_playing = True
while keep_playing:
    # process events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            keep_playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                keep_playing = False
        mouse_click = pygame.mouse.get_pressed()
        if sum(mouse_click) > 0:
            x, y = pygame.mouse.get_pos()
            i = int((y - 1) // cell_height)
            j = int((x - 1) // cell_width)
            board[i][j] = 1 - board[i][j]
    # update gamestate
    
    # render
    screen.fill(background_color)
    draw_grid(screen, nx, ny)
    draw_cells(screen, board)
    pygame.display.update()
    # wait
    time.sleep(0.1)