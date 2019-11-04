import modal

from modal import *


defaultGlobalConfig = {
    'name': 'DND',
    'width': 400,
    'height': 300,
    'fps': 50
}

defaultScenarioConfig = {
    'name': 'default_scenario',
    'width': 400,
    'height': 300,
    
    'CELL_PIXEL': 10,
    'MAP_PADDING_BLOCK': 2,
    'PADDING_PIXEL': 15,
    
    'slideWindowRow': 7,
    'slideWindowCol': 11
}

defaultMapConfig = {
    'name': 'default_map',
    'row': 11,
    'col': 16,
    'p': 0.98
}

defaultPlayerConfig = {
    'name': 'Hero'
}

class GameDelegator(object):
    def __init__(self):
        m = DefaultMap(Config(**defaultMapConfig))
        p = Player(Config(**defaultPlayerConfig))
        
        s = DefaultScenario(Config(**defaultScenarioConfig))
        s.appendMap(m)
        s.setActiveMap(m.getName())
        s.setPlayer(p)
        
        self.modal = PygModal(Config(**defaultGlobalConfig))
        self.modal.appendScenario(s)
        print(s.getName())
        self.modal.setActiveScenario(s.getName())

#     def getInstance(self):
#         return self
    
    def run(self):
        self.modal.run()