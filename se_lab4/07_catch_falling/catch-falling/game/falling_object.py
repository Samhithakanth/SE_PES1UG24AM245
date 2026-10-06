"""
FallingObject: a simple object that falls straight down.
"""

FALLING_OBJECT_RADIUS = 14


class FallingObject:
    def __init__(self, x, y, radius=FALLING_OBJECT_RADIUS, speed=3, color=(230, 140, 60)):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.color = color

    def update(self):
        self.y += self.speed

    def is_past_bottom(self, height):
        return self.y - self.radius > height
