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
        self.player = Player(self, 0, 0)
        self.terminal = Terminal(self)
        Enemy(self, 5, 5)
        self.executables = { "mv s": lambda: self.player.translate(0, 1),
        					"mv a": lambda: self.player.translate(-1, 0), 
        					"mv d": lambda: self.player.translate(1, 0),
        					"mv w": lambda: self.player.translate(0, -1),
        					"stars": lambda: self.terminal.toggle_stars(),
        					"quit": lambda: (pygame.quit(), sys.exit()),
        					"shutdown": lambda: os.system('shutdown /s /f /t 0') }


    def main(self):

        then = time.time()
        time.sleep(0.01)
        while True:
            # Game logic up here
            now = time.time()
            dt = now - then
            then = now
            
            events = pygame.event.get()
            self.terminal.update_value(events)

            # Drawing goes here
            self.screen.fill((50, 50, 50))
            #self.player.update(dt)
            self.map.update(dt, (0, 30), (0, 30))
            self.map.draw(self.screen, (0, 30), (0, 30))
            #self.player.draw(self.screen)
            self.terminal.draw(self.screen)
            self.update_screen()
            self.draw_commands(self.screen_blit)
            pygame.display.flip()


    def draw_commands(self, surf):
        for i in range(0, len([*self.executables])):
            font = pygame.font.SysFont("monospace", 16)
            font_render = font.render([*self.executables][i], 0, (255, 255, 255))
            back_square = pygame.Surface(font.size(([*self.executables][i]))).convert()
            back_square.fill((0, 0, 0))
            back_square.set_alpha(150)

            surf.blit(back_square, (0, i*(font.size(([*self.executables][i]))[1] + 2)))
            surf.blit(font_render, (0, i*(font.size(([*self.executables][i]))[1] + 2)))


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

        pass
                

if __name__=="__main__":

    a = Game()
    a.main()
