#TWepilepsy
import typing_extensions
import pygame
import time
from typing import List

class Entity:

    def update(self):
        pass
    
    def draw(self, screen):
        pass

    def do_events(self, events):
        pass


class Board(Entity):

    def __init__(self, rows: int = 20, cols: int = 20, width: int = 802, height: int = 802):
        # board properties
        self.nx = cols # columns
        self.ny = rows # rows
        self.active_color = (255, 255, 255)
        self.inactive_color = (160, 160, 160)
        self.background_color = (0, 0, 255)  # blue in RGB
        self.width = width
        self.height = height
        self.board_state = self.new_board()
        self.is_active = False
    

    def get_foreground_color(self):
        return self.active_color if self.is_active else self.inactive_color

    def get_cell_width(self):
        return (self.height - 2) // self.nx

    def get_cell_height(self):
        return (self.width - 2) // self.ny

    def set_active(self, active: bool):
        self.is_active = active

    def reset(self):
        self.board_state = self.new_board()

    def new_board(self) -> List[List[int]]:
        return [[0 for _ in range(self.nx)] for _ in range(self.ny)]

    def draw(self, screen):
        screen.fill(self.background_color)
        self.draw_grid(screen)
        self.draw_cells(screen)

    def draw_grid(self, screen):
        line_color = self.get_foreground_color()
        width = screen.get_width()
        height = screen.get_height()
        # draw border
        (x1, y1) = (0, 0)
        (x2, y2) = (width - 1, height - 1)
        pygame.draw.rect(screen, line_color, (x1, y1, x2, y2), width=1)
        
        # draw horizontal lines
        for i in range(self.ny - 1):
            y = self.get_cell_height() * (i + 1)
            pygame.draw.line(screen, line_color, (0, y), (width - 1, y))

        # draw vertical lines
        for j in range(self.nx - 1):
            x = self.get_cell_width() * (j + 1)
            pygame.draw.line(screen, line_color, (x, 0), (x, height - 1))

    def draw_cells(self, screen):
        cell_color = self.get_foreground_color()
        for i in range(self.ny):
            for j in range(self.nx):
                if self.board_state[i][j] == 1:
                    x = j * self.get_cell_width() + 1
                    y = i * self.get_cell_height() + 1
                    pygame.draw.rect(screen, cell_color, (x, y, self.get_cell_width(), self.get_cell_height()))

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

    def click(self, i, j):
        self.board_state[i][j] = 1 - self.board_state[i][j]

    def do_events(self, events):
        mouse_click = pygame.mouse.get_pressed()
        if sum(mouse_click) > 0:
            x, y = pygame.mouse.get_pos()
            if (x < 1 or x > self.width - 1) or (y < 1 or y > self.height - 1):
                return
            i = int((y - 1) // self.get_cell_height())
            j = int((x - 1) // self.get_cell_width())
            self.click(i, j)

class Game:
    
    def __init__(self, width: int, height: int) -> None:
        self.keep_playing = True
        self.is_paused = True
        self.entities: List[Entity] = []
        self.width = width
        self.height = height
        self.screen = None

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for entity in self.entities:
            entity.draw(screen)
        pygame.display.update()

    def do_events(self, events):
        self.do_game_events(events)
        for entity in self.entities:
            entity.do_events(events)

    def do_game_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.keep_playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.is_paused = not self.is_paused


    def update(self):
        for entity in self.entities:
            entity.update()

    def game_loop(self) -> None:
        while self.keep_playing:
            # process events
            events = pygame.event.get()
            self.do_events(events)

            # update gamestate
            if not self.is_paused:
                self.update()
            # render
            self.draw(self.screen)
            
            # board.draw(screen)
            pygame.display.update()

            # wait  
            time.sleep(0.1)

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.game_loop()


class GameOfLife(Game):

    def __init__(self) -> None:
        super().__init__(802, 802)
        self.rows = 10
        self.cols = 10
        self.board = Board(self.rows, self.cols, self.width, self.height)
        self.entities.append(self.board)

    def do_game_events(self, events):
        super().do_game_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.board.set_active(not self.is_paused)
                if event.key == pygame.K_r:
                    self.board.reset()
                if event.key == pygame.K_ESCAPE:
                    self.keep_playing = False


game = GameOfLife()

game.run()
