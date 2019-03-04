from game_object import GameObject
from sprite_tools import *

class Player(GameObject):

    def __init__(self, game, x, y):
        GameObject.__init__(self, game, x, y, 5, fps = 4)
        idle = SpriteSheet("will.png", (2, 1), 2);
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")

    def update(self, dt):
        GameObject.update(self, dt)

    def translate(self, dx, dy):
        return GameObject.translate(self, dx, dy)
