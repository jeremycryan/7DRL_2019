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


def move_random_or_screech(enemy):
    if enemy.moved_last_turn:
        enemy.moved_last_turn = False
        enemy.game.terminal.append_to_text("e")
    else:
        enemy.moved_last_turn = True
        random.shuffle(directions)
        for d in directions:
            if enemy.translate(*d):
                return


def approach_player(enemy):
    dx = enemy.game.player.x - enemy.x
    dy = enemy.game.player.y - enemy.y
    order = directions[:]
    if abs(dx) >= abs(dy):
        order[0] = RIGHT if dx>0 else LEFT
        order[1] = DOWN if dy>0 else UP
        order[2] = UP if dy>0 else DOWN
        order[3] = LEFT if dx>0 else RIGHT
    else:
        order[0] = DOWN if dy>0 else UP
        order[1] = RIGHT if dx>0 else LEFT
        order[2] = LEFT if dx>0 else RIGHT
        order[3] = UP if dy>0 else DOWN
    for d in order:
        if enemy.translate(*d):
            return

def approach_player_smart(enemy):
    dx = enemy.game.player.x - enemy.x + enemy.vx
    dy = enemy.game.player.y - enemy.y + enemy.vy
    if abs(dx - enemy.vx) + abs(dy - enemy.vy) == 1:
        enemy.translate(dx - enemy.vx, dy - enemy.vy)
        return
    order = directions[:]
    if abs(dx) >= abs(dy):
        order[0] = RIGHT if dx>0 else LEFT
        order[1] = DOWN if dy>0 else UP
        order[2] = UP if dy>0 else DOWN
        order[3] = LEFT if dx>0 else RIGHT
    else:
        order[0] = DOWN if dy>0 else UP
        order[1] = RIGHT if dx>0 else LEFT
        order[2] = LEFT if dx>0 else RIGHT
        order[3] = UP if dy>0 else DOWN
    for d in order:
        if enemy.translate(*d):
            return

