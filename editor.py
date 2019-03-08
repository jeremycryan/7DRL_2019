#!/usr/bin/env python
import pygame
from constants import *
from sprite_tools import *
import time
import sys

class Editor(object):

    def __init__(self):
        self.window_surf = pygame.image.load("editor_window.png")
        self.window_x = pygame.image.load("editor_x.png")
        self.window_xw = self.window_x.get_width()
        self.window_xh = self.window_x.get_height()
        self.macro_tiles = []#[MacroTile(self, 0, 0, idx = 0, path= "move_left_tile"),
                            #MacroTile(self, 0, 0, idx = 1, path= "move_up_tile"),
                            #MacroTile(self, 0, 0, idx = 2, path= "move_down_tile"),
                            #MacroTile(self, 0, 0, idx = 3, path= "move_right_tile")]
        self.draw_order = [item for item in self.macro_tiles]
        self.tile_containers = []
        cnum = 3
        for i in range(cnum):
            self.tile_containers.append(TileContainer(x = i * 60 + 35, y = 60))
        self.container_width = self.tile_containers[0].surf.get_width()
        self.container_height = self.tile_containers[0].surf.get_height()
        self.carrying = []
        self.macro_length = 3

        self.y = WINDOW_HEIGHT
        self.target_y = 0

    def draw(self, surf):

        surf.blit(self.window_surf, (0, self.y))
        surf.blit(self.window_x, (206, self.y + 10))
        for c in self.tile_containers:
            c.draw(surf, eyoff = self.y)
        for tile in self.draw_order:
            tile.draw(surf, eyoff = self.y)

    def update(self, dt):

        dy = self.target_y - self.y
        self.y += dy * dt * 10

        for tile in self.macro_tiles:
            tile.update(dt)


    def container_at(self, pos):

        for c in self.tile_containers:
            c.hovered = False
            if pos[0] >= c.x and pos[0] <= c.x + self.container_width:
                if pos[1] >= c.y and pos[1] <= c.y + self.container_height:
                    c.hovered = True
                    return c
        return 0

    def remove_tile_from_containers(self, tile):
        for c in self.tile_containers:
            if tile in c.tiles:
                c.tiles.remove(tile)


class TileContainer(object):

    def __init__(self, x = 0, y = 0):

        self.surf = pygame.image.load("editor_blank.png")
        self.hover_surf = pygame.image.load("editor_blank_hover.png")
        self.x = x
        self.y = y

        self.tiles = []

        self.hovered = False


    def draw(self, surf, eyoff = 0):

        if self.hovered:
            surf.blit(self.hover_surf, (self.x, self.y + eyoff))
        else:
            surf.blit(self.surf, (self.x, self.y + eyoff))


    def add_tile(self, tile):

        tile.tx = self.x
        tile.ty = self.y
        for item in self.tiles:
            item.remove_from_container()
        self.tiles = [tile]


class MacroTile(object):

    def __init__(self, editor, x=0, y=0, idx = 0, path="move_right_tile"):
        self.editor = editor
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
        if abs(dx) < 1: self.x = self.tx
        if abs(dy) < 1: self.y = self.ty

        p = 15.0
        self.x += dx * dt * p
        self.y += dy * dt * p

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
        else:
            for c in self.editor.tile_containers:
                if not c.tiles:
                    c.hovered = False


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


if __name__=="__main__":

    a = pygame.display.set_mode(BLIT_SIZE)
    e = Editor()
    blit = pygame.Surface(WINDOW_SIZE)

    then = time.time()
    time.sleep(0.001)

    while True:

        now = time.time()
        dt = now - then
        then = time.time()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        blit.fill((100, 100, 100))
        e.update(dt)
        e.draw(blit)
        a.blit(pygame.transform.scale(blit, BLIT_SIZE), (0, 0))
        pygame.display.flip()
