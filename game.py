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
from editor import *
from character_select import *

class Game(object):

    def __init__(self):
        pygame.mixer.init(44200, -16, 2, 1024)
        pygame.init()

        self.bug_noise = pygame.mixer.Sound("audio/bug.wav")
        self.bat_noise = pygame.mixer.Sound("audio/ebat.wav")
        self.swish_noise = pygame.mixer.Sound("audio/swish.wav")
        self.ram_noise = pygame.mixer.Sound("audio/ram.wav")
        self.firewall_noise = pygame.mixer.Sound("audio/firewall.wav")
        self.byte_noise = pygame.mixer.Sound("audio/byte.wav")
        self.hit_noise = pygame.mixer.Sound("audio/hit.wav")
        self.mus = pygame.mixer.Sound("audio/music.wav")
        self.mus.set_volume(0.5)
        self.mus.play(-1)
        
        self.swish_noise.set_volume(0.7)
        self.ram_noise.set_volume(0.6)
        self.byte_noise.set_volume(0.4)
        self.bat_noise.set_volume(0.8)
        self.hit_noise.set_volume(0.4)
        
        self.screen_blit = pygame.display.set_mode(BLIT_SIZE)
        self.screen = pygame.Surface(WINDOW_SIZE)
        self.editor = Editor(self)
        self.sel = CharacterSelect(self.screen_blit).sel
        self.player = Player(self, 0, 0, idx = self.sel)
        self.camera = Camera()
        self.level = 0

        self.black_screen = pygame.Surface(WINDOW_SIZE).convert()
        self.black_screen.fill((0, 0, 0))
        self.black_alpha = 255.0
        self.black_screen.set_alpha(self.black_alpha)
        self.black_shade = DOWN
        
        self.load_level()
        self.delay = 0
        self.command_font = pygame.font.SysFont("monospace", 12)
        self.command_rectangles = {}
        test_macro = Macro()
        test_macro.add_block(Right())
        test_macro.add_block(AttackRight())
        test_macro.add_block(Left())
        self.player.macros[0] = test_macro

        self.heart = pygame.image.load("heart.png")
        self.hheart = pygame.image.load("half_heart.png")
        self.eheart = pygame.image.load("empty_heart.png")
        self.heart_width = self.heart.get_width()

        self.mana_bar = pygame.image.load("mana_outer_bar.png")
        self.mana_fill = pygame.image.load("mana_inner_bar.png")
        self.display_mana = self.player.mana


    def update_mana_bar(self, dt):
        dm = self.player.mana - self.display_mana
        self.display_mana += dm * dt * 20.0
        
	
    def render_health(self, surf):

        mana = self.player.mana
        max_mana = self.player.mana_max
        surf.blit(self.mana_bar, (11, 30))
        new_width = int(self.display_mana*53//max_mana + 0.5)
        mana_fill = pygame.transform.scale(self.mana_fill, (new_width, self.mana_fill.get_height()))
        surf.blit(mana_fill, (14, 33))
        
        hp = self.player.hp
        xoff = 10
        yoff = 10
        xspace = 20
        for i in range(self.player.hp_max):
            if hp <= 0:
                surf.blit(self.eheart, (xoff + xspace*i, yoff))
            elif hp <= 0.5:
                surf.blit(self.hheart, (xoff + xspace*i, yoff))
            else:
                surf.blit(self.heart, (xoff + xspace*i, yoff))
            hp -= 1


    def handle_events(self, events):
        self.editor.update_mouse_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.black_shade == UP:
                    return
                if event.key == pygame.K_UP or event.key == pygame.K_w :
                    self.move_player(0, -1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.move_player(0, 1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.move_player(-1, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.move_player(1, 0)
                elif event.key == pygame.K_SPACE:
                    self.move_player(0, 0)
                    self.player.mana = self.player.mana_max
                elif event.key == pygame.K_p:
                    self.load_level()
                elif event.key == pygame.K_e:
                    self.editor.toggle()
                elif event.key == pygame.K_z:
                    if self.editor.active:
                        self.player.macros[0] = self.editor.get_macro()
                        self.player.mana = 0
                        self.editor.toggle()
                    elif self.player in self.turn_queue:
                        self.player.macro = self.player.macros[0]
                elif event.key == pygame.K_x:
                    if self.editor.active:
                        self.player.macros[1] = self.editor.get_macro()
                        self.player.mana = 0
                        self.editor.toggle()
                    elif self.player in self.turn_queue:
                        self.player.macro = self.player.macros[1]
                elif event.key == pygame.K_c:
                    if self.editor.active:
                        self.player.macros[2] = self.editor.get_macro()
                        self.player.mana = 0
                        self.editor.toggle()
                    elif self.player in self.turn_queue:
                        self.player.macro = self.player.macros[2]


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
            dt = min(dt, 1/30.0)

            events = pygame.event.get()
            self.handle_events(events)

            # Take turn
            if self.delay > 0:
                self.delay -= dt
            elif len(self.turn_queue) == 0:
                enemies = self.movers[:]
                enemies.remove(self.player)
                self.turn_queue = [self.player] + enemies
                for mover in self.turn_queue:
                    mover.turns = 1
            else:
                while len(self.turn_queue) > 0:
                    mover = self.turn_queue[0]
                    if mover is self.player:
                        if mover.turns <= 0: # end player turn
                            self.turn_queue.remove(mover)
                        elif mover.macro: # run player macro
                            if mover.macro.run(self, mover): # end macro
                                mover.macro = None
                                mover.turns = 0
                        break
                    else:
                        mover.turns -= 1
                        if mover.turns <= 0: # end enemy turn
                            self.turn_queue.remove(mover)
                        if self.map.on_screen(self.camera, mover.x, mover.y):
                            if mover in self.movers: # move enemy
                                mover.move()
                        if self.delay > 0:
                            break
            # Drawing goes here
            # TODO remove fill functions once screen is completely filled with tiles
            self.screen.fill((0, 0, 0))
            for obj in self.movers + self.effects + [self.editor]:
                obj.update(dt)
            
            self.update_camera_target()
            #self.map.update(dt, (0, 30), (0, 30))
            self.draw_map()
            #self.player.draw(self.screen)
            #self.terminal.draw(self.screen)
            self.render_health(self.screen)
            self.editor.draw(self.screen)
            self.update_black_screen(dt)
            self.update_mana_bar(dt)
            self.update_screen()
            self.draw_fps(real_dt)   #   TODO remove from final build
            pygame.display.flip()


    def update_black_screen(self, dt):
        rate = 350
        if self.black_shade == UP:
            self.black_alpha = min(self.black_alpha + rate*dt, 255)
        elif self.black_shade == DOWN:
            self.black_alpha = max(0, self.black_alpha - rate*dt)

        if self.black_alpha == 255 and self.black_shade == UP:
            if self.player.hp > 0:
                self.load_level()
            else:
                self.load_level(game_over=True)


    def draw_map(self):
        x_center, y_center = self.camera.center_tile_pos()
        xlim = (int(x_center - X_GIRTH), int(x_center + X_GIRTH))
        ylim = (int(y_center - Y_GIRTH), int(y_center + Y_GIRTH))
        self.map.draw(self.screen, ylim, xlim)


    def update_camera_target(self):
        self.camera.target_x = self.player.sprite.x_pos - (WINDOW_WIDTH)/2 + TILE_SIZE/2
        self.camera.target_y = self.player.sprite.y_pos - (WINDOW_HEIGHT)/2 + TILE_SIZE/2


    def generate_command_surface(self, text):
        font_render = self.command_font.render(text, 0, (255, 255, 255))
        back_square = pygame.Surface((font_render.get_width(), font_render.get_height()))
        back_square.fill((0, 0, 0))
        back_square.set_alpha(150)
        self.command_renders[text] = font_render
        self.command_rectangles[text] = back_square


    def update_screen(self):
        if self.black_alpha:
            self.black_screen.set_alpha(self.black_alpha)
            self.screen.blit(self.black_screen, (0, 0))
        self.screen_blit.blit(pygame.transform.scale(self.screen, BLIT_SIZE), (0, 0))


    def draw_fps(self, dt):
        self.dts.append(dt)
        if len(self.dts) > 300:
            self.dts = self.dts[-300:]
        dt_avg = sum(self.dts)*1.0/len(self.dts)
        fps = int(1/dt_avg)
        fonty_obj = self.command_font.render("FPS: " + str(fps), 0, (255, 255, 255))
        self.screen_blit.blit(fonty_obj, (WINDOW_WIDTH*SCALE - 60, 10))


    def move_player(self, dx, dy, end_turn=True):
        if self.player.macro or self.editor.active:
            return
        if len(self.turn_queue) and self.turn_queue[0] is self.player:
            self.player.translate(dx, dy)
            self.delay += 0.05
            if end_turn:
                self.player.turns -= 1
                self.player.mana = min(self.player.mana_max, self.player.mana + 1)
                if self.player.turns <= 0: # end player turn
                    self.turn_queue.remove(self.player)

    def end_level(self):
        self.black_shade = UP

    def load_level(self, game_over=False):
        if game_over:
            self.level = 0
            self.editor = Editor(self)
            self.player = Player(self, 0, 0, self.sel)
        else:
            self.level += 1
        print(self.level)
        self.movers = [self.player]
        self.effects = [self.player.slash]
        self.map = Map((30, 30))        
        spawn = self.map.populate_path(self, self.level)
        self.player.x = spawn[0]
        self.player.y = spawn[1]
        self.player.map = self.map
        self.map.add_to_cell(self.player, (self.player.x,self.player.y))
        self.camera.focus(self.player.x, self.player.y)
        self.turn_queue = []
        self.player.sprite.x_pos = self.player.x * TILE_SIZE
        self.player.sprite.y_pos = self.player.y * TILE_SIZE
        self.player.macro = False
        
        self.black_shade = DOWN
        self.black_alpha = 255.0


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

    def focus(self, x, y):
        self.x = x*TILE_SIZE-WINDOW_WIDTH/2 + TILE_SIZE/2
        self.y = y*TILE_SIZE-WINDOW_HEIGHT/2 + TILE_SIZE/2
        self.target_x = self.x
        self.target_y = self.y

    def get_x(self):
        return self.x

    def get_y(self):
        if self.shake_amp < 1:
            return self.y
        return self.y + sin(self.shake_freq * 2 * pi * self.t)*self.shake_amp


if __name__=="__main__":

    a = Game()
    a.main()
