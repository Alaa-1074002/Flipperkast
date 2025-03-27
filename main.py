import pygame
import constants
from objects.rect import Rect
from objects.flipper import Flipper
from objects.polygon import Polygon
from objects.ball import Ball
from objects.bumper import Bumper
import keyboard
import mouse
import pygame.mixer
import math

pygame.init()
pygame.mixer.init()

# Background music
pygame.mixer.music.load("assets/main_theme.ogg")
pygame.mixer.music.play(-1) 

# Sound effects
sounds = {
    "flipper": pygame.mixer.Sound("assets/flipper.wav"),
    "bumper": pygame.mixer.Sound("assets/bumper.wav"),
    "plunger": pygame.mixer.Sound("assets/plunger.wav"),
    "spawn": pygame.mixer.Sound("assets/spawn_ball.wav"),
    "destroyed": pygame.mixer.Sound("assets/ball_destroyed.wav"),
    "bonus": pygame.mixer.Sound("assets/bonus_ball.wav"),
    "game_over": pygame.mixer.Sound("assets/game_over.wav"),
    "spring": pygame.mixer.Sound("assets/spring.wav"),
    "target_base": pygame.mixer.Sound("assets/target_base.wav"),
    "target_group": pygame.mixer.Sound("assets/target_group.wav"),
    "teleport": pygame.mixer.Sound("assets/teleport.wav")
}

screen = pygame.display.set_mode((constants.gameW, constants.gameH))
pygame.display.set_caption("Pinball")
clock = pygame.time.Clock()

# UI elements
playButton = Rect(constants.gameW / 2 - 105, constants.gameH - 200, 210, 63, (0, 255, 0))  
plunger = Rect(constants.gameW - 30, constants.gameH - 60, 20, 60, (0, 0, 255))           

# Flippers
leftX = -15 + constants.gameW / 2 - 45
rightX = 15 + constants.gameW / 2 + 45 + 2 * 35
flippers = [
    Flipper(leftX, 550, 90, 20, 5 * math.pi / 36, -5 * math.pi / 36, (200, 0, 0), "L"),
    Flipper(rightX, 550, 90, 20, 31 * math.pi / 36, 41 * math.pi / 36, (200, 0, 0), "R")
]

# Ball
ball = Ball(380, 100, 10, (255, 255, 0))
sounds["spawn"].play()

# Bumpers
bumpers = [
    Bumper(150, 150),
    Bumper(250, 180),
    Bumper(200, 250)
]

score = 0
font = pygame.font.SysFont(None, 36)

# Walls
walls = [
    Rect(0, 0, constants.gameW, 10, (255, 255, 255)),              
    Rect(0, 0, 20, constants.gameH, (255, 255, 255)),              
    Rect(constants.gameW - 20, 0, 20, constants.gameH, (255, 255, 255))  
]

plunger_force = 0
plunger_charging = False
ball_launched = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        keyboard.listen(event)
        mouse.listen()

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball_launched:
                plunger_charging = True
                sounds["spring"].play()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and plunger_charging:
                plunger_charging = False
                ball_launched = True
                ball.spd[1] = -plunger_force
                plunger_force = 0
                sounds["plunger"].play()

    screen.fill((0, 0, 0))

    playButton.draw(screen)
    plunger.draw(screen)

    for flipper in flippers:
        if flipper.isActive():
            sounds["flipper"].play()
        flipper.draw(screen)

    if ball_launched:
        ball.go(screen)
    else:
        ball.draw(screen)

    for bumper in bumpers:
        bumper.draw(screen)
        if bumper.checkCollision(ball):
            score += 10
            sounds["bumper"].play()

    for wall in walls:
        wall.draw(screen)

    score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surf, (20, 20))

    if plunger_charging and plunger_force < 15:
        plunger_force += 0.2
        pygame.draw.rect(screen, (0, 255, 0), (plunger.x, plunger.y - plunger_force * 10, plunger.w, plunger_force * 10))
        
    pygame.display.flip()
    clock.tick(60)
