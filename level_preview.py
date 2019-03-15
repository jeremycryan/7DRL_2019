import pygame
import time
from constants import *

class LevelPreview(object):

    def __init__(self, game):

        self.game = game
        self.black = pygame.Surface(WINDOW_SIZE).convert()
        self.black.fill((0, 0, 0))
        self.black_alpha = 255
        self.duration = 1.5

        self.gray = (100, 100, 100)
        self.hp_surf = pygame.Surface((80, 30))
        self.hp_surf.fill(self.gray)
        self.game.render_health(self.hp_surf)

        self.show()


    def show(self):

        start_time = time.time()
        then = start_time
        time.sleep(0.001)
        rate = 400
        
        while True:
            now = time.time()
            dt = now - then
            then = now
            
            pygame.event.pump()

            
            if now - start_time > self.duration:
                self.black_alpha += dt*rate
                if self.black_alpha >= 255:
                    break
                self.black.set_alpha(self.black_alpha)
            else:
                self.black_alpha = max(self.black_alpha - dt*rate, 0)
            

            self.game.screen.fill(self.gray)
            self.black.set_alpha(self.black_alpha)
            self.game.screen.blit(self.hp_surf, (WINDOW_WIDTH/2 - 40,
                                                 WINDOW_HEIGHT/2 - 50))

            self.game.player.update(dt)
            self.game.player.sprite.x_pos = WINDOW_WIDTH/2 - 10
            self.game.player.sprite.y_pos = WINDOW_HEIGHT/2 - 10
            self.game.player.sprite.draw(self.game.screen)            

            
            self.game.screen.blit(self.black, (0, 0))
            self.game.screen_blit.blit(pygame.transform.scale(self.game.screen,
                                                              BLIT_SIZE),
                                                               (0, 0))

            pygame.display.flip()

        self.game.player.sprite.x_pos = self.game.player.x * TILE_SIZE
        self.game.player.sprite.y_pos = self.game.player.y * TILE_SIZE
