from constants import *
from sprite_tools import *
from game_object import GameObject

class Item(GameObject):
    def __init__(self, game, x, y, path="", fps=4):
        GameObject.__init__(self, game, x, y, layer=ITEM_LAYER, fps=fps)
        static = SpriteSheet(path+"_small.png", (1, 1), 1)
        self.layer = ITEM_LAYER
        self.sprite.add_animation({"Static": static})
        self.sprite.start_animation("Static")
        self.static = True
        self.map = game.map
        game.map.add_to_cell(self, (x,y))

    
class BlockItem(Item):
    def __init__(self, game, x, y, block):
        Item.__init__(self, game, x, y, path=block.path, fps=4)
        self.block = block
        

