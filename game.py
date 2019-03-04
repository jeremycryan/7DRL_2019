import pygame
import sys
from sprite_tools import *
from constants import *
from player import Player
from map import Map

class Game(object):

    def __init__(self):
        pygame.init()
        self.screen_blit = pygame.display.set_mode((640, 480))
        self.screen = pygame.Surface(WINDOW_SIZE)
        self.map = Map((30, 30))
        self.terminal = Terminal(self)
        self.player = Player(self, 0, 0)

    def main(self):

        while True:
            # Game logic up here
            events = pygame.event.get()
            self.terminal.update_value(events)

            # Drawing goes here
            self.screen.fill((50, 50, 50))
            self.player.update(0.1)
            self.player.draw(self.screen)
            self.terminal.draw(self.screen)
            self.update_screen()
            pygame.display.flip()

    def update_screen(self):
        self.screen_blit.blit(pygame.transform.scale(self.screen, (640, 480)), (0, 0))

class Terminal(object):

    def __init__(self, game):
        self.game = game
        self.text = ""

        self.font = pygame.font.SysFont("monospace", 12)

        self.x_pos = WINDOW_WIDTH/2 - 40
        self.y_pos = WINDOW_HEIGHT - 15

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
        font_render = self.font.render(self.text, 0, (255, 255, 255))
        surf.blit(font_render, (self.x_pos, self.y_pos))
        
    def execute(self):
        if self.text == "mv s":
            self.game.player.translate(0,1)
        elif self.text == "mv a":
            self.game.player.translate(-1,0)
        elif self.text == "mv d":
            self.game.player.translate(1,0)
        elif self.text == "mv w":
            self.game.player.translate(0,-1)
        elif self.text == "quit":
            pygame.quit()
            sys.exit()
        
        self.text = ""
                

if __name__ == "__main__":

    a = Game()
    a.main()
