import pygame
import time

def draw_grid(screen, nx: int, ny: int, width: int, height: int):
    line_color = (255, 255, 255)

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


pygame.init()

width = 802
height = 802
nx = 20
ny = 20
background_color = (0, 0, 255)  # blue in RGB

screen = pygame.display.set_mode((width, height))
screen.fill(background_color)
draw_grid(screen, nx, ny, width, height)
pygame.display.update()

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

    # update gamestate
    # render
    pygame.display.update()
    # wait
    time.sleep(0.1)