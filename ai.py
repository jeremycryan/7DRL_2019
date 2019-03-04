import random
import math

RIGHT = (1,0)
LEFT = (-1,0)
DOWN = (0,1)
UP = (0,-1)
directions = [UP, DOWN, LEFT, RIGHT]

def move_random(enemy):
    random.shuffle(directions)
    for d in directions:
        if enemy.translate(*d):
            return

def approach_player(enemy):
    dx = enemy.game.player.x - enemy.x
    dy = enemy.game.player.y - enemy.y
    order = directions[:]
    if abs(dx) >= abs(dy):
        directions[0] = RIGHT if dx>0 else LEFT
        directions[1] = DOWN if dy>0 else UP
        directions[2] = UP if dy>0 else DOWN
        directions[3] = LEFT if dx>0 else RIGHT
    else:
        directions[0] = DOWN if dy>0 else UP
        directions[1] = RIGHT if dx>0 else LEFT
        directions[2] = LEFT if dx>0 else RIGHT
        directions[3] = UP if dy>0 else DOWN
    for d in order:
        if enemy.translate(*d):
            return
