import pygame
import sys
from sprite_tools import *
from constants import *

class Game(object):

    def __init__(self):
        pygame.init()
        self.screen_blit = pygame.display.set_mode((640, 480))
        self.screen = pygame.Surface(WINDOW_SIZE)
        self.player = Player()
        self.terminal = Terminal(self)

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


class Player(object):

    def __init__(self):
        idle = SpriteSheet("will.png", (1, 1), 1);

        self.sprite = Sprite()
        self.sprite.add_animation({"IdleRight": idle})
        self.sprite.start_animation("IdleRight")

        self.x_pos = 0
        self.y_pos = 0
        self.sx_pos = self.x_pos * TILE_SIZE
        self.sy_pos = self.y_pos * TILE_SIZE

        self.image = pygame.image.load("will.png")

    def update(self, dt):
        targ_x = self.x_pos * TILE_SIZE
        targ_y = self.y_pos * TILE_SIZE

        self.sx_pos+= (targ_x - self.sprite.x_pos)*dt
        self.sy_pos += (targ_y - self.sprite.y_pos)*dt

        self.sprite.x_pos = int(self.sx_pos)
        self.sprite.y_pos = int(self.sy_pos)
        
        self.sprite.update(dt)

    def draw(self, surf):
        self.sprite.draw(surf)


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
            self.game.player.y_pos += 1
        elif self.text == "mv a":
            self.game.player.x_pos -= 1
        elif self.text == "mv d":
            self.game.player.x_pos += 1
        elif self.text == "mv w":
            self.game.player.y_pos -= 1
        elif self.text == "quit":
            pygame.quit()
            sys.exit()
        
        self.text = ""
                

if __name__=="__main__":

    a = Game()
    a.main()
