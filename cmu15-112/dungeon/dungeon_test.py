import dungeon
from dungeon import *

testGlobalConfig = {
    'name': 'test_case'
}

testViewConfig = {
    'name': 'test_400x300',
    'width': 400,
    'height': 300,
    'fps': 50
}

testScenarioConfig = {
    'name': 'test_scenario',
    'width': 400,
    'height': 300,
    
    'CELL_PIXEL': 15,
    'MAP_PADDING_BLOCK': 2,
    'PADDING_PIXEL': 20,
    
    'slideWindowRow': 7,
    'slideWindowCol': 11
}

testMapConfig = {
    'name': 'test_map',
    'row': 12,
    'col': 16,
    'p': 0.98
}

testPlayerConfig = {
    'name': 'DummyPlayer'
}

    
def testMovePlayer():
    m = DefaultMap(Config(**testMapConfig))
    p = Player(Config(**testPlayerConfig))
        
    s = DefaultScenario(Config(**testScenarioConfig))
    s.appendMap(m)
    s.setActiveMap(m.getName())
    s.setPlayer(p)

    print("Testing movePlayer and scrollMap...", end="")
    assert(s.getMapBorder() == (12, 16))
    assert(s.getSlideWindowBorder() == (7, 11))
    
    assert(s.getPlayerPos() == (0, 0))
    assert(s.getScrollIndex() == (0, 0))
    s.movePlayer(0, +4)
    assert(s.getPlayerPos() == (0, 4))
    assert(s.getScrollIndex() == (0, 0))
    s.movePlayer(0, +1)
    assert(s.getPlayerPos() == (0, 5))
    assert(s.getScrollIndex() == (0, 1))
    s.movePlayer(0, +4)
    assert(s.getPlayerPos() == (0, 9))
    assert(s.getScrollIndex() == (0, 5))
    s.movePlayer(0, +1)
    assert(s.getPlayerPos() == (0, 10))
    assert(s.getScrollIndex() == (0, 5))
    s.movePlayer(0, +5)
    assert(s.getPlayerPos() == (0, 15))
    assert(s.getScrollIndex() == (0, 5))
    
    s.movePlayer(+2, 0)
    assert(s.getPlayerPos() == (2, 15))
    assert(s.getScrollIndex() == (0, 5))
    s.movePlayer(+1, 0)
    assert(s.getPlayerPos() == (3, 15))
    assert(s.getScrollIndex() == (1, 5))
    s.movePlayer(+4, 0)
    assert(s.getPlayerPos() == (7, 15))
    assert(s.getScrollIndex() == (5, 5))
    s.movePlayer(+1, 0)
    assert(s.getPlayerPos() == (8, 15))
    assert(s.getScrollIndex() == (5, 5))
    s.movePlayer(+3, 0)
    assert(s.getPlayerPos() == (11, 15))
    assert(s.getScrollIndex() == (5, 5))
    
    print("Pass!")

def testConvertToSlideWindowPos():
    m = DefaultMap(Config(**testMapConfig))
    p = Player(Config(**testPlayerConfig))
        
    s = DefaultScenario(Config(**testScenarioConfig))
    s.appendMap(m)
    s.setActiveMap(m.getName())
    s.setPlayer(p)
    
    print("Testing convertToSlideWindowPos...", end="")
    assert(s.getMapBorder() == (12, 16))
    assert(s.getSlideWindowBorder() == (7, 11))
    
    assert(s.convertToSlideWindowPos(0, 0) == (0, 0))
    assert(s.convertToSlideWindowPos(0, 3) == (0, 3))
    assert(s.convertToSlideWindowPos(0, 4) == (0, 4))
    assert(s.convertToSlideWindowPos(0, 9) == (0, 4))
    assert(s.convertToSlideWindowPos(0, 10) == (0, 5))
    assert(s.convertToSlideWindowPos(0, 15) == (0, 10))
    
    assert(s.convertToSlideWindowPos(1, 0) == (1, 0))
    assert(s.convertToSlideWindowPos(2, 0) == (2, 0))
    assert(s.convertToSlideWindowPos(7, 0) == (2, 0))
    assert(s.convertToSlideWindowPos(8, 0) == (3, 0))
    assert(s.convertToSlideWindowPos(11, 0) == (6, 0))
    
    assert(s.convertToSlideWindowPos(11, 15) == (6, 10))
    
    print("Pass!")


def testAll():
    testConvertToSlideWindowPos()
    testMovePlayer()

if __name__ == '__main__':
    testAll()