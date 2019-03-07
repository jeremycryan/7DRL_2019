#!/usr/bin/env python
import pygame
from constants import *
from sprite_tools import *
import time

class Editor(object):

    def __init__(self):

        self.font = pygame.font.SysFont("monospace", 12)

        self.cur_macro = None

        self.line_spacing = 14

        self.chars = "abcdefghijklmnopqrstuvwxyz "
        self.char_surfs = {}
        for char in self.chars:
            self.char_surfs[char] = self.font.render(char, 0, (255, 255, 255))
        self.char_width = self.char_surfs["a"].get_width()
        self.char_height = self.char_surfs["a"].get_height()

        self.cursor_pos = [0, 0]        
        self.cursor_surf = pygame.image.load("cursor.png")
        self.cursor_surf = pygame.transform.scale(self.cursor_surf,
                                                    (self.char_width, self.char_height))
        self.time = 0
        self.blink_rate = 1

        self.back_pressed = False
        self.back_time = 0


    def draw(self, surf):

        surf.fill((0, 0, 0))

        yoff = 20
        xoff = 20
        letter_spacing = 0
        for (y, line) in enumerate(self.cur_macro.lines):

            for (x, letter) in enumerate(line + " "):
                surf.blit(self.char_surfs[letter], (xoff + letter_spacing, yoff))
                if [x, y] == self.cursor_pos and (self.time*self.blink_rate)%1 < 0.5:
                    surf.blit(self.cursor_surf, (xoff + letter_spacing, yoff))
                letter_spacing += self.char_width

            letter_spacing = 0
            yoff += self.line_spacing


    def update(self, dt):
        self.time += dt
        if self.back_pressed:
            self.back_time += dt
        else:
            self.back_time = 0

    def move_cursor(self, dx, dy):
        self.cursor_pos[0] += dx
        self.cursor_pos[1] += dy

        if self.cursor_pos[1] >= len(self.cur_macro.lines):
            self.cursor_pos[1] = len(self.cur_macro.lines) - 1
        if self.cursor_pos[1] <= 0:
            self.cursor_pos[1] = 0

        if self.cursor_pos[0] <= 0:
            self.cursor_pos[0] = 0
        elif self.cursor_pos[0] > len(self.cur_macro.lines[self.cursor_pos[1]]):
            self.cursor_pos[0] = len(self.cur_macro.lines[self.cursor_pos[1]])
        


    def check_events(self, events):

        col = self.cursor_pos[0]
        line = self.cursor_pos[1]

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.time = 0
                if event.key == pygame.K_UP:
                    self.move_cursor(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.move_cursor(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.move_cursor(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.move_cursor(1, 0)
                elif event.key == pygame.K_BACKSPACE:
                    if self.cur_macro.delete_char(line, col - 1):
                        self.move_cursor(-1, 0)
                    self.back_pressed = True
                elif event.key in KEYDICT:
                    new_char = KEYDICT[event.key]
                    self.cur_macro.insert_char(line, col, new_char)
                    self.move_cursor(1, 0)

            elif event.type = pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.back_pressed = False
    


class Macro(object):

    def __init__(self, line_num = 3):

        self.line_num = line_num
        self.lines = [""] * line_num


    def insert_char(self, line, col, char):

        if col >= len(self.lines[line]):
            self.lines[line] = self.lines[line] + char
            return True                        
        
        self.lines[line] = self.lines[line][:col] + char + self.lines[line][col:]
        return True
        
    def delete_char(self, line, col):
        if col < 0:
            return False
        self.lines[line] = self.lines[line][:col] + self.lines[line][col+1:]
        return True
                    

    def write_line(self, line, text):

        self.lines[line] = text



if __name__=="__main__":

    pygame.init()

    a = Macro(3)
    a.write_line(0, "marsupial")
    a.write_line(1, "quagmire")
    a.write_line(2, "matt damon")
    b = Editor()
    b.cur_macro = a

    c = pygame.Surface((WINDOW_SIZE))
    d = pygame.display.set_mode((BLIT_SIZE))

    then = time.time()
    time.sleep(0.001)
    while True:

        events = pygame.event.get()

        now = time.time()
        dt = now - then
        then = now

        b.update(dt)
        b.draw(c)
        b.check_events(events)
        d.blit(pygame.transform.scale(c, BLIT_SIZE), (0, 0))
        pygame.display.flip()
    
