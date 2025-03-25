import pygame, constants, math

from pygame import gfxdraw

from img import images


import os
from win32api import GetSystemMetrics
windowX = GetSystemMetrics(0)/2 - constants.gameW/2
windowY = GetSystemMetrics(1)/2 - constants.gameH/2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (windowX, windowY)

pygame.init()
from pygame.locals import NOFRAME, DOUBLEBUF
ctx = pygame.display.set_mode((constants.gameW,constants.gameH), DOUBLEBUF)
ctx.set_alpha(None)
pygame.display.set_caption("Pinball")
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ctx.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()