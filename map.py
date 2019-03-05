from game_object import GameObject
from sprite_tools import *
from enemy import Enemy
import random
from constants import *

class Map(object):

    def __init__(self, size = (60, 60)):

        self.cells = []

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
        for x in range(1, 4):
            for y in range(1, 4):
                Tile(game, x, y)


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

        
    def populate_enemies(self, game, difficulty=1):
        for x in range(1, len(self.cells)-1):
            for y in range(1, len(self.cells[0])-1):
                if not self.get((x,y), "blocking"):
                    if random.random() < .05:
                        Enemy(game, x, y)
    

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


class Tile(GameObject):

    def __init__(self, game, x, y, fps=4):
        GameObject.__init__(self, game, x, y, layer=0, fps=fps)
        static = SpriteSheet("default_tile.png", (1, 1), 1)
        self.sprite.add_animation({"Static": static})
        self.sprite.start_animation("Static")
        self.static = True

    def draw(self, surf):
        GameObject.draw(self, surf)

class Wall(Tile):

    def __init__(self, game, x, y, fps=4):
        Tile.__init__(self, game, x, y, fps=fps)
        self.layer = 2
        self.blocking = True
        static = SpriteSheet("wall_tile.png", (1, 1), 1)
        self.sprite.add_animation({"Static": static})
        self.sprite.start_animation("Static")
        self.static = True
    


if __name__=="__main__":

    m = Map()
    a = Map()
    a.hidden = True

    m.add_to_cell(a, (3, 3))

