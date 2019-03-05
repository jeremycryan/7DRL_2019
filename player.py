from game_object import GameObject
from sprite_tools import *

class Player(GameObject):

    def __init__(self, game, x, y):
        GameObject.__init__(self, game, x, y, 5, fps = 4)
        idle = SpriteSheet("will.png", (2, 1), 2);
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
        self.game.movers += [self]

        # TODO make this dependent on weapon?
        self.attack_damage = 1

    def update(self, dt):
        GameObject.update(self, dt)
        print(self.sprite.x_pos, self.sprite.y_pos)

    def translate(self, dx, dy):
        return GameObject.translate(self, dx, dy)

    def attack(self, dx, dy):
        # TODO generalize this for different weapon types/interactions
        things_hit = self.game.map.get((self.x + dx, self.y + dy), "hittable")
        for thing in things_hit:
            self.hit(thing)

    def hit(self, thing):
        #TODO attack swing animation
        
        thing.take_damage(self.attack_damage)

