from game_object import GameObject
from sprite_tools import *

class Player(GameObject):

    def __init__(self, game, x, y):
        GameObject.__init__(self, game, x, y, 5)
        idle = SpriteSheet("will.png", (1, 1), 1);
        self.sprite.add_animation({"IdleRight": idle})
        self.sprite.start_animation("IdleRight")

    def update(self, dt):
        GameObject.update(self, dt)
        
    def draw(self, surf):
        self.sprite.draw(surf)
