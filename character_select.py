import time
import pygame
from sprite_tools import *
from constants import *
import sys




class CharacterSelect(object):

    def __init__(self, surf):

        self.will_sprite = Sprite(4)
        self.vicky_sprite = Sprite(4)
        self.prava_sprite = Sprite(4)
        self.nick_sprite = Sprite(4)

        self.blip_sound = pygame.mixer.Sound("audio/blip.wav")
        self.blip_sound.set_volume(0.16)
        self.select_sound = pygame.mixer.Sound("audio/character_select.wav")
        
        will = SpriteSheet("images/will.png", (2, 1), 2)
        vicky = SpriteSheet("images/vicky.png", (2, 1), 2)
        prava = SpriteSheet("images/prava.png", (2, 1), 2)
        nick = SpriteSheet("images/nick.png", (2, 1), 2)

        self.will_sprite.add_animation({"Idle": will})
        self.vicky_sprite.add_animation({"Idle": vicky})
        self.prava_sprite.add_animation({"Idle": prava})
        self.nick_sprite.add_animation({"Idle": nick})

        self.sprites = (self.will_sprite,
                        self.nick_sprite,
                        self.vicky_sprite,
                        self.prava_sprite)

        for sprite in self.sprites:
            sprite.start_animation("Idle")

        self.will_sprite.set_position((60, 75))
        self.vicky_sprite.set_position((125, 75))
        self.nick_sprite.set_position((92, 75))
        self.prava_sprite.set_position((158, 75))

        self.back = pygame.image.load("images/char_select.png")
        
        self.surf = surf
        self.blit_surf = pygame.Surface(WINDOW_SIZE)

        self.sel = 0
        self.gray = pygame.Surface((30, 45)).convert()
        self.gray.fill((89, 89, 89))
        self.gray.set_alpha(160)

        self.black = pygame.Surface((WINDOW_SIZE)).convert()
        self.black.fill((0, 0, 0))
        self.black.set_alpha(255)
        self.black_alpha = 255
        self.fadeout = False

        self.main()

    def main(self):

        then = time.time()
        time.sleep(0.001)

        while True:
            now = time.time()
            dt = now - then
            then = now

            if not self.fadeout:
                rate = 500
                self.black_alpha = max(0, self.black_alpha - rate*dt)
                self.black.set_alpha(self.black_alpha)

            if self.fadeout:
                rate = 350
                self.black_alpha = min(255, self.black_alpha + rate*dt)
                self.black.set_alpha(self.black_alpha)
                if self.black_alpha == 255:
                    return self.sel

            self.blit_surf.blit(self.back, (0, 0))
            for (i, sprite) in enumerate(self.sprites):
                if i != self.sel or self.fadeout == False or now%0.2 < 0.1:
                    sprite.draw(self.blit_surf)
                if i == self.sel:
                    sprite.update(dt)
                else:
                    self.blit_surf.blit(self.gray, (sprite.x_pos - 5, sprite.y_pos))

            events = pygame.event.get()
            for event in events:
                if not self.fadeout:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.sel = max(0, self.sel - 1)
                            self.blip_sound.play()
                        if event.key == pygame.K_RIGHT:
                            self.sel = min(3, self.sel + 1)
                            self.blip_sound.play()
                        if event.key == pygame.K_RETURN:
                            self.fadeout = True
                            self.select_sound.play()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            if self.black_alpha:
                self.blit_surf.blit(self.black, (0, 0))
            self.surf.blit(pygame.transform.scale(self.blit_surf, BLIT_SIZE),
                (0, 0))
            pygame.display.flip()
            

if __name__=="__main__":

    pygame.init()
    a = pygame.display.set_mode(BLIT_SIZE)
    CharacterSelect(a)
    pygame.quit()
            
