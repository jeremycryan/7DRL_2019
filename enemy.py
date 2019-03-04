from game_object import GameObject
import ai
from sprite_tools import *

class Enemy(GameObject):

    def __init__(self, game, x, y, delay=1, behavior=ai.approach_player):
        GameObject.__init__(self, game, x, y, layer=4)
        idle = SpriteSheet("bug.png", (2, 1), 2);
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
        self.behavior = behavior
        self.delay = delay
        self.timer = 0
        self.game.movers += [self]

    def update(self, dt):
        GameObject.update(self, dt)
        self.timer += dt
        if self.timer >= self.delay:
            self.behavior(self)
            self.timer = 0
        
    def translate(self, dx, dy):
        players = self.map.get((self.x+dx, self.y+dy), ("layer", 5))
        if players:
            self.hit(players[0])
            return True
        return GameObject.translate(self, dx, dy)

    def collide(self, x, y):
        collisions = self.map.get((x, y), "blocking")
        occupants = self.map.get((x, y), ("layer", 4))
        return collisions or occupants

    def hit(self, player):
        print("Oof!")
