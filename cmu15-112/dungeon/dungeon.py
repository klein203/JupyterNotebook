import random, uuid
import pygame
from abc import ABC, abstractmethod


defaultGlobalConfig = {
    'name': 'DND'
}

defaultViewConfig = {
    'name': '400x300',
    'width': 400,
    'height': 300,
    'fps': 50,
    
#     'fontname': 'arial',
    'fontname': 'calibri',
    'fontsize': 10
}

defaultScenarioConfig = {
    'name': 'default_scenario',
    'width': 400,
    'height': 300,
    
    'CELL_PIXEL': 20,
    'MAP_PADDING_BLOCK': 2,
    'PADDING_PIXEL': 30,
    
    'slideWindowRow': 10,
    'slideWindowCol': 15
}

defaultMapConfig = {
    'name': 'default_map',
    'row': 15,
    'col': 20,
    'randomMode': True,
    'p': 0.98
}

defaultPlayerConfig = {
    'name': 'Hero'
}


class Logger(object):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    FATAL = 3
    
    LEVEL_MSG = ['D', 'I', 'W', 'E', 'F']
    
    def __init__(self):
        pass
        
    def setLevel(self, level):
        self.level = level
    
    def log(self, message):
        print('[%s] %s' % (LEVEL_MSG[self.level], message))
    
    def log(self, message, level):
        if level >= self.level:
            print('[%s] %s' % (LEVEL_MSG[level], message))
        
    def debug(self, message):
        self.log(message, level=Logger.DEBUG)
        
    def info(self, message):
        self.log(message, level=Logger.INFO)
        
    def warning(self, message):
        self.log(message, level=Logger.WARNING)
    
    def error(self, message):
        self.log(message, level=Logger.ERROR)
        
    def fatal(self, message):
        self.log(message, level=Logger.FATAL)


class Config(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class GameObject(object):
    SCENARIO = 0
    MAP = 1
    MONSTER = 2
    PLAYER = 3
    ITEM = 4
    
    def __init__(self, objType, config):
        self.uuid = uuid.uuid4()
        self.name = config.name
        self.type = objType
    
    def __repr__(self):
#         return "%s - %s" % (self.__class__.__name__, self.getName())
        return self.name
    
    def getUUID(self):
        return self.uuid
    
    def getName(self):
        return self.name
    
    def getType(self):
        return self.type


class Scenario(GameObject):
    def __init__(self, modal, config):
        super().__init__(GameObject.SCENARIO, config)
        self.modal = modal
    
    def on_event(self, event):
        raise NotImplementedError("function on_event() should be implemented")
    
    def on_action(self):
        raise NotImplementedError("function on_action() should be implemented")
    
    def on_rendor(self, view):
        raise NotImplementedError("function on_rendor() should be implemented")
    
    def isDebugMode(self):
        return self.getModal().isDebugMode()
    
    def getModal(self):
        return self.modal


class DefaultScenario(Scenario):
    def __init__(self, modal, config):
        super().__init__(modal, config)
        
        # constant
        self.CELL_PIXEL = config.CELL_PIXEL
        self.MAP_PADDING_BLOCK = config.MAP_PADDING_BLOCK
        self.PADDING_PIXEL = config.PADDING_PIXEL
        
        # slide window frame setting
        self.slideWindowCol = config.slideWindowCol
        self.slideWindowRow = config.slideWindowRow
        
        self.offsetCol = self.slideWindowCol // 2
        self.offsetRow = self.slideWindowRow // 2
        
        self.scrollColIdx = 0
        self.scrollRowIdx = 0
        
        # maps
        self.maps = dict()
        self.map = None
        
        # items
        self.items = dict()
        
        # player
        self.player = None
        

    def reset(self):
        self.scrollColIdx = 0
        self.scrollRowIdx = 0
        
        self.player.reset()
    
    def getCellPixel(self):
        return self.CELL_PIXEL
    
    def appendMap(self, m):
        if isinstance(m, Map):
            self.maps[m.getName()] = m
        else:
            loggerError('Error in loading map %s' % m)
    
    def setActiveMap(self, name):
        if name in self.maps.keys():
            self.map = self.maps[name]
    
    def getActiveMap(self):
        return self.map

    def getMapBorder(self):
        return self.map.getBorder()
    
    def getScrollIndex(self):
        return (self.scrollColIdx, self.scrollRowIdx)
    
    def setSlideWindowBorder(self, col, row):
        self.slideWindowCol = col
        self.slideWindowRow = row
        self.offsetCol = self.slideWindowCol // 2
        self.offsetRow = self.slideWindowRow // 2

    def getSlideWindowBorder(self):
        return (self.slideWindowCol, self.slideWindowRow)
    
    def setPlayer(self, p):
        self.player = p
        
    def getPlayer(self):
        return self.player

    def getPlayerPos(self):
        return self.player.getPos()
    
#     def movePlayerToPos(self, col, row):
#         self.player.moveToPos(col, row)
#         self.updateScrollIndex()
    
    def movePlayer(self, dcol, drow):
        curColIdx, curRowIdx = self.getPlayerPos()
        
        tryColIdx = curColIdx + dcol
        tryRowIdx = curRowIdx + drow
        
        mapBorderCol, mapBorderRow = self.getMapBorder()
        
        if tryColIdx >= 0 and tryColIdx < mapBorderCol and tryRowIdx >= 0 and tryRowIdx < mapBorderRow:
            if self.hasBlock(tryColIdx, tryRowIdx) == False:
                self.player.move(dcol, drow)
                self.updateScrollIndex()
    
    def hasBlock(self, colIdx, rowIdx):
        return self.getActiveMap().hasBlock(colIdx, rowIdx)
    
    def updateScrollIndex(self):
        curColIdx, curRowIdx = self.getPlayerPos()
        mapBorderCol, mapBorderRow = self.getMapBorder()

        if curColIdx < self.offsetCol:
            self.scrollColIdx = 0
        elif curColIdx < mapBorderCol - self.slideWindowCol + self.offsetCol:
            self.scrollColIdx = curColIdx - self.offsetCol + 1
        else:
            self.scrollColIdx = mapBorderCol - self.slideWindowCol
        
        if curRowIdx < self.offsetRow:
            self.scrollRowIdx = 0
        elif curRowIdx < mapBorderRow - self.slideWindowRow + self.offsetRow:
            self.scrollRowIdx = curRowIdx - self.offsetRow + 1
        else:
            self.scrollRowIdx = mapBorderRow - self.slideWindowRow
        
    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.movePlayer(0, +1)
            elif event.key == pygame.K_LEFT:
                self.movePlayer(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.movePlayer(+1, 0)
            elif event.key == pygame.K_UP:
                self.movePlayer(0, -1)
    
    def on_action(self):
        # dummy action
        pass
    
    def on_render(self, view):
        dx = self.MAP_PADDING_BLOCK * self.PADDING_PIXEL
        dy = self.MAP_PADDING_BLOCK * self.PADDING_PIXEL
        self.drawSlideWindow(view, dx, dy)
#         self.drawText(view, dx, dy)
        
    def drawSlideWindow(self, view, dx, dy):
        self.drawMap(view, dx, dy)
        self.drawPlayer(view, dx, dy)

    def drawMap(self, view, dx, dy):
        # slide window border
        x = dx
        y = dy
        w = self.slideWindowCol * self.CELL_PIXEL
        h = self.slideWindowRow * self.CELL_PIXEL

        self.getActiveMap().draw(view, **{'xywh': ((x, y), (w, h))})

    def convertToSlideWindowPos(self, colIdx, rowIdx):
        sColIdx = self.offsetCol - 1
        sRowIdx = self.offsetRow - 1

        mapBorderCol, mapBorderRow = self.getMapBorder()
        
        if colIdx < self.offsetCol:
            sColIdx = colIdx
        elif colIdx > mapBorderCol - (self.slideWindowCol - self.offsetCol) - 1:
            sColIdx = colIdx - (mapBorderCol - self.slideWindowCol)
        
        if rowIdx < self.offsetRow:
            sRowIdx = rowIdx
        elif rowIdx > mapBorderRow - (self.slideWindowRow - self.offsetRow) - 1:
            sRowIdx = rowIdx - (mapBorderRow - self.slideWindowRow)
        
        return (sColIdx, sRowIdx)
        
    def drawPlayer(self, view, dx, dy):
        (curColIdx, curRowIdx) = self.getPlayerPos()
        (slideColIdx, slideRowIdx) = self.convertToSlideWindowPos(curColIdx, curRowIdx)
        pad = 3
        x = dx + slideColIdx * self.CELL_PIXEL + pad
        y = dy + slideRowIdx * self.CELL_PIXEL + pad
        w = self.CELL_PIXEL - 2 * pad
        h = w
        
        self.getPlayer().draw(view, **{'xywh': ((x, y), (w, h))})
        
    def drawText(self, view, dx, dy):
        # map border
        view.text((dx + (self.CELL_PIXEL - view.fontsize) // 2, 
                   dy + self.slideWindowRow * self.CELL_PIXEL + (self.CELL_PIXEL - view.fontsize) // 2),
                  text="slide (r%d x c%d)" % self.getSlideWindowBorder(), 
                  color=View.COLOR_BLACK)
        
        view.text((dx + (self.CELL_PIXEL - view.fontsize) // 2, 
                   dy + self.slideWindowRow * self.CELL_PIXEL + (self.CELL_PIXEL - view.fontsize) // 2),
                  text="map (r%d x c%d)" % self.getMapBorder(),
                  color=View.COLOR_BLACK)
        
        # debug
        self.drawDebugText(view, dx, dy)
    
    def drawDebugText(self, view, dx, dy):
        pass
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
#                            text='%d' % self.getPlayerPos()[0], 
#                            fill='black', 
#                            font='Arial 8')
#         view.create_text(self.PADDING_PIXEL + self.PADDING_PIXEL // 2, 
#                            dy + self.CELL_PIXEL // 2, 
#                            text='%d' % self.getPlayerPos()[1], 
#                            fill='black', 
#                            font='Arial 8')

# class BattleScenario(Scenario):
#     def __init__(self, modal, config):
#         super().__init__(modal, config)
    
#     def battle(self, attacker, defencer):
#         pass


class Map(GameObject):
    def __init__(self, scenario, config):
        super().__init__(GameObject.MAP, config)
        self.scenario = scenario
    
    def isDebugMode(self):
        return self.scenario.isDebugMode()
    
    def getScenario(self):
        return self.scenario

    def draw(self, view, **kwargs):
        raise NotImplementedError("function draw() should be implemented")


class DefaultMap(Map):
    def __init__(self, scenario, config):
        super().__init__(scenario, config)
        
        self.col = config.col
        self.row = config.row
        self.board = [([0] * self.col) for i in range(self.row)]

        if config.randomMode:
            self.randomMap(config.p)
        
    def getBorder(self):
        return self.col, self.row
    
    def hasBlock(self, colIdx, rowIdx):
        if self.board[rowIdx][colIdx] == 0:
            return False
        else:
            return True
    
    def randomMap(self, p=0.999):
        for i in range(self.row):
            for j in range(self.col):
                if random.random() > p:
                    self.board[i][j] = 1
    
    def draw(self, view, **kwargs):
        ((x, y), (w, h)) = kwargs['xywh']
        view.rectangle(((x, y), (w, h)), color=View.COLOR_BLACK, border=1)
        
        # grid
        if self.isDebugMode():
            (slideWindowCol, slideWindowRow) = self.getScenario().getSlideWindowBorder()
            cellPixel = self.getScenario().getCellPixel()
            for j in range(1, slideWindowCol):
                start_x = dx + j * cellPixel
                start_y = dy
                end_x = start_x
                end_y = start_y + slideWindowRow * cellPixel
                view.line((start_x, start_y), (end_x, end_y), color=View.COLOR_LIGHT_GREY, border=1)

            for i in range(1, slideWindowRow):
                start_x = dx
                start_y = dy + i * cellPixel
                end_x = start_x + slideWindowCol * cellPixel
                end_y = start_y
                view.line((start_x, start_y), (end_x, end_y), color=View.COLOR_LIGHT_GREY, border=1)
            
        
        # block cells
        for i in range(self.slideWindowRow):
            for j in range(self.slideWindowCol):
                sColIdx = j + self.scrollColIdx
                sRowIdx = i + self.scrollRowIdx
                if self.hasBlock(sColIdx, sRowIdx):
                    pad = 2
                    x = dx + j * self.CELL_PIXEL + pad
                    y = dy + i * self.CELL_PIXEL + pad
                    w = self.CELL_PIXEL - 2 * pad
                    h = w
                    view.rectangle(((x, y), (w, h)), color=View.COLOR_BLACK, border=0)
                    if self.isDebugMode():
                        view.text((x + self.CELL_PIXEL, y + (self.CELL_PIXEL - view.fontsize) // 2),
                                  text='(%d, %d)' % (sColIdx, sRowIdx), 
                                  color=View.COLOR_BLACK)


class Creature(GameObject):
    def __init__(self, objType, scenario, config):
        super().__init__(objType, config)
        self.scenario = scenario
        
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
        self.colIdx = 0
        self.rowIdx = 0
        
        # dice
        self.maxDice = 20
    
    def dice(self):
        return random.randint(1, self.maxDice)
    
    def move(self, dcol, drow):
        self.colIdx += dcol
        self.rowIdx += drow
    
#     def moveToPos(self, rowIdx, colIdx):
#         self.rowIdx = rowIdx
#         self.colIdx = colIdx
    
    def getPos(self):
        return self.colIdx, self.rowIdx
    
    def reset(self):
        self.colIdx = 0
        self.rowIdx = 0
    
    def draw(self, view, **kwargs):
        raise NotImplementedError("function draw() should be implemented")
    
    def isDebugMode(self):
        return self.getScenario().isDebugMode()

    def getScenario(self):
        return self.scenario


class Player(Creature):
    def __init__(self, scenario, config):
        super().__init__(GameObject.PLAYER, scenario, config)
    
    def draw(self, view, **kwargs):
        ((x, y), (w, h)) = kwargs['xywh']
        view.rectangle(((x, y), (w, h)), color=View.COLOR_GREY, border=0)
        
        # debug
        if self.isDebugMode():
            offset = self.getScenario().getCellPixel()
            view.text((x + offset, y),
                      text='(%d, %d)' % (self.colIdx, self.rowIdx), 
                      color=View.COLOR_GREY)


class Monster(Creature):
    def __init__(self, scenario, config):
        super().__init__(GameObject.MONSTER, scenario, config)


class Item(GameObject):
    def __init__(self, scenario, config):
        super().__init__(GameObject.ITEM, config)
        self.scenario = scenario
    
    def isDebugMode(self):
        return self.scenario.isDebugMode()
    
    def getScenario(self):
        return self.scenario

    def draw(self, view, **kwargs):
        raise NotImplementedError("function draw() should be implemented")


class MountainItem(Item):
    def __init__(self, scenario, config):
        super().__init__(scenario, config)
    
    def draw(self, view, **kwargs):
        pass


class PygModal(GameObject):
    def __init__(self, config):
        super().__init__(config)
        pygame.init()
        self.running = False
        
        # all scenarios
        self.scenarios = dict()
        self.scenario = None
        
        self.view = None
        
        self.debugMode = False
    
    def methodWrapper(appMethod):
        def m(*args, **kwargs):
            logger.debug('begin %s' % appMethod)
            ret = appMethod(*args, **kwargs)
            logger.debug('end %s, ret %s' % (appMethod, ret))
            return ret
        
        return m
    
    def setDebugMode(self, mode=True):
        self.debugMode = mode
    
    def toggleDebugMode(self):
        self.debugMode = not self.debugMode
    
    def isDebugMode(self):
        return self.debugMode
    
    def appendScenario(self, s):
        if isinstance(s, Scenario):
            self.scenarios[s.getName()] = s
        else:
            loggerError('Error in loading scenario %s' % s)
    
    def setActiveScenario(self, name):
        if name in self.scenarios.keys():
            self.scenario = self.scenarios[name]
        else:
            loggerError('Error in setting active scenario' % name)
    
    def getActiveScenario(self):
        return self.scenario

    def setView(self, view):
        self.view = view
    
    def getView(self):
        return self.view
    
    def getViewFPS(self):
        return self.view.getFPS()
    
    def viewTick(self):
        self.view.tick()
    
    def viewRender(self):
        # overall
        caption = "%s%s - FPS@%d" % (self.getName(), '[DEBUG]' if self.isDebugMode() else '', self.getViewFPS())
        pygame.display.set_caption(caption)
        
        # active scenario render
        self.getActiveScenario().on_render(self.getView())
            
        # view rendor
        self.getView().render()
    
    def run(self):
        self.running = True
        
        if self.getActiveScenario() == None:
            pygame.quit()
            return
        
        while self.running:
            self.viewTick()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_d:
                        self.toggleDebugMode()
                
                self.getActiveScenario().on_event(event)

#             self.getActiveScenario().on_action()
            
            self.viewRender()
            
        pygame.quit()


class View(GameObject):
    COLOR_BLACK = (0, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_LIGHT_GREY = (191, 191, 191)
    COLOR_GREY = (127, 127, 127)
    COLOR_DARK_GREY = (63, 63, 63)
    
    def __init__(self, modal, config):
        super().__init__(config)
        self.modal = modal
        
        self.width = config.width
        self.height = config.height
        
        # clock tick and fps
        self.fps = config.fps
        self.clock = pygame.time.Clock()
        
        # font
        if pygame.font.get_init() == False:
            pygame.font.init()

        self.fontname = config.fontname
        self.fontsize = config.fontsize
        self.font = pygame.font.SysFont(self.fontname, self.fontsize, bold=False)
        
        # canvas
        self.canvas = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.canvas.get_size()).convert()
        self.background.fill(View.COLOR_WHITE)
    
    def getFPS(self):
        return self.clock.get_fps()
    
    def tick(self):
        return self.clock.tick_busy_loop(self.fps)
    
    def render(self):
        pygame.display.flip()
        self.canvas.blit(self.background, (0, 0))
    
    def rectangle(self, xywh, color, border=1):
        pygame.draw.rect(self.canvas, color, xywh, border)

    def line(self, start_xy, end_xy, color, border=1):
        pygame.draw.line(self.canvas, color, start_xy, end_xy, border)
    
    def circle(self, xy, r, color, border=0):
        pygame.draw.circle(self.canvas, color, xy, r, border)

    def text(self, xy, text, color):
        surface = self.font.render(text, True, color)
        self.canvas.blit(surface, xy)


class DefaultView(View):
    def __init__(self, modal, config):
        super().__init__(modal, config)


class GameDelegator(object):
    def __init__(self):
        self.modal = PygModal(Config(**defaultGlobalConfig))
        
        s = DefaultScenario(self.modal, Config(**defaultScenarioConfig))
        
        m = DefaultMap(s, Config(**defaultMapConfig))
        s.appendMap(m)
        s.setActiveMap(m.getName())

        p = Player(s, Config(**defaultPlayerConfig))
        s.setPlayer(p)
        
        self.modal.appendScenario(s)
        self.modal.setActiveScenario(s.getName())
        
        v = DefaultView(self.modal, Config(**defaultViewConfig))
        self.modal.setView(v)

    def run(self):
        self.modal.run()


def main():
    logger = Logger()
    logger.setLevel(Logger.DEBUG)
    GameDelegator().run()
    
if __name__ == '__main__':
    main()