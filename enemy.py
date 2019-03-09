from game_object import GameObject
import ai
import random
from sprite_tools import *
from constants import *


class Enemy(GameObject):

    def __init__(self, game, x, y, delay=1, hp=1, damage=1, behavior=ai.approach_player_smart):
        GameObject.__init__(self, game, x, y, layer=4)
        idle = SpriteSheet("bug.png", (2, 1), 2)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
        self.behavior = behavior
        self.game.movers += [self]
        self.hp = hp
        self.damage = damage
        self.delay = delay
        self.countdown = random.randint(0, delay)
        self.enemy = True
        self.hittable = True

    def update(self, dt):
        GameObject.update(self, dt)

    def move(self):
        if self.countdown:
            self.countdown -= 1
        else:
            self.countdown = self.delay
            if self.behavior(self):
                self.game.delay += 0

    def draw(self, surf):
        GameObject.draw(self, surf)

    def translate(self, dx, dy):
        players = self.map.get((self.x+dx, self.y+dy), ("layer", 5))
        avoid = self.map.get((self.x+dx, self.y+dy), ("avoid"))
        if players:
            self.hit(players[0])
            if abs(dx) > 0:
                self.flipped = dx < 0
            return True
        if avoid:
            return False
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
        player.take_damage(self.damage);


class Bug(Enemy):
    
    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=1.0, behavior=ai.approach_player_smart, hp=1, damage=1)
        readied = SpriteSheet("bug_readied.png", (2, 1), 2)
        self.sprite.add_animation({"Readied": readied})

    def move(self):
        Enemy.move(self)
        if self.countdown == 0:
            self.sprite.start_animation("Readied")
        else:
            self.sprite.start_animation("Idle")


class Ebat(Enemy):

    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=1, hp = 1, behavior=ai.move_random, damage=1)
        idle = SpriteSheet("ebat.png", (2, 1), 2)
        readied = SpriteSheet("ebat_readied.png", (2, 1), 2)
        self.sprite.add_animation({"Idle": idle, "Readied": readied})
        self.sprite.start_animation("Idle")

    def move(self):
        Enemy.move(self)
        if self.countdown == 0:
            self.sprite.start_animation("Readied")
        else:
            self.sprite.start_animation("Idle")


class Bit(Enemy):

    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=0, behavior=ai.charge_player, hp = 1, damage=1)
        idle = SpriteSheet("bit.png", (2, 1), 2)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")

class FlameSpawner(Enemy): #Needs art, flame dude

    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=0, behavior=ai.approach_player_smart_minelay, hp = 1, damage=1)
        idle = SpriteSheet("bit.png", (2, 1), 2)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")

    def spawn(self, x, y):
        GroundHazard(self.game, x, y)

class GroundHazard(Enemy): #Needs art, flame

    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=0, behavior=ai.hazard, hp = 5)
        idle = SpriteSheet("bit.png", (2, 1), 2)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
        self.hittable = False
        self.layer = FLOOR_DETAIL_LAYER
        self.avoid = True

class GroundHazard_Fixed(Enemy): #Needs art, spikes

    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=0, behavior=ai.hazard_fixed, hp = 1)
        idle = SpriteSheet("bit.png", (2, 1), 2)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
        self.hittable = False
        self.layer = FLOOR_DETAIL_LAYER

class Bomb(Enemy): #Needs art, bomb

    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=0, behavior=ai.hazard, hp = 3, damage=1)
        idle = SpriteSheet("bit.png", (2, 1), 2)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
        self.hittable = False
        self.layer = FLOOR_DETAIL_LAYER

