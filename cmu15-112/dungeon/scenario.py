import pygame
import modal

class Scenario(GameObject):
    def __init__(self, config):
        super().__init__(config)
    
    def on_event(self, event):
        pass
    
    def on_action(self):
        pass
    
    def on_rendor(self, view):
        pass


class DefaultScenario(Scenario):
    def __init__(self, config):
        super().__init__(config)
        
        # constant
        self.CELL_PIXEL = config.CELL_PIXEL
        self.MAP_PADDING_BLOCK = config.MAP_PADDING_BLOCK
        self.PADDING_PIXEL = config.PADDING_PIXEL
        
        # maps
        self.maps = dict()
        self.map = None
        
        # slide window frame setting
        self.slideWindowRow = config.slideWindowRow
        self.slideWindowCol = config.slideWindowCol
        
        self.offsetRow = self.slideWindowRow // 2
        self.offsetCol = self.slideWindowCol // 2
        
        self.scrollRowIdx = 0
        self.scrollColIdx = 0
        
        # player
        self.player = None
        self.initPlayer()

    def appendMap(self, m):
        if isinstance(m, Map):
            self.maps[m.getName()] = m
    
    def setActiveMap(self, name):
        if name in self.maps.keys():
            self.map = self.maps[name]
    
    def getActiveMap(self):
        return self.map
    
    def initPlayer(self):
        self.player = Player('Hero')

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
        
    def on_event(self, event):
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
    
    def on_action(self):
        pass
    
    def on_rendor(self, view):
        view.render(self)
    
    def redrawAll(self, view)
        dx = self.MAP_PADDING_BLOCK * self.PADDING_PIXEL
        dy = self.MAP_PADDING_BLOCK * self.PADDING_PIXEL
        self.drawSlideWindow(view, dx, dy)
        self.drawText(view, dx, dy)
        
    def drawSlideWindow(self, view, dx, dy):
        self.drawMap(view, dx, dy)
        self.drawPlayer(view, dx, dy)

    def drawMap(self, view, dx, dy):
        # slide window border
        x0 = dx
        y0 = dy
        x1 = x0 + self.slideWindowCol * self.CELL_PIXEL
        y1 = y0 + self.slideWindowRow * self.CELL_PIXEL
        fill = 'white'
#         view.create_rectangle(x0, y0, x1, y1, fill=fill)
        
        # grid
        for i in range(1, self.slideWindowRow):
            x0 = dx
            y0 = dy + i * self.CELL_PIXEL
            x1 = x0 + self.slideWindowCol * self.CELL_PIXEL
            y1 = y0
            fill = 'grey'
#             view.create_line(x0, y0, x1, y1, fill=fill)
            
        for j in range(1, self.slideWindowCol):
            x0 = dx + j * self.CELL_PIXEL
            y0 = dy
            x1 = x0
            y1 = y0 + self.slideWindowRow * self.CELL_PIXEL
            fill = 'grey'
#             view.create_line(x0, y0, x1, y1, fill=fill)
        
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
#                     view.create_oval(x0, y0, x1, y1, fill='black')
#                     view.create_text(x1 + 20, 
#                                        (y0 + y1) / 2, 
#                                        text='(%d, %d)' % (sRowIdx, sColIdx), 
#                                        fill='black', 
#                                        font='Arial 8')

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
        
    def drawPlayer(self, view, dx, dy):
        (curRowIdx, curColIdx) = self.getPlayerPos()
        (slideRowIdx, slideColIdx) = self.convertToSlideWindowPos(curRowIdx, curColIdx)
        
        x0 = dx + slideColIdx * self.CELL_PIXEL
        y0 = dy + slideRowIdx * self.CELL_PIXEL
        x1 = x0 + self.CELL_PIXEL
        y1 = y0 + self.CELL_PIXEL
#         view.create_oval(x0 + 1, 
#                            y0 + 1, 
#                            x1 - 1, 
#                            y1 - 1, 
#                            fill='grey')
        # debug
#         view.create_text(x1 + 20, 
#                            (y0 + y1) / 2, 
#                            text='(%d, %d)' % (slideRowIdx, slideColIdx), 
#                            fill='black', 
#                            font='Arial 8')
    
    def drawText(self, view, dx, dy):
        # map border
#         view.create_text(dx + self.slideWindowCol * self.CELL_PIXEL // 2,
#                            dy + self.slideWindowRow * self.CELL_PIXEL + self.PADDING_PIXEL // 2, 
#                            text='slide (r%d x c%d)' % self.getSlideWindowBorder(), 
#                            fill='black', 
#                            font='Arial 8')
#         view.create_text(dx + self.slideWindowCol * self.CELL_PIXEL // 2, 
#                            dy + self.slideWindowRow * self.CELL_PIXEL + self.PADDING_PIXEL + self.PADDING_PIXEL // 2, 
#                            text='map (r%d x c%d)' % self.getMapBorder(), 
#                            fill='black', 
#                            font='Arial 8')
        
        # debug
        self.drawDebugText(view, dx, dy)
    
    def drawDebugText(self, view, dx, dy):
        # scroll window index
#         view.create_text(dx + self.CELL_PIXEL // 2, 
#                            self.PADDING_PIXEL // 2, 
#                            text='%d' % self.scrollColIdx, 
#                            fill='black', 
#                            font='Arial 8')
#         view.create_text(self.PADDING_PIXEL // 2, 
#                            dy + self.CELL_PIXEL // 2, 
#                            text='%d' % self.scrollRowIdx, 
#                            fill='black', 
#                            font='Arial 8')
        
        # offset index
#         view.create_text(dx + (self.offsetCol - 1) * self.CELL_PIXEL + self.CELL_PIXEL // 2, 
#                            self.PADDING_PIXEL // 2, 
#                            text='%d' % (self.offsetCol - 1), 
#                            fill='grey', 
#                            font='Arial 8')
#         view.create_text(self.PADDING_PIXEL // 2, 
#                            dy + (self.offsetRow - 1) * self.CELL_PIXEL + self.CELL_PIXEL // 2, 
#                            text='%d' % (self.offsetRow - 1), 
#                            fill='grey', 
#                            font='Arial 8')
        
        # player position index
#         view.create_text(dx + self.CELL_PIXEL // 2, 
#                            self.PADDING_PIXEL + self.PADDING_PIXEL // 2, 
#                            text='%d' % self.getPlayerPos()[1], 
#                            fill='black', 
#                            font='Arial 8')
#         view.create_text(self.PADDING_PIXEL + self.PADDING_PIXEL // 2, 
#                            dy + self.CELL_PIXEL // 2, 
#                            text='%d' % self.getPlayerPos()[0], 
#                            fill='black', 
#                            font='Arial 8')

# class BattleScenario(Scenario):
#     def __init__(self, name, player, monster, **kwargs):
#         super().__init__(name, **kwargs)
#         self.player = player
#         self.monster = monster
    
#     def battle(self, attacker, defencer):
#         pass
