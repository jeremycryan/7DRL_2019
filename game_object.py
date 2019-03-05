from constants import *
from sprite_tools import *

class GameObject(object):

    def __init__(self, game, x, y, layer, fps = 4):
        self.sprite = Sprite(fps=fps)
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.flipped = False
        self.layer = layer
        self.game = game
        self.map = game.map
        game.map.add_to_cell(self, (x,y))
        self.sprite.x_pos = self.x * TILE_SIZE
        self.sprite.y_pos = self.y * TILE_SIZE

    def update(self, dt):
        targ_x = self.x * TILE_SIZE - self.game.camera.x
        targ_y = self.y * TILE_SIZE - self.game.camera.y
        self.sprite.x_pos += (targ_x - self.sprite.x_pos)*dt*20
        self.sprite.y_pos += (targ_y - self.sprite.y_pos)*dt*20
        self.sprite.update(dt)

    def draw(self, surf):
        self.sprite.draw(surf, self.flipped)

    def translate(self, dx, dy):
        if self.collide(self.x+dx, self.y+dy):
            return False
        self.map.remove_from_cell(self,(self.x, self.y))
        self.x += dx
        self.y += dy
        self.map.add_to_cell(self, (self.x, self.y))
        if abs(dx) > 0:
            self.flipped = dx < 0
        self.vx = dx
        self.vy = dy
        return True

    def collide(self, x, y):
        collisions = self.map.get((x, y), "blocking")
        occupants = self.map.get((x, y), ("layer", 4))
        players = self.map.get((x, y), ("layer", 5))
        return collisions or occupants or players
