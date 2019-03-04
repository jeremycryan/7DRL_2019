from game_object import GameObject
from sprite_tools import *

class Player(GameObject):

    def __init__(self, game, x, y):
        GameObject.__init__(self, game, x, y, 5, fps = 4)
        right_idle = SpriteSheet("will.png", (2, 1), 2);
        left_idle = SpriteSheet("will.png", (2, 1), 2);
        left_idle.reverse(1, 0)
        self.sprite.add_animation({"IdleRight": right_idle,
                                    "IdleLeft": left_idle})
        self.sprite.start_animation("IdleRight")

    def update(self, dt):
        GameObject.update(self, dt)
        
    def draw(self, surf):
        self.sprite.draw(surf)

    def translate(self, dx, dy):
        GameObject.translate(self, dx, dy)
        if (dx < 0):
            self.sprite.start_animation("IdleLeft")
        elif (dx > 0):
            self.sprite.start_animation("IdleRight")
