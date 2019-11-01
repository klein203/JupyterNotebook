import random
import modal

class Creature(GameObject):
    def __init__(self, config):
        super().__init__(config)
        
        self.type = 0
        
        self.level = 1
        self.experience = 0
        
#         self.str = 10
#         self.dex = 10
#         self.agi = 10
#         self.int = 10
#         self.con = 10
#         self.luk = 10
        
        self.hp = 0
#         self.sp = 0
        self.attack = 0
        self.defense = 0
#         self.hit = 0
#         self.avoid = 0
        
        # position
        self.rowIdx = 0
        self.colIdx = 0
        
        # dice
        self.maxDice = 20
    
    def dice(self):
        return random.randint(1, self.maxDice)
    
    def move(self, drow, dcol):
        self.rowIdx += drow
        self.colIdx += dcol
    
#     def moveToPos(self, rowIdx, colIdx):
#         self.rowIdx = rowIdx
#         self.colIdx = colIdx
    
    def getPos(self):
        return self.rowIdx, self.colIdx


class Player(Creature):
    def __init__(self, config):
        super().__init__(config)


class Monster(Creature):
    def __init__(self, config):
        super().__init__(config)




