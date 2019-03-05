from game_object import GameObject
from sprite_tools import *
import random

class Map(object):

    def __init__(self, size = (60, 60)):

        self.cells = []

        for i in range(size[0]):
            self.cells.append([])
            for j in range(size[1]):
                self.cells[i].append([])


    def populate_random(self, game):

        for x in range(len(self.cells)):
            for y in range(len(self.cells[0])):
                if random.random() < 0.2:
                    self.add_to_cell(Wall(game, x, y), (x, y))
                else:
                    self.add_to_cell(Tile(game, x, y), (x, y))


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
        for x in [i + xlim[0] for i in range(xlim[1] - xlim[0])]:
            for y in [j + ylim[0] for j in range(ylim[1] - ylim[0])]:
                for item in self.get((y, x)):
                    item.draw(surf)


class Tile(GameObject):

    def __init__(self, game, x, y, fps=4):
        GameObject.__init__(self, game, x, y, layer=0, fps=fps)
        static = SpriteSheet("default_tile.png", (1, 1), 1)
        self.sprite.add_animation({"Static": static})
        self.sprite.start_animation("Static")
        self.static = True

    def draw(self, surf):
        self.sprite.x_pos -= int(self.game.camera.x)
        self.sprite.y_pos -= int(self.game.camera.y)
        GameObject.draw(self, surf)
        self.sprite.x_pos += int(self.game.camera.x)
        self.sprite.y_pos += int(self.game.camera.y)

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

