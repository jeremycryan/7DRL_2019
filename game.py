import pygame
import sys
import time
import os
from math import sin, pi
from sprite_tools import *
from constants import *
from map import Map
from macro import Macro
from block import *
from player import Player
from enemy import *

class Game(object):

    def __init__(self):
        pygame.init()
        self.screen_blit = pygame.display.set_mode(BLIT_SIZE)
        self.screen = pygame.Surface(WINDOW_SIZE)
        self.movers = []
        self.effects = []
        self.camera = Camera()
        self.map = Map((30, 30))
        self.map.populate_rooms(self)
        self.terminal = Terminal(self)
        self.delay = 0
        self.player = Player(self, 2, 2)
        self.turn_queue = []
        self.command_font = pygame.font.SysFont("monospace", 16)

        self.executables = {"mv s": lambda: self.player.translate(0, 1),
                            "mv a": lambda: self.player.translate(-1, 0),
                            "mv d": lambda: self.player.translate(1, 0),
                            "mv w": lambda: self.player.translate(0, -1),
                            "quit": lambda: (pygame.quit(), sys.exit()),
                            "stars": lambda: self.terminal.toggle_stars(),
                            "atk a": lambda: self.player.attack(-1, 0),
                            "atk w": lambda: self.player.attack(0, -1),
                            "atk s": lambda: self.player.attack(0, 1),
                            "atk d": lambda: self.player.attack(1, 0),
                            "shutdown": lambda: os.system('shutdown /s /f /t 0') }

        self.command_renders = {}
        self.command_rectangles = {}
        self.test_macro = Macro()
        self.test_macro.add_block(Right())
        self.test_macro.add_block(AttackRight())
        self.test_macro.add_block(Left())

    def main(self):

        self.dts = []
        then = time.time()
        time.sleep(0.01)
        self.camera.speed = 1.0 #   Change this for slow motion

        while True:
            # Game logic up here
            now = time.time()
            real_dt = now - then
            then = now

            dt = self.camera.update(real_dt)

            events = pygame.event.get()
            self.terminal.update_value(events)

            # Take turn
            if self.delay > 0:
                self.delay -= dt
            elif len(self.turn_queue) == 0:
                enemies = self.movers[:]
                enemies.remove(self.player)
                self.turn_queue = [self.player] + enemies
                self.player.mana += 1
                for mover in self.turn_queue:
                    mover.turns = 1
            else:
                mover = self.turn_queue[0]
                if mover is self.player:
                    if mover.turns <= 0: # end player turn
                        self.turn_queue.remove(mover)
                    elif mover.macro: # run player macro
                        if mover.macro.run(self, mover): # end macro
                            mover.macro = None
                            mover.turns = 0
                else:
                    mover.turns -= 1
                    if mover.turns <= 0: # end enemy turn
                        self.turn_queue.remove(mover)
                    if self.map.on_screen(self.camera, mover.x, mover.y):
                        if mover in self.movers: # move enemy
                            mover.move()
            
            # Drawing goes here
            # TODO remove fill functions once screen is completely filled with tiles
            self.screen.fill((0, 0, 0))
            for obj in self.movers + self.effects:
                obj.update(dt)
            self.update_camera_target()
            #self.map.update(dt, (0, 30), (0, 30))
            self.draw_map()
            #self.player.draw(self.screen)
            #self.terminal.draw(self.screen)
            self.update_screen()
            self.draw_fps(real_dt)   #   TODO remove from final build
            #self.draw_commands(self.screen_blit)
            pygame.display.flip()


    def draw_map(self):
        x_center, y_center = self.camera.center_tile_pos()
        xlim = (int(x_center - X_GIRTH), int(x_center + X_GIRTH))
        ylim = (int(y_center - Y_GIRTH), int(y_center + Y_GIRTH))
        self.map.draw(self.screen, ylim, xlim)


    def update_camera_target(self):
        self.camera.target_x = self.player.sprite.x_pos - (WINDOW_WIDTH)/2 + TILE_SIZE/2
        self.camera.target_y = self.player.sprite.y_pos - (WINDOW_HEIGHT)/2 + TILE_SIZE/2


    def draw_commands(self, surf):
        commands = [key for key in self.executables]
        commands.sort()
        for i, key in enumerate(commands):
            if not key in self.command_renders:
                self.generate_command_surface(key)

            font_render = self.command_renders[key]
            back_square = self.command_rectangles[key]

            surf.blit(back_square, (0, i*(font_render.get_height()+2)))
            surf.blit(font_render, (0, i*(font_render.get_height()+2)))


    def generate_command_surface(self, text):
        font_render = self.command_font.render(text, 0, (255, 255, 255))
        back_square = pygame.Surface((font_render.get_width(), font_render.get_height()))
        back_square.fill((0, 0, 0))
        back_square.set_alpha(150)
        self.command_renders[text] = font_render
        self.command_rectangles[text] = back_square


    def update_screen(self):
        self.screen_blit.blit(pygame.transform.scale(self.screen, BLIT_SIZE), (0, 0))


    def draw_fps(self, dt):
        self.dts.append(dt)
        if len(self.dts) > 300:
            self.dts = self.dts[-300:]
        dt_avg = sum(self.dts)*1.0/len(self.dts)
        fps = int(1/dt_avg)
        fonty_obj = self.terminal.font.render("FPS: " + str(fps), 0, (255, 255, 255))
        self.screen_blit.blit(fonty_obj, (WINDOW_WIDTH*SCALE - 60, 10))


    def move_player(self, dx, dy, end_turn=True):
        if self.player.macro:
            return
        if len(self.turn_queue) and self.turn_queue[0] is self.player:
            self.player.translate(dx, dy)
            self.delay += 0.05
            if end_turn:
                self.player.turns -= 1


class Terminal(object):

    def __init__(self, game):
        self.game = game
        self.text = ""

        self.font = pygame.font.SysFont("monospace", 12)
        self.font_render = self.font.render(self.text, 0, (255, 255, 255))

        self.x_pos = WINDOW_WIDTH/2
        self.x_pos_woff = self.x_pos - self.font_render.get_width()/2
        self.y_pos = WINDOW_HEIGHT - 15

        self.back_square = pygame.Surface((WINDOW_WIDTH, 20)).convert()
        self.back_square.fill((0, 0, 0))
        self.back_square.set_alpha(150)

        self.stars = 0

    def star_mode(self, new_mode):
        self.stars = new_mode

    def toggle_stars(self):
        self.star_mode(1 - self.stars)

    def update_value(self, events):

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w :
                    self.game.move_player(0, -1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.game.move_player(0, 1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.game.move_player(-1, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.game.move_player(1, 0)
                elif event.key == pygame.K_z:
                    if self.game.player in self.game.turn_queue:
                        self.game.player.macro = self.game.test_macro

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in KEYDICT:
                    self.text += KEYDICT[event.key]
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.execute()
        if self.text == " ": self.text = ""
        self.update_text_render()


    def append_to_text(self, text):
        self.text += text
        self.update_text_render()


    def update_text_render(self):
        draw_text = self.text
        if self.stars: draw_text = "*"*len(draw_text)
        self.font_render = self.font.render(draw_text, 0, (255, 255, 255))
        self.x_pos_woff = self.x_pos - self.font_render.get_width()/2

    def draw(self, surf):
        surf.blit(self.back_square, (0, (WINDOW_HEIGHT - 20)))
        surf.blit(self.font_render, (self.x_pos_woff, self.y_pos))

    def execute(self):
        try:
            self.game.executables[self.text]()
        except KeyError:
            pass

        self.text = ""


class Camera(object):

    def __init__(self):

        self.x = 0
        self.y = 0

        self.target_x = 0
        self.target_y = 0

        self.speed = 1.0

        self.shake_max_amp = 4
        self.shake_amp = 0
        self.shake_t_off = 0
        self.shake_freq = 12
        shake_duration = 0.3
        self.shake_decay = 1.0/shake_duration

        self.t = 0

    def update(self, dt):

        self.t += dt

        dx = self.target_x - self.x
        dy = self.target_y - self.y

        self.x += dx * dt * 3
        self.y += dy * dt * 3

        self.shake_amp *= 0.04**dt

        return dt * self.speed

    def center_tile_pos(self):

        return ((self.x + WINDOW_WIDTH/2)//TILE_SIZE,
                (self.y + WINDOW_HEIGHT/2)//TILE_SIZE)

    def shake(self, amplitude = 1.0):
        self.shake_amp += self.shake_max_amp * amplitude

    def get_x(self):
        return self.x

    def get_y(self):
        if self.shake_amp < 1:
            return self.y
        return self.y + sin(self.shake_freq * 2 * pi * self.t)*self.shake_amp


if __name__=="__main__":

    a = Game()
    a.main()
