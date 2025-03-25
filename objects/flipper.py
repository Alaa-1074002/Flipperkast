import pygame, math, constants, keyboard
from pygame import gfxdraw
from objects.rect import Rect

class Flipper(Rect):
    def __init__(self, x, y, w, h, angle, activeAngle, color, name="flipper"):
        super().__init__(x, y, w, h, color)
        self.angle = angle
        self.activeAngle = activeAngle
        self.color = color
        self.name = name
        self.angleCoords = self.prepCoords(angle)
        self.activeAngleCoords = self.prepCoords(activeAngle)

    def prepCoords(self, theta):
        points = [[self.x - self.w/2, self.y - self.h/2],
                [self.x + self.w/2, self.y - self.h/2],
                [self.x + self.w/2, self.y + self.h/2],
                [self.x - self.w/2, self.y + self.h/2]]
        for i in range(len(points)):
            x, y = points[i][0] - self.x, points[i][1] - self.y
            x_new = x * math.cos(theta) - y * math.sin(theta)
            y_new = x * math.sin(theta) + y * math.cos(theta)
            points[i] = [x_new + self.x, y_new + self.y]
        return points

    def isActive(self):
        return (self.name == "L" and keyboard.leftFlipper()) or \
            (self.name == "R" and keyboard.rightFlipper())

    def draw(self, ctx):
        coords = self.activeAngleCoords if self.isActive() else self.angleCoords
        gfxdraw.filled_polygon(ctx, coords, self.color)
        gfxdraw.aapolygon(ctx, coords, self.color)
