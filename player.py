from game_object import GameObject
from constants import *
from sprite_tools import *

class Player(GameObject):

    def __init__(self, game, x, y):
        GameObject.__init__(self, game, x, y, 5, fps = 4)
        idle = SpriteSheet("will.png", (2, 1), 2)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
        self.game.movers += [self]

        # TODO make this dependent on weapon?
        self.attack_damage = 1
        self.delay = PLAYER_DELAY
        self.timer = self.delay
        meter = SpriteSheet("bars.png", (11, 1), 11)
        self.meter_sprite = Sprite(fps = 11.0/self.delay)
        self.meter_sprite.add_animation({"Default": meter})
        self.meter_sprite.start_animation("Default")
        self.update_meter_pos()

    def update(self, dt):
        GameObject.update(self, dt)
        self.timer += dt
        self.prop_to_move = self.timer/self.delay
        if self.timer >= self.delay:
            self.timer = self.delay
        else:
            self.meter_sprite.update(dt)
        self.update_meter_pos()
        
    def draw(self, surf):
        self.meter_sprite.draw(surf)
        GameObject.draw(self, surf)
        
    def translate(self, dx, dy, push=False):
        if not push:
            if not self.ready():
                return False
            self.meter_sprite.start_animation("Default")
            self.timer = 0
        enemies = self.map.get((self.x+dx, self.y+dy), ("layer", 4))
        # TODO: Being pushed into enemies
        if enemies:
            self.hit(enemies[0])
            if abs(dx) > 0:
                self.flipped = dx < 0
            return True
        return GameObject.translate(self, dx, dy)

    def attack(self, dx, dy):
        # TODO generalize this for different weapon types/interactions
        things_hit = self.game.map.get((self.x + dx, self.y + dy), "hittable")
        for thing in things_hit:
            self.hit(thing)

    def hit(self, thing):
        #TODO attack swing animation
        
        thing.take_damage(self.attack_damage)

    def update_meter_pos(self):
        self.meter_sprite.x_pos = self.sprite.x_pos + 4 - self.game.camera.x
        self.meter_sprite.y_pos = self.sprite.y_pos - 7 - self.game.camera.y
        
    def ready(self):
        return self.timer >= self.delay

