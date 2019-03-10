import pygame

WINDOW_WIDTH = 240
WINDOW_HEIGHT = 180
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
SCALE = 3
BLIT_SIZE = (WINDOW_WIDTH*SCALE, WINDOW_HEIGHT*SCALE)
X_GIRTH, Y_GIRTH = 10, 8

FLOOR_LAYER = 0
FLOOR_DETAIL_LAYER = 1
WALL_LAYER = 2
ITEM_LAYER = 3
PLAYER_LAYER = 4
ENEMY_LAYER = 5
FACE_MONKEY_LAYER = 6

PLAYER_DELAY = 1

TILE_SIZE = 20
REBOUND = 12
HOP = 12
REBOUND_DURATION = 0.18
HOP_DURATION = 0.1

RIGHT = (1,0)
LEFT = (-1,0)
DOWN = (0,1)
UP = (0,-1)
directions = [UP, DOWN, LEFT, RIGHT]

KEYDICT = {pygame.K_a: "a",
           pygame.K_b: "b",
           pygame.K_c: "c",
           pygame.K_d: "d",
           pygame.K_e: "e",
           pygame.K_f: "f",
           pygame.K_g: "g",
           pygame.K_h: "h",
           pygame.K_i: "i",
           pygame.K_j: "j",
           pygame.K_k: "k",
           pygame.K_l: "l",
           pygame.K_m: "m",
           pygame.K_n: "n",
           pygame.K_o: "o",
           pygame.K_p: "p",
           pygame.K_q: "q",
           pygame.K_r: "r",
           pygame.K_s: "s",
           pygame.K_t: "t",
           pygame.K_u: "u",
           pygame.K_v: "v",
           pygame.K_w: "w",
           pygame.K_x: "x",
           pygame.K_y: "y",
           pygame.K_z: "z",
           pygame.K_SPACE: " "}
