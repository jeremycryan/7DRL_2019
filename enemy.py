from game_object import GameObject
import ai
from sprite_tools import *

class Enemy(GameObject):

    def __init__(self, game, x, y, delay=1, behavior=ai.move_random):
        GameObject.__init__(self, game, x, y, layer=4)
        idle = SpriteSheet("bug.png", (2, 1), 2);
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
        self.behavior = behavior
        self.delay = delay
        self.timer = 0

    def update(self, dt):
        GameObject.update(self, dt)
        self.timer += dt
        if self.timer >= self.delay:
            self.behavior(self)
            self.timer = 0
        
    def translate(self, dx, dy):
        return GameObject.translate(self, dx, dy)
