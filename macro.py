from block import *

class Macro:
    def __init__(self, length = 3):
        self.length = length
        self.clear()
        self.index = 0

    def add_block(self, block, index=-1):
        if index == -1:
            for i, b in enumerate(self.blocks):
                if not b:
                    self.blocks[i] = block
                    break
        else:
            self.blocks[index] = block

    def remove_block(self, index):
        self.blocks[index] = False

    def clear(self):
        self.blocks = [False for i in range(self.length)]
        
    def reset(self):
        self.index = 0

    def run(self, game, player):
        if self.blocks[self.index] and not self.blocks[self.index].run(game, player):
            self.index = 0
            return True
        self.index += 1
        if self.index >= self.length:
            self.index = 0
            return True
        return False
