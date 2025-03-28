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
from objects.brick import Brick

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
ball = Ball(plunger.x + plunger.w // 2, constants.gameH - 30, 10, (255, 255, 0))
sounds["spawn"].play()

# Bumpers
bumpers = [
    Bumper(150, 150),
    Bumper(250, 180),
    Bumper(200, 250)
]

score = 0

# Bricks
bricks = []
brick_width = 60
brick_height = 20
cols = 5
rows = 3
x_start = 100
y_start = 100
gap = 10

for row in range(rows):
    for col in range(cols):
        x = x_start + col * (brick_width + gap)
        y = y_start + row * (brick_height + gap)
        bricks.append(Brick(x, y, brick_width, brick_height, 0, 0))
font = pygame.font.SysFont(None, 36)

# Walls
walls = [
    Rect(0, 0, constants.gameW, 10, (255, 255, 255)),              
    Rect(0, 0, 20, constants.gameH, (255, 255, 255)),              
    Rect(constants.gameW - 20, 0, 20, constants.gameH - 100, (255, 255, 255))

]

guiding_wall = Polygon([
    (constants.gameW - 20, constants.gameH - 100),
    (constants.gameW - 60, constants.gameH - 60),
    (constants.gameW - 20, constants.gameH - 60)
], 0, (100, 100, 100))


plunger_force = 0
plunger_charging = False
ball_launched = False
ball_lost = False
lives = 3
game_over = False

def main_menu():
    font_big = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)

    title = font_big.render("Flipperkast", True, (255, 255, 0))
    subtitle = font_small.render("Press SPACE to Start", True, (255, 255, 255))

    while True:
        screen.fill((0, 0, 50))
        screen.blit(title, (constants.gameW // 2 - title.get_width() // 2, 200))
        screen.blit(subtitle, (constants.gameW // 2 - subtitle.get_width() // 2, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        pygame.display.flip()
        clock.tick(60)


main_menu()

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
            elif event.key == pygame.K_r and game_over:
                # Reset all game state
                ball.x = plunger.x + plunger.w // 2
                ball.y = plunger.y - 10
                ball.spd = [0, 0]
                ball_launched = False
                ball_lost = False
                lives = 3
                score = 0
                game_over = False
                plunger_force = 0
                plunger_charging = False
                sounds["spawn"].play()
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
        ball.go(screen, flippers, [], walls, bumpers, bricks) 
    if ball_launched and ball.x > constants.gameW - 50 and ball.y > constants.gameH - 120:
        ball.spd[0] = -2 

    else:
        ball.draw(screen)

    if ball_launched and ball.y - ball.r > constants.gameH:
        ball_lost = True
        ball_launched = False
        lives -= 1
        sounds["destroyed"].play()
    
    if ball_lost:
        if lives <= 0:
            game_over = True
        else:
            ball.x = plunger.x + plunger.w // 2
            ball.y = plunger.y - 10
            ball.spd = [0, 0]
            ball_lost = False
            sounds["spawn"].play()
    
    
    for bumper in bumpers:
        bumper.draw(screen)
        sounds["bumper"].play()


    for brick in bricks:
        brick.draw(screen)
        if brick.checkCollision(ball):
            score += 20
            sounds["target_base"].play()
    for wall in walls:

        for brick in bricks:
            brick.draw(screen)
            if brick.checkCollision(ball):
                score += 20
                sounds["target_base"].play()
                wall.draw(screen)

    guiding_wall.draw(screen)
    
    score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surf, (20, 20))

    lives_surf = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_surf, (20, 60))
    
    if game_over:
        over_surf = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
        screen.blit(over_surf, (constants.gameW // 2 - 150, constants.gameH // 2))
    
    if not ball_launched:
        msg = font.render("Press SPACE to launch!", True, (255, 255, 0))
        screen.blit(msg, (constants.gameW // 2 - 150, 40))
    
    if plunger_charging and plunger_force < 15:
        plunger_force += 0.2
        pygame.draw.rect(screen, (0, 255, 0), (plunger.x, plunger.y - plunger_force * 10, plunger.w, plunger_force * 10))
        
    pygame.display.flip()
    clock.tick(60)