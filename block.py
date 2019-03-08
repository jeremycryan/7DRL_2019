from ai import *

class Block:
    def __init__(self, cost=1, duration=0, delay=0.05):
        self.cost = cost
        self.duration = duration
        self.delay = delay
    
    def run(self, game, player):
        player.mana -= self.cost
        if player.mana < 0:
            player.mana = 0
            return False
        self.action(player)
        game.delay += self.delay
        player.turns -= self.duration
        return True

    def action(self):
        pass

class Up(Block):
    def action(self, player):
        player.translate(*UP, False)

class Down(Block):
    def action(self, player):
        player.translate(*DOWN, False)

class Left(Block):
    def action(self, player):
        player.translate(*LEFT, False)

class Right(Block):
    def action(self, player):
        player.translate(*RIGHT, False)

class AttackUp(Block):
    def action(self, player):
        player.attack(*UP, True)
        
class AttackDown(Block):
    def action(self, player):
        player.attack(*DOWN, True)
        
class AttackLeft(Block):
    def action(self, player):
        player.attack(*LEFT, True)
        
class AttackRight(Block):
    def action(self, player):
        player.attack(*RIGHT, True)
