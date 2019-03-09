from ai import *

class MacroTile(object):

    def __init__(self, editor, x=0, y=0, idx = 0, path=""):
        self.editor = editor
        if not path:
            return
        self.set_surf_from_path(path)
        self.y = 125

        self.x = 30 * idx + 50
        self.tx = x
        self.ty = y

        self.full_w = self.surf.get_width()
        self.full_h = self.surf.get_height()

        self.follow_mouse = False
        self.mouse_clicked = False
        self.in_container = False

        self.scale = 0.5
        self.target_scale = 0.5

    @property
    def w(self):
        return self.surf.get_width() * self.scale

    @property
    def h(self):
        return self.surf.get_height() * self.scale


    def set_surf_from_path(self, path):
        self.surf = pygame.image.load(path + ".png")
        self.surf_small = pygame.image.load(path + "_small.png")

    def update(self, dt):
        dx = self.tx - self.x
        dy = self.ty - self.y

        p = 15.0
        self.x += dx * dt * p
        self.y += dy * dt * p

        if abs(dx) <= 1: self.x = self.tx
        if abs(dy) <= 1: self.y = self.ty

        ds = self.target_scale - self.scale
        self.scale += ds * dt * 20.0

        self.update_from_mouse()

        if not self.in_container and not self.follow_mouse:
            self.ty = 125
            self.tx = 30*self.editor.macro_tiles.index(self) + 50

    def update_from_mouse(self):
        x, y = [p//SCALE for p in pygame.mouse.get_pos()]
        new_click = pygame.mouse.get_pressed()[0]
        if new_click and not self.mouse_clicked:
            if (x >= self.x and x <= self.x + self.w):
                if (y >= self.y and y <= self.y + self.h):
                    self.pickup()
        self.mouse_clicked = new_click
        if not new_click and self.follow_mouse: self.putdown()

        if self.follow_mouse:
            self.tx = x - self.w/2
            self.ty = y - self.h/2
            self.editor.container_at((x, y))


    def draw(self, surf, eyoff = 0):
        xoff = 0
        yoff = eyoff

        surf_to_draw = self.surf
        if self.scale <= 0.6:
            surf_to_draw = self.surf_small
        if abs(self.scale - 1.0) > 0.01:
            surf_to_draw = pygame.transform.scale(surf_to_draw,
                (int(self.full_w*self.scale), int(self.full_h*self.scale)))
            xoff += 0
            yoff += 0

        surf.blit(surf_to_draw, (self.x + xoff, self.y + yoff))

    def pickup(self):
        self.follow_mouse = True
        self.target_scale = 0.5

        self.editor.draw_order.remove(self)
        self.editor.draw_order.append(self)
        self.editor.remove_tile_from_containers(self)

        if len(self.editor.carrying):
            for item in self.editor.carrying:
                if item != self:
                    item.putdown()
        self.editor.carrying.append(self)

    def add_to_container(self):
        self.in_container = True
        self.target_scale = 1.0

    def remove_from_container(self):
        self.in_container = False
        self.target_scale = 0.5
        self.editor.remove_tile_from_containers(self)

    def putdown(self):
        self.follow_mouse = False
        self.target_scale = 0.5

        c = self.editor.container_at((self.x + self.w/2, self.y + self.h/2))
        if c:
            c.add_tile(self)
            self.add_to_container()
        else:
            self.remove_from_container()

class Block (MacroTile):
    def __init__(self, path="", cost=1, duration=0, delay=0.05, editor=None, idx=0):
        MacroTile.__init__(self, editor, idx=idx, path=path)
        self.cost = cost
        self.duration = duration
        self.delay = delay

    def run(self, game, player):
        player.mana -= self.cost
        if player.mana < 0:
            player.mana = 0
            return False
        self.action(player)
        game.delay += self.delay
        player.turns -= self.duration
        return True

    def action(self):
        pass

class Up(Block):
    def __init__(self, *args, **kwargs):
        Block.__init__(self, *args, path="move_up_tile", **kwargs)

    def action(self, player):
        player.translate(*UP, False)

class Down(Block):
    def __init__(self, *args, **kwargs):
        Block.__init__(self, *args, path="move_down_tile", **kwargs)

    def action(self, player):
        player.translate(*DOWN, False)

class Left(Block):
    def __init__(self, *args, **kwargs):
        Block.__init__(self, *args, path="move_left_tile", **kwargs)

    def action(self, player):
        player.translate(*LEFT, False)

class Right(Block):
    def __init__(self, *args, **kwargs):
        Block.__init__(self, *args, path="move_right_tile", **kwargs)

    def action(self, player):
        player.translate(*RIGHT, False)

class AttackUp(Block):
    def __init__(self, *args, **kwargs):
        Block.__init__(self, *args, path="atk_up_tile", **kwargs)
        
    def action(self, player):
        player.attack(*UP, True)

class AttackDown(Block):
    def __init__(self, *args, **kwargs):
        Block.__init__(self, *args, path="atk_down_tile", **kwargs)
    
    def action(self, player):
        player.attack(*DOWN, True)

class AttackLeft(Block):
    def __init__(self, *args, **kwargs):
        Block.__init__(self, *args, path="atk_left_tile", **kwargs)
        
    def action(self, player):
        player.attack(*LEFT, True)

class AttackRight(Block):
    def __init__(self, *args, **kwargs):
        Block.__init__(self, *args, path="atk_right_tile", **kwargs)
        
    def action(self, player):
        player.attack(*RIGHT, True)

