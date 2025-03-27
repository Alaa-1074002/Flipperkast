import pygame, constants
from objects.circle import Circle

class Ball(Circle):
    bounciness = 0.8

    def __init__(self, x, y, r, color, img=None, name="ball"):
        super().__init__(x, y, r, color, [0, 0], name)
        self.img = img
        self.launching = True

    def accelerate(self):
        self.spd[1] += constants.TABLE_ACCELERATION

    # def move(self):
    #     self.x += self.spd[0]
    #     self.y += self.spd[1]

    #     # Simple floor bounce
    #     if self.y + self.r > constants.gameH:
    #         self.y = constants.gameH - self.r
    #         self.spd[1] = -self.spd[1] * self.bounciness

    def draw(self, ctx):
        pygame.draw.circle(ctx, self.color, (int(self.x), int(self.y)), self.r)

    def go(self, ctx):
        self.accelerate()
        self.move()
        self.draw(ctx)
    
    
    def move(self):
        self.x += self.spd[0]
        self.y += self.spd[1]

        # Bounce off floor
        if self.y + self.r > constants.gameH:
            self.y = constants.gameH - self.r
            self.spd[1] = -self.spd[1] * self.bounciness

        # Bounce off ceiling
        if self.y - self.r < 0:
            self.y = self.r
            self.spd[1] = -self.spd[1] * self.bounciness

        # Bounce off left wall
        if self.x - self.r < 0:
            self.x = self.r
            self.spd[0] = -self.spd[0] * self.bounciness

        # Bounce off right wall
        if self.x + self.r > constants.gameW:
            self.x = constants.gameW - self.r
            self.spd[0] = -self.spd[0] * self.bounciness