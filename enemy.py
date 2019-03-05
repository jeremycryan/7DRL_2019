from game_object import GameObject
import ai
import random
from sprite_tools import *

class Enemy(GameObject):

    def __init__(self, game, x, y, delay=4.0, behavior=ai.approach_player_smart, hp = 1):
        GameObject.__init__(self, game, x, y, layer=4)
        idle = SpriteSheet("bug.png", (2, 1), 2)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
        self.behavior = behavior
        self.delay = delay
        self.timer = delay*random.random()
        self.prop_to_move = 0
        self.game.movers += [self]

        meter = SpriteSheet("circles.png", (16, 1), 16)
        self.meter_sprite = Sprite(fps = 16.0/delay)
        self.meter_sprite.add_animation({"Default": meter})
        self.meter_sprite.start_animation("Default")
        self.update_meter_pos

        self.hp = hp
        self.enemy = True
        self.hittable = True

    def update(self, dt):
        GameObject.update(self, dt)
        self.timer += dt
        self.prop_to_move = self.timer/self.delay
        if self.timer >= self.delay:
            self.behavior(self)
            self.timer -= self.delay
            self.meter_sprite.start_animation("Default")
        self.update_meter_pos()
        self.meter_sprite.update(dt)

    def draw(self, surf):
        self.meter_sprite.draw(surf)
        GameObject.draw(self, surf)

    def update_meter_pos(self):
        self.meter_sprite.x_pos = self.sprite.x_pos + 5 - self.game.camera.x
        self.meter_sprite.y_pos = self.sprite.y_pos - 1 - self.game.camera.y
        
    def translate(self, dx, dy):
        players = self.map.get((self.x+dx, self.y+dy), ("layer", 5))
        if players:
            self.hit(players[0])
            if abs(dx) > 0:
                self.flipped = dx < 0
            return True
        return GameObject.translate(self, dx, dy)

    def die(self):
        #TODO death animation
        self.game.map.remove_from_cell(self, (self.x, self.y))
        self.game.movers.remove(self)

    def take_damage(self, amt):
        self.hp -= amt
        if self.hp <= 0:
            self.die()

    def collide(self, x, y):
        collisions = self.map.get((x, y), "blocking")
        occupants = self.map.get((x, y), ("layer", 4))
        return collisions or occupants

    def hit(self, player):
        self.reboundx = player.x - self.x
        self.reboundy = player.y - self.y
        self.game.camera.shake()
        print("Oof!")
