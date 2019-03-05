from constants import *
from sprite_tools import *

class GameObject(object):

    def __init__(self, game, x, y, layer, fps = 4):
        self.sprite = Sprite(fps=fps)
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.reboundx = 0
        self.reboundy = 0
        self.hop = 0
        self.flipped = False
        self.layer = layer
        self.game = game
        self.map = game.map
        game.map.add_to_cell(self, (x,y))
        self.sprite.x_pos = self.x * TILE_SIZE
        self.sprite.y_pos = self.y * TILE_SIZE

    def update(self, dt):
        targ_x = self.x * TILE_SIZE
        targ_y = self.y * TILE_SIZE
        self.reboundx = converge(self.reboundx, dt/REBOUND_DURATION)
        self.reboundy = converge(self.reboundy, dt/REBOUND_DURATION)
        self.hop = converge(self.hop, dt/HOP_DURATION)
        self.sprite.x_pos += (targ_x - self.sprite.x_pos)*dt*20
        self.sprite.y_pos += (targ_y - self.sprite.y_pos)*dt*20
        self.sprite.update(dt)

    def draw(self, surf):
        self.sprite.x_pos -= int(self.game.camera.get_x())
        self.sprite.y_pos -= int(self.game.camera.get_y())
        rebound = self.get_rebound()
        hop = self.get_hop()
        self.sprite.x_pos -= rebound[0]
        self.sprite.y_pos -= rebound[1]
        self.sprite.y_pos -= hop
        self.sprite.draw(surf, self.flipped)
        self.sprite.y_pos += hop
        self.sprite.x_pos += rebound[0]
        self.sprite.y_pos += rebound[1]
        self.sprite.x_pos += int(self.game.camera.get_x())
        self.sprite.y_pos += int(self.game.camera.get_y())

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
        self.hop = 1
        return True

    def collide(self, x, y):
        collisions = self.map.get((x, y), "blocking")
        occupants = self.map.get((x, y), ("layer", 4))
        players = self.map.get((x, y), ("layer", 5))
        return collisions or occupants or players

    def get_rebound(self):
        x = int(4*REBOUND*((abs(self.reboundx)-0.5)**2-0.25))
        y = int(4*REBOUND*((abs(self.reboundy)-0.5)**2-0.25))
        x = x if self.reboundx > 0 else -x
        y = y if self.reboundy > 0 else -y
        return (x,y)

    def get_hop(self):
        return -int(4*HOP*((abs(self.hop)-0.5)**2-0.25))

def converge(val, step, target=0):
    if val > target + step:
        return val - step
    elif val < target - step:
        return val + step
    else:
        return target
