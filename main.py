import pygame
import constants
from objects.rect import Rect
from objects.flipper import Flipper
from objects.polygon import Polygon
import math

pygame.init()
screen = pygame.display.set_mode((constants.gameW, constants.gameH))
pygame.display.set_caption("Pinball")

clock = pygame.time.Clock()

# ui elements
playButton = Rect(constants.gameW / 2 - 105, constants.gameH - 200, 210, 63, (0, 255, 0))  
plunger = Rect(constants.gameW - 30, constants.gameH - 60, 20, 60, (0, 0, 255))           

# flippers
leftX = -15 + constants.gameW / 2 - 45
rightX = 15 + constants.gameW / 2 + 45 + 2 * 35
flippers = [
    Flipper(leftX, 550, 90, 20, 5 * math.pi / 36, -5 * math.pi / 36, (200, 0, 0), "L"),
    Flipper(rightX, 550, 90, 20, 31 * math.pi / 36, 41 * math.pi / 36, (200, 0, 0), "R")
]

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    playButton.draw(screen)
    plunger.draw(screen)

    for flipper in flippers:
        flipper.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
