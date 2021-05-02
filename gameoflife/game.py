#TWepilepsy
import pygame
import time
from typing import List


class Board:

    def __init__(self, rows: int = 20, cols: int = 20):
        # board properties
        self.nx = cols # columns
        self.ny = rows # rows
        self.active_color = (255, 255, 255)
        self.inactive_color = (160, 160, 160)
        self.background_color = (0, 0, 255)  # blue in RGB
        self.foreground_color = self.active_color
        self.board_state = self.new_board()

    def new_board(self) -> List[List[int]]:
        return [[0 for _ in range(self.nx)] for _ in range(self.ny)]

    def draw(self, screen):
        screen.fill(self.background_color)
        self.draw_grid(screen)
        self.draw_cells(screen)

    def draw_grid(self, screen):
        line_color = self.foreground_color
        width = screen.get_width()
        height = screen.get_height()
        # draw border
        (x1, y1) = (0, 0)
        (x2, y2) = (width - 1, height - 1)
        pygame.draw.rect(screen, line_color, (x1, y1, x2, y2), width=1)
        
        # draw horizontal lines
        cell_height = (width - 2) / self.ny
        for i in range(self.ny - 1):
            y = cell_height * (i + 1)
            pygame.draw.line(screen, line_color, (0, y), (width - 1, y))

        # draw vertical lines
        cell_width = (height - 2) / self.nx
        for j in range(self.nx - 1):
            x = cell_width * (j + 1)
            pygame.draw.line(screen, line_color, (x, 0), (x, height - 1))

    def draw_cells(self, screen):
        cell_color = self.foreground_color
        cell_width = (screen.get_width()-2) // self.nx
        cell_height = (screen.get_height()-2) // self.ny
        for i in range(self.ny):
            for j in range(self.nx):
                if self.board_state[i][j] == 1:
                    x = j * cell_width + 1
                    y = i * cell_height + 1
                    pygame.draw.rect(screen, cell_color, (x, y, cell_width, cell_height))

    def update(self):
        next_board_state = self.new_board()
        for i in range(self.ny):
            for j in range(self.nx):
                neighbors = [
                    self.board_state[(i + k) % self.ny][(j + l) % self.nx]
                    for k in range(-1, 2)
                    for l in range(-1, 2)
                ]
                current_state = self.board_state[i][j]
                alive_neighbors = sum(neighbors) - current_state
                if current_state == 1 and alive_neighbors not in [2, 3]:
                    next_board_state[i][j] = 0
                elif current_state == 0 and alive_neighbors == 3:
                    next_board_state[i][j] = 1
                else:
                    next_board_state[i][j] = current_state
        self.board_state = next_board_state

pygame.init()


# screen properties
width = 802
height = 802

# game state properties
rows = 10
cols = 10
board = Board(rows, cols)

# board properties, derived from screen properties and other board properties
cell_width = (width - 2) / board.nx
cell_height = (height - 2) / board.ny

# game initialization
screen = pygame.display.set_mode((width, height))
board.draw(screen)
pygame.display.update()

# Game loop

keep_playing = True
is_paused = True
foreground_color = board.inactive_color
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
                foreground_color = board.inactive_color if is_paused else board.active_color
            if event.key == pygame.K_r:
                board = Board(rows, cols)
        mouse_click = pygame.mouse.get_pressed()
        if sum(mouse_click) > 0:
            x, y = pygame.mouse.get_pos()
            if (x < 1 or x > width - 1) or (y < 1 or y > height - 1):
                continue
            i = int((y - 1) // cell_height)
            j = int((x - 1) // cell_width)
            board.board_state[i][j] = 1 - board.board_state[i][j]

    # update gamestate
    if not is_paused:
        board.update()
    # render
    screen.fill((0, 0, 0))
    board.draw(screen)
    pygame.display.update()
    # wait  
    time.sleep(0.1)
