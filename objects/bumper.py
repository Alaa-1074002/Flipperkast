import pygame
from objects.circle import Circle
import math

class Bumper(Circle):
    def __init__(self, x, y, r=20, color=(255, 0, 0)):
        super().__init__(x, y, r, color)
    
    def draw(self, ctx):
        pygame.draw.circle(ctx, self.color, (int(self.x), int(self.y)), self.r)

    def checkCollision(self, ball):
        dx = self.x - ball.x
        dy = self.y - ball.y
        dist = math.hypot(dx, dy)
        if dist < self.r + ball.r:
            norm_x = dx / dist
            norm_y = dy / dist
            dot = ball.spd[0]*norm_x + ball.spd[1]*norm_y
            ball.spd[0] -= 2 * dot * norm_x
            ball.spd[1] -= 2 * dot * norm_y
            return True
        return False
