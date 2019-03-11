from game_object import GameObject
from sprite_tools import *
import random
from enemy import *
from item import *
from block import *
from constants import *

class Map(object):

    def __init__(self, size = (60, 60)):

        self.cells = []

        self.size = size

        for i in range(size[0]):
            self.cells.append([])
            for j in range(size[1]):
                self.cells[i].append([])


    def populate_random(self, game, wall_ratio=0.2):
        self.populate_wall(game)
        for x in range(1, len(self.cells)-1):
            for y in range(1, len(self.cells[0])-1):
                if self.get((x,y)):
                    continue
                if random.random() < wall_ratio:
                    Wall(game, x, y)
                else:
                    Tile(game, x, y)
        self.populate_enemies(game)


    def populate_wall(self, game):
        xmax = len(self.cells)
        ymax = len(self.cells[0])
        for x in range(xmax):
            Wall(game, x, 0)
            Wall(game, x, ymax-1)
        for y in range(ymax):
            Wall(game, 0, y)
            Wall(game, xmax-1, y)
        for x in range(1, 6):
            for y in range(1, 6):
                pass#Tile(game, x, y)


    def populate_rooms(self, game):
        self.populate_wall(game)
        xmax = len(self.cells)-1
        ymax = len(self.cells[0])-1
        SEED_DENSITY = 0.1
        ROOM_MIN_SIZE = 3
        ROOM_MAX_SIZE = 4
        for i in range(int(SEED_DENSITY*xmax*ymax)):
            x = random.randint(-int(ROOM_MIN_SIZE/2), xmax-1)
            y = random.randint(-int(ROOM_MIN_SIZE/2), ymax-1)
            w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            if random.randint(0,1):
                w += 1
                h -= 1
            else:
                h += 1
                w -= 1
            for x1 in range(x, x+w):
                if x1 >= 1 and x1 < xmax:
                    for y1 in range(y, y+h):
                        if y1 >= 1 and y1 < ymax:
                            if not self.get((x1, y1)):
                                Tile(game, x1, y1)
        self.populate_random(game, 0.9)

    def populate_path(self, game, difficulty=1):
        self.populate_wall(game)
        xmax = len(self.cells)-1
        ymax = len(self.cells[0])-1
        SEED_DENSITY = 0.07
        ROOM_MIN_SIZE = 3
        ROOM_MAX_SIZE = 5
        N = int(SEED_DENSITY*xmax*ymax)
        seeds = [(random.randint(1, xmax-1), random.randint(1,ymax-1)) for i in range(N)]
        seeds.sort(key=lambda x: x[0])
        # Create path
        for i, s1 in enumerate(seeds[:-1]):
            s_min = None
            d_min = None
            for s2 in seeds[i+1:]:
                d = abs(s2[0]-s1[0]) + abs(s2[1]-s1[1])
                if not s_min or d < d_min:
                    s_min = s2
                    d_min = d
            self.clear_path(game, s1, s_min)
        # Create rooms
        for s in seeds:
            w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            for x1 in range(s[0], s[0]+w):
                if x1 >= 1 and x1 < xmax:
                    for y1 in range(s[1], s[1]+h):
                        if y1 >= 1 and y1 < ymax:
                            if not self.get((x1, y1)):
                                Tile(game, x1, y1)
        # Fill walls
        for x in range(1, xmax):
            for y in range(1, ymax):
                if not self.get((x,y)):
                    Wall(game, x, y)
        # Spawn enemies
        if random.random() < 0.5:
            seeds.sort(key=lambda x: x[1])
        if random.random() < 0.5:
            seeds = seeds[::-1]
        Stairs(game, seeds[-1][0], seeds[-1][1])
        self.populate_enemies(game, seeds[0], difficulty)
        return seeds[0]

    def clear_path(self, game, s1, s2):
        x, y = s1[0], s1[1]
        while True:
            Tile(game, x, y)
            dx = s2[0]-x
            dy = s2[1]-y
            if dx == 0 and dy == 0:
                return
            if abs(dx) >= abs(dy):
                x += 1 if dx>0 else -1
            else:
                y += 1 if dy>0 else -1
        

    def populate_enemies(self, game, spawn, difficulty=1):
        for x in range(1, len(self.cells)-1):
            for y in range(1, len(self.cells[0])-1):
                if abs(spawn[0] - x) < 3 and abs(spawn[1] - y) < 3:
                    continue
                if not self.get((x,y), "blocking"):

                    r = random.random()
                    if r < 0.015:
                        Bug(game, x, y)
                    elif r < 0.03:
                        Ebat(game, x, y)
                    elif r < 0.04:
                        Bit(game, x, y)
                    elif r < 0.045:
                        FlameSpawner(game, x, y)
                    elif r < 0.05:
                        GroundHazard_Fixed(game, x, y)
                    elif r < 0.06:
                        Hedgehog(game, x, y)



    def add_to_cell(self, new_item, pos):
        self.cells[pos[0]][pos[1]].append(new_item)
        self.sort_cell(pos)


    def sort_cell(self, pos):
        self.cells[pos[0]][pos[1]].sort(key=lambda a: a.layer)


    def remove_from_cell(self, remove_item, pos):
        if remove_item in self.cells[pos[0]][pos[1]]:
            self.cells[pos[0]][pos[1]].remove(remove_item)
            return remove_item


    def get(self, pos, *args):
        """ Example usage:

        map.get((0, 1), ("layer", 3), ("hidden", 0), "blocking")
        """

        things_at_pos = self.cells[pos[0]][pos[1]]
        return_list = []
        for thing in things_at_pos:
            add_to_list = True
            for arg in args:
                if type(arg) == str:
                    if not hasattr(thing, arg) or not getattr(thing, arg):
                        add_to_list = False
                else:
                    if not hasattr(thing, arg[0]) or getattr(thing, arg[0]) != arg[1]:
                        add_to_list = arg[1]==False
            if add_to_list:
                return_list.append(thing)
        return return_list

    def draw(self, surf, xlim, ylim):

        ## Limit bounds if off map
        if xlim[0] < 0: xlim = (0, xlim[1])
        if ylim[0] < 0: ylim = (0, ylim[1])
        if xlim[1] > self.size[1]: xlim = (xlim[0], self.size[1])
        if ylim[1] > self.size[0]: ylim = (ylim[0], self.size[0])

        # Draw all tile and detail tiles first
        for x in [i + xlim[0] for i in range(xlim[1] - xlim[0])]:
            for y in [j + ylim[0] for j in range(ylim[1] - ylim[0])]:
                for item in self.get((y, x)):
                    if item.layer in [FLOOR_LAYER, FLOOR_DETAIL_LAYER]:
                        item.draw(surf)

        # Then draw enemies, players, items, etc
        for x in [i + xlim[0] for i in range(xlim[1] - xlim[0])]:
            for y in [j + ylim[0] for j in range(ylim[1] - ylim[0])]:
                for item in self.get((y, x)):
                    if not item.layer in [FLOOR_LAYER, FLOOR_DETAIL_LAYER]:
                        item.draw(surf)


    def on_screen(self, camera, x, y):
        x_center, y_center = camera.center_tile_pos()
        xlim = (int(x_center - X_GIRTH), int(x_center + X_GIRTH))
        ylim = (int(y_center - Y_GIRTH), int(y_center + Y_GIRTH))
        if xlim[0] < 0: xlim = (0, xlim[1])
        if ylim[0] < 0: ylim = (0, ylim[1])
        if xlim[1] > self.size[1]: xlim = (xlim[0], self.size[1])
        if ylim[1] > self.size[0]: ylim = (ylim[0], self.size[0])
        return x >= xlim[0] and x < xlim[1] and y >= ylim[0] and y < ylim[1]
    

    def is_straight_path(self, pos1, pos2):
        if pos1[0] == pos2[0]:
            for y in range(min(pos1[1], pos2[1])+1, max(pos1[1], pos2[1])):
                if self.get((pos1[0], y), "blocking"):
                    return False
        elif pos1[1] == pos2[1]:
            for x in range(min(pos1[0], pos2[0])+1, max(pos1[0], pos2[0])):
                if self.get((x, pos1[1]), "blocking"):
                    return False
        else:
            return False
        return True


class Tile(GameObject):

    def __init__(self, game, x, y, fps=4):
        GameObject.__init__(self, game, x, y, layer=0, fps=fps)
        self.layer = FLOOR_LAYER
        sprite_paths = [("default_tile" + str(a) + ".png") for a in ["", 0, 1, 2, 3, 4]]
        static = SpriteSheet(random.choice(sprite_paths), (1, 1), 1)
        self.sprite.add_animation({"Static": static})
        self.sprite.start_animation("Static")
        self.static = True
        self.map = game.map
        game.map.add_to_cell(self, (x,y))

    def draw(self, surf):
        GameObject.draw(self, surf)

class Wall(Tile):

    def __init__(self, game, x, y, fps=4):
        Tile.__init__(self, game, x, y, fps=fps)
        self.layer = WALL_LAYER
        self.blocking = True
        sprite_paths = [("wall_tile" + str(a) + ".png") for a in ["", 0, 1, 2]]
        static = SpriteSheet(random.choice(sprite_paths), (1, 1), 1)
        self.sprite.add_animation({"Static": static})
        self.sprite.start_animation("Static")
        self.static = True

class Stairs(Tile):

    def __init__(self, game, x, y, fps=4):
        Tile.__init__(self, game, x, y, fps=fps)
        self.layer = FLOOR_LAYER
        sprite_paths = "stair.png"
        static = SpriteSheet(sprite_paths, (1, 1), 1)
        self.sprite.add_animation({"Static": static})
        self.sprite.start_animation("Static")
        self.static = True
        self.stairs = True
        self.avoid = True


if __name__=="__main__":

    m = Map()
    a = Map()
    a.hidden = True

    m.add_to_cell(a, (3, 3))
