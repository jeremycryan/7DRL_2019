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
            return True
    return False

def approach_player(enemy):
    dx = enemy.game.player.x - enemy.x
    dy = enemy.game.player.y - enemy.y
    order = go_to(dx, dy)
    for d in order:
        if enemy.translate(*d):
            return True
    return False

def approach_player_smart(enemy):
    dx = enemy.game.player.x - enemy.x + enemy.vx
    dy = enemy.game.player.y - enemy.y + enemy.vy
    if abs(dx - enemy.vx) + abs(dy - enemy.vy) == 1:
        enemy.translate(dx - enemy.vx, dy - enemy.vy)
        return True
    order = go_to(dx, dy)
    for d in order:
        if enemy.translate(*d):
            return True
    return False

def charge_player(enemy):
    if not hasattr(enemy, "charging"):
        enemy.charging = False
    player = enemy.game.player
    if enemy.charging:
        if player.x == enemy.x + enemy.vx:
            if player.y == enemy.y + enemy.vy: # Hit player
                enemy.charging = False
        if enemy.translate(enemy.vx, enemy.vy): # Continue charge
            return True
        enemy.charging = False # Hit wall
        return False
    if enemy.map.is_straight_path((enemy.x, enemy.y), (player.x, player.y)):
        order = go_to(player.x - enemy.x, player.y - enemy.y)
        if player.x == enemy.x + order[0][0]:
            if player.y == enemy.y + order[0][1]:
                enemy.translate(*order[0]) # Hit player
                return True
        if enemy.translate(*order[0]): # Start charge
            enemy.charging = True
            return True
    dx = player.x - enemy.x + enemy.vx
    dy = player.y - enemy.y + enemy.vy
    order = go_to(dx, dy)
    for d in order:
        if enemy.translate(*d): # Seek player
            return True
    return False

def go_to(dx, dy):
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
    return order
