from objects.entity import Entity

class Circle(Entity):
    def __init__(self, x, y, r, color, spd=[0, 0], name="circle"):
        super().__init__(x, y, color, spd, name)
        self.r = r

    def draw(self, ctx):
        pass  # Ball overrides this
