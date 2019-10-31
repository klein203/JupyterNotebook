import math, copy, random, uuid

from cmu_112_graphics import *
from tkinter import *


class GameObject(object):
    def __init__(self, name, **kwargs):
        self.uuid = uuid.uuid4()
        self.name = name
        print('[init][%s][%s] %s' % (self.__class__.__name__, self.uuid, self))
    
    def __repr__(self):
        return self.name


class Scenario(GameObject):
    def __init__(self, name, row, col, **kwargs):
        super().__init__(name, **kwargs)
        self.row = row
        self.col = col
        self.board = [([0] * col) for i in range(row)]
#         self.activated = False
        
    def getBorder(self):
        return self.row, self.col
    
    def hasBlock(self, rowIdx, colIdx):
        if self.board[rowIdx][colIdx] == 0:
            return False
        else:
            return True
    
#     def activate(self):
#         self.activated = True
        
#     def deactivate(self):
#         self.activated = False
        
#     def isActivated(self):
#         return self.activated
        

class Map(Scenario):
    def __init__(self, name, row, col, **kwargs):
        super().__init__(name, row, col, **kwargs)
        self.randomMap()
    
    def randomMap(self, p=0.999):
        for i in range(self.row):
            for j in range(self.col):
                if random.random() > p:
                    self.board[i][j] = 1
    

class Item(GameObject):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.category = 0


class Creature(GameObject):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        
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
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class Monster(Creature):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


# class BattleMode(Mode):
#     def __init__(self, name, player, monster, **kwargs):
#         super().__init__(name, **kwargs)
#         self.player = player
#         self.monster = monster
    
#     def battle(self, attacker, defencer):
#         pass
        

class MainMode(Mode):
    def __init__(self, name, width=420, height=420, x=0, y=0, **kwargs):
        super().__init__(width=width, height=height, x=x, y=y, **kwargs)
        # constant
        self.CELL_PIXEL = 10
        self.MAP_PADDING_BLOCK = 2
        self.PADDING_PIXEL = 15
        
        # game
        self.name = name

        # maps
        self.maps = dict()
        self.initMaps()
        self.map = self.maps['map_default']
        
        # slide window frame setting
        # should be odd
        self.slideWindowRow = 7
        self.slideWindowCol = 11
        
        self.offsetRow = self.slideWindowRow // 2
        self.offsetCol = self.slideWindowCol // 2
        
        self.scrollRowIdx = 0
        self.scrollColIdx = 0
        
        # player
        self.player = None
        self.initPlayer()

    def appendMap(self, m):
        self.maps[m.name] = m
    
    def setActiveMap(self, name):
        if name in self.maps:
            self.map = self.maps[name]
    
    def getActiveMap(self):
        return self.map
    
    def initMaps(self):
        self.appendMap(Map('map_default', 12, 16))
#         self.appendMap(Map('map_test_11_15', 11, 15))
    
    def initPlayer(self):
        self.player = Player('Hero')

#     def initMonsters(self, number):
#         self.monsters = []
#         for i in range(1, 6):
#             m = Monster('slime_%d' % i)
#             self.monsters.append(m)
    
    def getMapBorder(self):
        return self.map.getBorder()
    
    def getScrollIndex(self):
        return (self.scrollRowIdx, self.scrollColIdx)
    
    def setSlideWindowBorder(self, row, col):
        self.slideWindowRow = row
        self.slideWindowCol = col
        self.offsetRow = self.slideWindowRow // 2
        self.offsetCol = self.slideWindowCol // 2

    def getSlideWindowBorder(self):
        return (self.slideWindowRow, self.slideWindowCol)
    
    def getPlayerPos(self):
        return self.player.getPos()
    
#     def movePlayerToPos(self, row, col):
#         self.player.moveToPos(row, col)
#         self.scrollMap()
    
    def movePlayer(self, drow, dcol):
        curRowIdx, curColIdx = self.getPlayerPos()
        
        tryRowIdx = curRowIdx + drow
        tryColIdx = curColIdx + dcol
        
        mapBorderRow, mapBorderCol = self.getMapBorder()
        
        if tryRowIdx >= 0 and tryRowIdx < mapBorderRow and tryColIdx >= 0 and tryColIdx < mapBorderCol:
            if self.hasBlock(tryRowIdx, tryColIdx) == False:
                self.player.move(drow, dcol)
                self.scrollMap()
    
    def hasBlock(self, rowIdx, colIdx):
        return self.getActiveMap().hasBlock(rowIdx, colIdx)
    
    def scrollMap(self):
        curRowIdx, curColIdx = self.getPlayerPos()
        mapBorderRow, mapBorderCol = self.getMapBorder()
        
        if curRowIdx < self.offsetRow:
            self.scrollRowIdx = 0
        elif curRowIdx < mapBorderRow - self.slideWindowRow + self.offsetRow:
            self.scrollRowIdx = curRowIdx - self.offsetRow + 1
        else:
            self.scrollRowIdx = mapBorderRow - self.slideWindowRow
        
#         print('offsetCol', offsetCol, 'mapbordercol', mapBorderCol, ' - wincol', self.slideWindowCol)
#         print('scroll', self.scrollColIdx, 'col', curCol, offsetCol, mapBorderCol - self.slideWindowCol)

        if curColIdx < self.offsetCol:
            self.scrollColIdx = 0
        elif curColIdx < mapBorderCol - self.slideWindowCol + self.offsetCol:
            self.scrollColIdx = curColIdx - self.offsetCol + 1
        else:
            self.scrollColIdx = mapBorderCol - self.slideWindowCol
        
    def keyPressed(self, event):
        if event.key == 'Down':
            self.movePlayer(+1, 0)
            self.scrollMap()
        elif event.key == 'Left':
            self.movePlayer(0, -1)
            self.scrollMap()
        elif event.key == 'Right':
            self.movePlayer(0, +1)
            self.scrollMap()
        elif event.key == 'Up':
            self.movePlayer(-1, 0)
            self.scrollMap()

    def redrawAll(self, canvas):
        dx = self.MAP_PADDING_BLOCK * self.PADDING_PIXEL
        dy = self.MAP_PADDING_BLOCK * self.PADDING_PIXEL
        self.drawSlideWindow(canvas, dx, dy)
        self.drawText(canvas, dx, dy)
        
    def drawSlideWindow(self, canvas, dx, dy):
        self.drawMap(canvas, dx, dy)
        self.drawPlayer(canvas, dx, dy)

    def drawMap(self, canvas, dx, dy):
        # slide window border
        x0 = dx
        y0 = dy
        x1 = x0 + self.slideWindowCol * self.CELL_PIXEL
        y1 = y0 + self.slideWindowRow * self.CELL_PIXEL
        fill = 'white'
        canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
        
        # grid
        for i in range(1, self.slideWindowRow):
            x0 = dx
            y0 = dy + i * self.CELL_PIXEL
            x1 = x0 + self.slideWindowCol * self.CELL_PIXEL
            y1 = y0
            fill = 'grey'
            canvas.create_line(x0, y0, x1, y1, fill=fill)
            
        for j in range(1, self.slideWindowCol):
            x0 = dx + j * self.CELL_PIXEL
            y0 = dy
            x1 = x0
            y1 = y0 + self.slideWindowRow * self.CELL_PIXEL
            fill = 'grey'
            canvas.create_line(x0, y0, x1, y1, fill=fill)
        
        # block cells
        for i in range(self.slideWindowRow):
            for j in range(self.slideWindowCol):
                sRowIdx = i + self.scrollRowIdx
                sColIdx = j + self.scrollColIdx
                if self.hasBlock(sRowIdx, sColIdx):
                    x0 = dx + j * self.CELL_PIXEL
                    y0 = dy + i * self.CELL_PIXEL
                    x1 = x0 + self.CELL_PIXEL
                    y1 = y0 + self.CELL_PIXEL
                    canvas.create_oval(x0, y0, x1, y1, fill='black')
                    canvas.create_text(x1 + 20, 
                                       (y0 + y1) / 2, 
                                       text='(%d, %d)' % (sRowIdx, sColIdx), 
                                       fill='black', 
                                       font='Arial 8')

    def convertToSlideWindowPos(self, rowIdx, colIdx): # 51
        sRowIdx = self.offsetRow - 1
        sColIdx = self.offsetCol - 1 # 7

        mapBorderRow, mapBorderCol = self.getMapBorder() # 60
                
        if rowIdx < self.offsetRow:
            sRowIdx = rowIdx
        elif rowIdx > mapBorderRow - (self.slideWindowRow - self.offsetRow) - 1:
            sRowIdx = rowIdx - (mapBorderRow - self.slideWindowRow)
        
        if colIdx < self.offsetCol: # < 8
            sColIdx = colIdx
        elif colIdx > mapBorderCol - (self.slideWindowCol - self.offsetCol) - 1:
            sColIdx = colIdx - (mapBorderCol - self.slideWindowCol)

        return (sRowIdx, sColIdx)
        
    def drawPlayer(self, canvas, dx, dy):
        (curRowIdx, curColIdx) = self.getPlayerPos()
        (slideRowIdx, slideColIdx) = self.convertToSlideWindowPos(curRowIdx, curColIdx)
        
        x0 = dx + slideColIdx * self.CELL_PIXEL
        y0 = dy + slideRowIdx * self.CELL_PIXEL
        x1 = x0 + self.CELL_PIXEL
        y1 = y0 + self.CELL_PIXEL
        canvas.create_oval(x0 + 1, 
                           y0 + 1, 
                           x1 - 1, 
                           y1 - 1, 
                           fill='grey')
        # debug
        canvas.create_text(x1 + 20, 
                           (y0 + y1) / 2, 
                           text='(%d, %d)' % (slideRowIdx, slideColIdx), 
                           fill='black', 
                           font='Arial 8')
    
    def drawText(self, canvas, dx, dy):
        # map border
        canvas.create_text(dx + self.slideWindowCol * self.CELL_PIXEL // 2,
                           dy + self.slideWindowRow * self.CELL_PIXEL + self.PADDING_PIXEL // 2, 
                           text='slide (r%d x c%d)' % self.getSlideWindowBorder(), 
                           fill='black', 
                           font='Arial 8')
        canvas.create_text(dx + self.slideWindowCol * self.CELL_PIXEL // 2, 
                           dy + self.slideWindowRow * self.CELL_PIXEL + self.PADDING_PIXEL + self.PADDING_PIXEL // 2, 
                           text='map (r%d x c%d)' % self.getMapBorder(), 
                           fill='black', 
                           font='Arial 8')
        
        # debug
        self.drawDebugText(canvas, dx, dy)
    
    def drawDebugText(self, canvas, dx, dy):
        # scroll window index
        canvas.create_text(dx + self.CELL_PIXEL // 2, 
                           self.PADDING_PIXEL // 2, 
                           text='%d' % self.scrollColIdx, 
                           fill='black', 
                           font='Arial 8')
        canvas.create_text(self.PADDING_PIXEL // 2, 
                           dy + self.CELL_PIXEL // 2, 
                           text='%d' % self.scrollRowIdx, 
                           fill='black', 
                           font='Arial 8')
        
        # offset index
        canvas.create_text(dx + (self.offsetCol - 1) * self.CELL_PIXEL + self.CELL_PIXEL // 2, 
                           self.PADDING_PIXEL // 2, 
                           text='%d' % (self.offsetCol - 1), 
                           fill='grey', 
                           font='Arial 8')
        canvas.create_text(self.PADDING_PIXEL // 2, 
                           dy + (self.offsetRow - 1) * self.CELL_PIXEL + self.CELL_PIXEL // 2, 
                           text='%d' % (self.offsetRow - 1), 
                           fill='grey', 
                           font='Arial 8')
        
        # player position index
        canvas.create_text(dx + self.CELL_PIXEL // 2, 
                           self.PADDING_PIXEL + self.PADDING_PIXEL // 2, 
                           text='%d' % self.getPlayerPos()[1], 
                           fill='black', 
                           font='Arial 8')
        canvas.create_text(self.PADDING_PIXEL + self.PADDING_PIXEL // 2, 
                           dy + self.CELL_PIXEL // 2, 
                           text='%d' % self.getPlayerPos()[0], 
                           fill='black', 
                           font='Arial 8')
        

class GameModalApp(ModalApp):
    def appStarted(self):
        self.mainMode = MainMode()
#         self.battleMode = BattleMode()
        self.setActiveMode(app.mainMode)
        self.timerDelay = 50

class GameDelegator(object):
    def __init__(self, name, width=200, height=130, x=750, y=550, **kwargs):
        self.game = GameModalApp(width=width, height=height, **kwargs)
    
    def getInstance(self):
        return self.game
    
    def run(self):
        self.getInstance().run()

