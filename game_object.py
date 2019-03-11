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
        rebound = self.get_rebound()
        hop = self.get_hop()
        xoff = int(self.game.camera.get_x() + rebound[0])
        yoff = int(self.game.camera.get_y() + rebound[1] + hop)
        self.sprite.x_pos -= xoff
        self.sprite.y_pos -= yoff
        if hasattr(self, "draw_hp"):
            self.draw_hp(surf, self.sprite.x_pos + self.sprite.animations[self.sprite.active_animation].get_frame(0).get_width()/2,
                         self.sprite.y_pos - self.sprite.animations[self.sprite.active_animation].get_frame(0).get_height()/3 + 7 )
        self.sprite.draw(surf, self.flipped)
        self.sprite.y_pos += yoff
        self.sprite.x_pos += xoff

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
        if self.map.get((self.x, self.y), "stairs"):
            self.game.end_level()
        items = self.map.get((self.x, self.y), ("layer",ITEM_LAYER))
        if items:
            self.collect(items)
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

    def collect(self, items):
        for item in items:
            self.map.remove_from_cell(item, (self.x, self.y))


class Slash(GameObject):

    def __init__(self, game, x, y):
        GameObject.__init__(self, game, x, y, FACE_MONKEY_LAYER, fps=12)
        blank = SpriteSheet("images/empty.png", (1, 1), 1)
        left = SpriteSheet("images/slash_left.png", (5, 1), 5)
        right = SpriteSheet("images/slash_left.png", (5, 1), 5)
        right.reverse(1, 0)
        up = SpriteSheet("images/slash_up.png", (5, 1), 5)
        down = SpriteSheet("images/slash_up.png", (5, 1), 5)
        down.reverse(0, 1)
        
        for obj in [left, right, up, down]: obj.repeat = False
        
        self.sprite.add_animation({"Left": left,
                                   "Right": right,
                                   "Down": down,
                                   "Up": up,
                                   "Blank": blank})

        self.sprite.start_animation("Blank")

    def set_direction(self, direction):

        if direction == LEFT:
            self.sprite.start_animation("Left")
        elif direction == RIGHT:
            self.sprite.start_animation("Right")
        elif direction == UP:
            self.sprite.start_animation("Up")
        elif direction == DOWN:
            self.sprite.start_animation("Down")

    def set_position(self, x, y):
        self.game.map.remove_from_cell(self, (self.x, self.y))
        self.x = x
        self.y = y
        self.game.map.add_to_cell(self, (self.x, self.y))

    def start_slash(self, x, y, direction):
        self.set_position(x, y)
        self.set_direction(direction)

    def update(self, dt):
        self.sprite.x_pos = self.x * TILE_SIZE
        self.sprite.y_pos = self.y * TILE_SIZE
        self.sprite.update(dt)
        
        

def converge(val, step, target=0):
    if val > target + step:
        return val - step
    elif val < target - step:
        return val + step
    else:
        return target
