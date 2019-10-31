from cmu_112_graphics import *
from tkinter import *
from dungeon import *

def testAll():
    testConvertToSlideWindowPos()
    testMovePlayer()
    
def testMovePlayer():
    d = GameDelegator('Test', autorun=False)
    g = d.getInstance()
    
    map = Map('test_12_16', 12, 16)
    g.appendMap(map)
    g.setActiveMap('test_12_16')
    
    print("Testing movePlayer and scrollMap...", end="")
    assert(g.getMapBorder() == (12, 16))
    assert(g.getSlideWindowBorder() == (7, 11))
    
    assert(g.getPlayerPos() == (0, 0))
    assert(g.getScrollIndex() == (0, 0))
    g.movePlayer(0, +4)
    assert(g.getPlayerPos() == (0, 4))
    assert(g.getScrollIndex() == (0, 0))
    g.movePlayer(0, +1)
    assert(g.getPlayerPos() == (0, 5))
    assert(g.getScrollIndex() == (0, 1))
    g.movePlayer(0, +4)
    assert(g.getPlayerPos() == (0, 9))
    assert(g.getScrollIndex() == (0, 5))
    g.movePlayer(0, +1)
    assert(g.getPlayerPos() == (0, 10))
    assert(g.getScrollIndex() == (0, 5))
    g.movePlayer(0, +5)
    assert(g.getPlayerPos() == (0, 15))
    assert(g.getScrollIndex() == (0, 5))
    
    g.movePlayer(+2, 0)
    assert(g.getPlayerPos() == (2, 15))
    assert(g.getScrollIndex() == (0, 5))
    g.movePlayer(+1, 0)
    assert(g.getPlayerPos() == (3, 15))
    assert(g.getScrollIndex() == (1, 5))
    g.movePlayer(+4, 0)
    assert(g.getPlayerPos() == (7, 15))
    assert(g.getScrollIndex() == (5, 5))
    g.movePlayer(+1, 0)
    assert(g.getPlayerPos() == (8, 15))
    assert(g.getScrollIndex() == (5, 5))
    g.movePlayer(+3, 0)
    assert(g.getPlayerPos() == (11, 15))
    assert(g.getScrollIndex() == (5, 5))
    
    print("Pass!")

def testConvertToSlideWindowPos():
    d = GameDelegator('Test', autorun=False)
    g = d.getInstance()
    
    map = Map('test_12_16', 12, 16)
    g.appendMap(map)
    g.setActiveMap('test_12_16')
    
    print("Testing convertToSlideWindowPos...", end="")
    assert(g.getMapBorder() == (12, 16))
    assert(g.getSlideWindowBorder() == (7, 11))
    
    assert(g.convertToSlideWindowPos(0, 0) == (0, 0))
    assert(g.convertToSlideWindowPos(0, 3) == (0, 3))
    assert(g.convertToSlideWindowPos(0, 4) == (0, 4))
    assert(g.convertToSlideWindowPos(0, 9) == (0, 4))
    assert(g.convertToSlideWindowPos(0, 10) == (0, 5))
    assert(g.convertToSlideWindowPos(0, 15) == (0, 10))
    
    assert(g.convertToSlideWindowPos(1, 0) == (1, 0))
    assert(g.convertToSlideWindowPos(2, 0) == (2, 0))
    assert(g.convertToSlideWindowPos(7, 0) == (2, 0))
    assert(g.convertToSlideWindowPos(8, 0) == (3, 0))
    assert(g.convertToSlideWindowPos(11, 0) == (6, 0))
    
    assert(g.convertToSlideWindowPos(11, 15) == (6, 10))
    
    print("Pass!")