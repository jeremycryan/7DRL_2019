#!/usr/bin/env python
import pygame
from constants import *
from sprite_tools import *
from editor import *
from macro import Macro
import time
import sys

class Editor(object):

    def __init__(self, game, populate_demo=False):
        self.game = game
        self.window_surf = pygame.image.load("editor_window.png")
        self.window_x = pygame.image.load("editor_x.png")
        self.next = pygame.image.load("next_page.png")
        self.prev = pygame.image.load("prev_page.png")
        self.window_x_hovered = pygame.image.load("editor_x_hovered.png")
        self.window_xw = self.window_x.get_width()
        self.window_xh = self.window_x.get_height()
        self.macro_tiles = []

        if populate_demo:
            self.macro_tiles = [MoveUp(self, idx = 0),
                                MoveDown(self, idx = 1),
                                MoveLeft(self, idx = 2),
                                MoveRight(self, idx = 3)]

        self.draw_order = [item for item in self.macro_tiles]
        self.tile_containers = []
        cnum = 3
        for i in range(cnum):
            self.tile_containers.append(TileContainer(x = i * 60 + 35, y = 39))
        self.container_width = self.tile_containers[0].surf.get_width()
        self.container_height = self.tile_containers[0].surf.get_height()
        self.carrying = []
        self.macro_length = 3

        self.y = WINDOW_HEIGHT
        self.target_y = 0
        self.active = False
        self.shown = False
        self.page = 0

        self.black = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT)).convert()
        self.black.fill((0, 0, 0))
        self.black.set_alpha(255)

    def populate(self, blocks):
        self.macro_tiles = [item for item in blocks]
        self.draw_order = [item for item in blocks]
        self.carrying = []
        for item in blocks:
            item.in_container = False
            item.scale = 0.5
            item.target_scale = 0.5
            item.reset(hard=True)
        for item in self.tile_containers:
            item.hovered = False
            item.tiles = []

    def show(self):
        self.active = True
        self.target_y = 0
        self.y = WINDOW_HEIGHT
        self.shown = True
        self.populate(self.macro_tiles)
        self.game.mus.set_volume(0.15)

    def hide(self):
        self.target_y = WINDOW_HEIGHT + 5
        self.shown = False
        self.game.mus.set_volume(0.5)

    def toggle(self):
        if self.shown:
            self.hide()
            return False
        else:
            self.show()
            return True

    def draw(self, surf):

        if self.active:
            self.black.set_alpha((255 - 255*self.y/WINDOW_HEIGHT)/2)
            surf.blit(self.black, (0, 0))
            surf.blit(self.window_surf, (0, self.y))
            x, y = 206, self.y + 10
            if self.mouse_in_rect(x, y, self.window_xw, self.window_xh):
                surf.blit(self.window_x_hovered, (x, y))
            else:
                surf.blit(self.window_x, (x, y))
            for c in self.tile_containers:
                c.draw(surf, eyoff = self.y)
            for tile in self.draw_order:
                tile.draw(surf, eyoff = self.y)
            if len(self.macro_tiles) > 12 and self.page == 0:
                surf.blit(self.next, (214, self.y+120))
            if self.page > 0:
                surf.blit(self.prev, (18, self.y+120))

    def mouse_in_rect(self, x, y, w, h):
        mpos = pygame.mouse.get_pos()
        if mpos[0] >= x*SCALE and mpos[0] <= (x + w)*SCALE:
            if mpos[1] >= y*SCALE and mpos[1] <= (y + h)*SCALE:
                return True

        return False

    def update_mouse_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouse_in_rect(206, self.y + 10, self.window_xw, self.window_xh):
                    self.hide()
                if len(self.macro_tiles) > 12 and self.page == 0:
                    if self.mouse_in_rect(214, self.y+120, self.next.get_width(), self.next.get_height()):
                        self.page += 1
                if self.page > 0:
                    if self.mouse_in_rect(18, self.y+120, self.next.get_width(), self.next.get_height()):
                        self.page -= 1                        
        

    def update(self, dt):

        if self.active:
            dy = self.target_y - self.y
            self.y += dy * dt * 10

            for tile in self.macro_tiles:
                tile.update(dt)

        if self.y > WINDOW_HEIGHT:
            self.active = False


    def container_at(self, pos):

        for c in self.tile_containers:
            c.hovered = False
        for c in self.tile_containers:
            if pos[0] >= c.x and pos[0] <= c.x + self.container_width:
                if pos[1] >= c.y and pos[1] <= c.y + self.container_height:
                    c.hovered = True
                    return c
        return 0

    def remove_tile_from_containers(self, tile):
        for c in self.tile_containers:
            if tile in c.tiles:
                c.tiles.remove(tile)

    def get_macro(self):
        macro = Macro(len(self.tile_containers))
        for i, container in enumerate(self.tile_containers):
            if container.tiles:
                macro.add_block(container.tiles[0], i)
            else:
                macro.add_block(False, i)
        return macro


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



if __name__=="__main__":

    a = pygame.display.set_mode(BLIT_SIZE)
    e = Editor(populate_demo=True)
    e.show()


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
