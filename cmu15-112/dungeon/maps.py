import random
import modal
from modal import *

class DefaultMap(Map):
    def __init__(self, config):
        super().__init__(config)
        self.row = config.row
        self.col = config.col
        self.board = [([0] * self.col) for i in range(self.row)]

        self.randomMap(config.p)
        
    def getBorder(self):
        return self.row, self.col
    
    def hasBlock(self, rowIdx, colIdx):
        if self.board[rowIdx][colIdx] == 0:
            return False
        else:
            return True
    
    def randomMap(self, p=0.999):
        for i in range(self.row):
            for j in range(self.col):
                if random.random() > p:
                    self.board[i][j] = 1