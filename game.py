import pygame
import sys
import time
import os
from sprite_tools import *
from constants import *
from map import Map
from player import Player
from enemy import Enemy

class Game(object):

    def __init__(self):
        pygame.init()
        self.screen_blit = pygame.display.set_mode(BLIT_SIZE)
        self.screen = pygame.Surface(WINDOW_SIZE)
        self.map = Map((30, 30))
        self.map.populate_random(self)
        self.movers = []
        self.player = Player(self, 0, 0)
        self.terminal = Terminal(self)
        Enemy(self, 5, 5)
        self.camera = Camera()
        self.executables = { "mv s": lambda: self.player.translate(0, 1),
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


    def main(self):

        then = time.time()
        time.sleep(0.01)

        while True:
            # Game logic up here
            now = time.time()
            dt = now - then
            then = now

            dt = self.camera.update(dt)
            
            events = pygame.event.get()
            self.terminal.update_value(events)

            # Drawing goes here
            # TODO remove fill functions once screen is completely filled with tiles
            self.screen_blit.fill((50, 50, 50))
            self.screen.fill((50, 50, 50))
            for obj in self.movers:
                obj.update(dt)
            self.update_camera_target()
            #self.map.update(dt, (0, 30), (0, 30))
            self.map.draw(self.screen, (0, 16), (0, 12))
            #self.player.draw(self.screen)
            self.terminal.draw(self.screen)
            self.update_screen()
            self.draw_commands(self.screen_blit)
            pygame.display.flip()


    def update_camera_target(self):
        self.camera.target_x = self.player.sprite.x_pos - (WINDOW_WIDTH)/2
        self.camera.target_y = self.player.sprite.y_pos - (WINDOW_HEIGHT)/2


    def draw_commands(self, surf):
        for i in range(0, len([key for key in self.executables])):
            font = pygame.font.SysFont("monospace", 16)
            font_render = font.render([key for key in self.executables][i], 0, (255, 255, 255))
            back_square = pygame.Surface(font.size(([key for key in self.executables][i]))).convert()
            back_square.fill((0, 0, 0))
            back_square.set_alpha(150)

            surf.blit(back_square, (0, i*(font.size(([key for key in self.executables][i]))[1] + 2)))
            surf.blit(font_render, (0, i*(font.size(([key for key in self.executables][i]))[1] + 2)))


    def update_screen(self):
        self.screen_blit.blit(pygame.transform.scale(self.screen, BLIT_SIZE), (0, 0))


class Terminal(object):

    def __init__(self, game):
        self.game = game
        self.text = ""

        self.font = pygame.font.SysFont("monospace", 12)

        self.x_pos = WINDOW_WIDTH/2 - 40
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
            if event.type == pygame.KEYDOWN:
                if event.key in KEYDICT:
                    self.text += KEYDICT[event.key]
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.execute()
        if self.text == " ": self.text = ""

    def draw(self, surf):
        surf.blit(self.back_square, (0, (WINDOW_HEIGHT - 20)))
        draw_text = self.text
        if self.stars: draw_text = "*"*len(draw_text)
        font_render = self.font.render(draw_text, 0, (255, 255, 255))
        surf.blit(font_render, (self.x_pos, self.y_pos))

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

    def update(self, dt):
        
        dx = self.target_x - self.x
        dy = self.target_y - self.y

        self.x += dx * dt * 2
        self.y += dy * dt * 2

        return dt
                

if __name__=="__main__":

    a = Game()
    a.main()
