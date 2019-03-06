from game_object import GameObject
import ai
import random
from sprite_tools import *

class Enemy(GameObject):

    def __init__(self, game, x, y, delay=3.0, behavior=ai.approach_player_smart, hp = 1):
        GameObject.__init__(self, game, x, y, layer=4)
        idle = SpriteSheet("bug.png", (2, 1), 2)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
        self.behavior = behavior
        self.delay = delay
        self.timer = delay*random.random()
        self.prop_to_move = 0
        self.game.movers += [self]

        meter = SpriteSheet("bars.png", (11, 1), 11)
        self.meter_sprite = Sprite(fps = 11.0/delay)
        self.meter_sprite.add_animation({"Default": meter})
        self.meter_sprite.start_animation("Default")
        self.update_meter_pos()

        self.hp = hp
        self.enemy = True
        self.hittable = True

    def update(self, dt):
        GameObject.update(self, dt)
        self.timer += dt
        self.prop_to_move = self.timer/self.delay
        if self.timer >= self.delay:
            self.behavior(self)
            self.timer = 0
            self.meter_sprite.start_animation("Default")
        self.update_meter_pos()
        self.meter_sprite.update(dt)

    def draw(self, surf):
        self.meter_sprite.draw(surf)
        GameObject.draw(self, surf)

    def update_meter_pos(self):
        self.meter_sprite.x_pos = self.sprite.x_pos + 4 - self.game.camera.x
        self.meter_sprite.y_pos = self.sprite.y_pos - 3 - self.game.camera.y
        
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

    def hit(self, player):
        self.reboundx = player.x - self.x
        self.reboundy = player.y - self.y
        self.game.camera.shake()
        print("Oof!")

class Ebat(Enemy):

    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=3.0, behavior=ai.move_random_or_screech, hp = 1)
        idle = SpriteSheet("ebat.png", (2, 1), 2)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
    
        self.moved_last_turn = False  
