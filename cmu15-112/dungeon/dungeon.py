import modal

globalConfig = {
    'width': 400,
    'height': 300,
    'fps': 50
}

defaultScenarioConfig = {
    'name': 'default_scenario'
    'width': 400,
    'height': 300,
    
    'CELL_PIXEL': 10,
    'MAP_PADDING_BLOCK': 2,
    'PADDING_PIXEL': 15,
    
    'slideWindowRow': 7,
    'slideWindowCol': 11
}

mapConfig = {
    'name': 'default_map'
    'row': 11,
    'col': 16,
    'p': 0.98
}


class GameDelegator(object):
    def __init__(self):
        m = Map(Config(**mapConfig))
        
        s = DefaultScenario(Config(**defaultScenarioConfig))
        s.appendMap(m)
        s.setActiveMap(m)
        
        pyg = PygModal(Config(**globalConfig))
        pyg.setActiveScenario(s)
    
    def getInstance(self):
        return self
    
    def run(self):
        pyg.run()