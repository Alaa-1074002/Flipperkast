from objects.polygon import Polygon

class Brick(Polygon):
    def __init__(self, x, y, w, h, min_angle, max_angle):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        points = [
            (x, y),
            (x + w, y),
            (x + w, y + h),
            (x, y + h)
        ]
        color = (150, 75, 0)  # Brown
        super().__init__(points, 0, color)
        self.min = min_angle
        self.max = max_angle

    def checkCollision(self, ball):
        return (
            self.x <= ball.x <= self.x + self.w and
            self.y <= ball.y <= self.y + self.h
        )
