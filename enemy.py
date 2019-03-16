from game_object import GameObject
import ai
import random
from sprite_tools import *
from constants import *
from item import *
from block import *
import pygame


class Enemy(GameObject):

    def __init__(self, game, x, y, delay=1, hp=1, damage=0.5, behavior=ai.approach_player_smart):
        GameObject.__init__(self, game, x, y, layer=4)
        idle = SpriteSheet("images/bug.png", (2, 1), 2)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
        self.behavior = behavior
        self.game.movers += [self]
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.delay = delay
        self.map = game.map
        game.map.add_to_cell(self, (x,y))
        self.countdown = random.randint(0, delay)
        self.enemy = True
        self.hittable = True
        self.heart = pygame.image.load("images/heart_small.png")
        self.eheart = pygame.image.load("images/empty_heart_small.png")
        self.heart_width = self.heart.get_width()
        self.width = TILE_SIZE/2
        self.hp_visible = True

    def update(self, dt):
        GameObject.update(self, dt)

    def move(self):
        if self.countdown:
            self.countdown -= 1
        else:
            self.countdown = self.delay
            if self.behavior(self):
                self.game.delay += 0

    def draw_hp(self, surf, x, y):
        if self.hp_visible:
            if self.hp < self.max_hp:
                x_start = x - self.heart_width/2 * self.max_hp
                y_start = y
                x_space = self.heart_width
                hp = self.hp
                for i in range(self.max_hp):
                    if hp >= 1:
                        surf.blit(self.heart, (x_start, y_start))
                    else:
                        surf.blit(self.eheart, (x_start, y_start))
                    x_start += x_space
                    hp -= 1

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
        if self.layer == 4 and random.random() < 0.12:
            self.drop_item()
        if hasattr(self, "death_noise"):
            self.death_noise.play()

    def drop_item(self, value=1):
        direction = random.randint(0,3)
        val = random.randint(0,1+min(self.game.level//3,1))
        r = direction + val*4
        if r == 0:
            BlockItem(self.game, self.x, self.y, Left(editor=self.game.editor))
        elif r == 1:
            BlockItem(self.game, self.x, self.y, Right(editor=self.game.editor))
        elif r == 2:
            BlockItem(self.game, self.x, self.y, Up(editor=self.game.editor))
        elif r == 3:
            BlockItem(self.game, self.x, self.y, Down(editor=self.game.editor))
        elif r == 4:
            BlockItem(self.game, self.x, self.y, AttackLeft(editor=self.game.editor))
        elif r == 5:
            BlockItem(self.game, self.x, self.y, AttackRight(editor=self.game.editor))
        elif r == 6:
            BlockItem(self.game, self.x, self.y, AttackUp(editor=self.game.editor))
        elif r == 7:
            BlockItem(self.game, self.x, self.y, AttackDown(editor=self.game.editor))
        elif r == 8:
            BlockItem(self.game, self.x, self.y, JumpLeft(editor=self.game.editor))
        elif r == 9:
            BlockItem(self.game, self.x, self.y, JumpRight(editor=self.game.editor))
        elif r == 10:
            BlockItem(self.game, self.x, self.y, JumpUp(editor=self.game.editor))
        elif r == 11:
            BlockItem(self.game, self.x, self.y, JumpDown(editor=self.game.editor))

    def take_damage(self, amt):
        self.hp -= amt
        if self.hp <= 0:
            self.die()

    def hit(self, player, rebound=True):
        if rebound:
            self.reboundx = player.x - self.x
            self.reboundy = player.y - self.y
        player.take_damage(self.damage);


class Bug(Enemy):
    
    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=1.0, behavior=ai.approach_player_smart, hp=2)
        readied = SpriteSheet("images/bug_readied.png", (2, 1), 2)
        self.sprite.add_animation({"Readied": readied})
        self.death_noise = self.game.bug_noise

    def move(self):
        Enemy.move(self)
        if self.countdown == 0:
            self.sprite.start_animation("Readied")
        else:
            self.sprite.start_animation("Idle")


class Ebat(Enemy):

    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=1, hp = 1, behavior=ai.move_random)
        idle = SpriteSheet("images/ebat.png", (2, 1), 2)
        readied = SpriteSheet("images/ebat_readied.png", (2, 1), 2)
        self.sprite.add_animation({"Idle": idle, "Readied": readied})
        self.sprite.start_animation("Idle")
        self.death_noise = self.game.bat_noise

    def move(self):
        Enemy.move(self)
        if self.countdown == 0:
            self.sprite.start_animation("Readied")
        else:
            self.sprite.start_animation("Idle")


class Bit(Enemy):

    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=0, behavior=ai.charge_player, hp = 3)
        idle = SpriteSheet("images/ram.png", (2, 1), 2)
        charging = SpriteSheet("images/ram_charge.png", (2, 1), 2)
        self.death_noise = self.game.ram_noise
        self.sprite.add_animation({"Idle": idle, "Charging": charging})
        self.sprite.start_animation("Idle")
        self.charging = False

    def draw(self, surf):
        self.sprite.y_pos -= 5
        self.sprite.x_pos -= 3
        Enemy.draw(self, surf)
        self.sprite.x_pos += 3
        self.sprite.y_pos += 5

class FlameSpawner(Enemy): #Needs art, flame dude

    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=0, behavior=ai.approach_player_smart_minelay, hp = 1)
        idle = SpriteSheet("images/flameboi.png", (2, 1), 2)
        self.death_noise = self.game.firewall_noise
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")

    def spawn(self, x, y):
        GroundHazard(self.game, x, y)
        
class GroundHazard(Enemy): #Needs art, flame

    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=0, behavior=ai.hazard, hp = 5)
        high = SpriteSheet("images/fire.png", (2, 1), 2)
        med = SpriteSheet("images/fire_low.png", (2, 1), 2)
        low = SpriteSheet("images/fire_lower.png", (2, 1), 2)
        self.sprite.add_animation({"High": high,
                                    "Med": med,
                                   "Low": low})
        self.sprite.start_animation("High")
        self.hittable = False
        self.layer = WALL_LAYER
        self.avoid = True
        self.height = 2

        self.hp_visible = False

    def update(self, dt):
        Enemy.update(self, dt)

        if self.height == 2 and self.hp <= 3:
            self.height = 1
            self.sprite.start_animation("Med")
        elif self.height == 1 and self.hp <= 1:
            self.height = 0
            self.sprite.start_animation("Low")
        

class GroundHazard_Fixed(Enemy): #Needs art, spikes

    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=0, behavior=ai.hazard_fixed, hp = 1)
        idle = SpriteSheet("images/spikes.png", (1, 1), 1)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
        self.hittable = False
        self.layer = WALL_LAYER
        self.avoid = True

class Bomb(Enemy): #Needs art, bomb

    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=0, behavior=ai.hazard_bomb, hp = 3)
        idle = SpriteSheet("images/bit.png", (2, 1), 2)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
        self.hittable = False
        self.avoid = True
        self.layer = FLOOR_DETAIL_LAYER

class Hedgehog(Enemy): #Needs art, moves fast

    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y, delay=0, behavior=ai.approach_player_smart_fast, hp = 1, damage=0.5)
        idle = SpriteSheet("images/bit.png", (2, 1), 2)
        self.death_noise = self.game.byte_noise
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")

