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