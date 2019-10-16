#################################################
# hw7.py: Tetris!
#
# Your name:
# Your andrew id:
#
# Your partner's name:
# Your partner's andrew id:
#################################################

import cs112_f19_week7_linter
import math, copy, random

from cmu_112_graphics import *
from tkinter import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

def gameDimensions():
#     rows, cols, cellSize, margin = 15, 10, 20, 25
    rows, cols, cellSize, margin = 15, 10, 12, 10
    return (rows, cols, cellSize, margin)

def playTetris():
    (rows, cols, cellSize, margin) = gameDimensions()
    width = cols * cellSize + margin * 2
    height = rows * cellSize + margin * 2
#     runApp(width=width, height=height)
    runApp(width=width, height=height, x=1200, y=500)

# app start
def appStarted(app):
    iPiece = [[ True,  True,  True, True]]
    jPiece = [[ True, False, False],
              [ True,  True,  True]]
    lPiece = [[False, False,  True],
              [ True,  True,  True]]
    oPiece = [[ True,  True],
              [ True,  True]]
    sPiece = [[False,  True,  True],
              [ True,  True, False]]
    tPiece = [[False,  True, False],
              [ True,  True,  True]]
    zPiece = [[ True,  True, False],
              [False,  True,  True]]
    vPiece = [[ True,  False, True],
              [False,  True,  False]]
    pPiece = [[ True,  True,  True],
              [False,  True,  True]]
    qPiece = [[ True,  True, False],
              [ True,  True,  True]]
    
    app.SETTING = {
        'LINES_PER_LEVEL_UP': 5,
        'CELL_WIDTH': 3,
        'TIMER_DELAY': 300,
        'START_LEVEL': 1,
        'MAX_LEVEL': 10,
        'START_SCORE': 0,
        'BASIC_SCORES_PER_ROW': 10,
        'EMPTY_COLOR': 'blue',
        'NORMAL_BLK_IDX': 7,
        'PIECES': [iPiece, jPiece, lPiece, oPiece, sPiece,
                   tPiece, zPiece, vPiece, pPiece, qPiece],
        'PIECES_COLOR': ['red', 'yellow', 'magenta', 'pink', 'cyan',
                         'green', 'orange', 'moccasin', 'seashell', 'violet']
    }
    app.MESSAGE = {
        'GAME_PAUSE': 'Pause !',
        'GAME_OVER': 'Game Over !',
        'BONUS_MODE': 'Bonus Mode',
        'ON': 'On',
        'OFF': 'Off',
        'SCORE': 'Score',
        'LEVEL': 'Level'
    }
    app.timerDelay = app.SETTING["TIMER_DELAY"]
    app.level = app.SETTING["START_LEVEL"]
    app.score = app.SETTING["START_SCORE"]
    app.fullRows = 0
    app.isGameOver = False
#     app.isBonusMode = False
    app.isBonusMode = True
    app.rotateClockwise = False
    app.gamePaused = False
    
    (app.rows, app.cols, app.cellSize, app.margin) = gameDimensions()
    
    # init cells
    app.emptyColor = app.SETTING["EMPTY_COLOR"]
    app.board = [[app.emptyColor] * app.cols for i in range(app.rows)]
    
    # Seven "standard" pieces (tetrominoes)
    app.tetrisPieces = app.SETTING["PIECES"]
    app.tetrisPieceColors = app.SETTING["PIECES_COLOR"]
    
    newFallingPiece(app)
    
    # board test
#     app.board[0][0] = "red" # top-left is red
#     app.board[0][app.cols-1] = "white" # top-right is white
#     app.board[app.rows-1][0] = "green" # bottom-left is green
#     app.board[app.rows-1][app.cols-1] = "gray" # bottom-right is gray

# event driven, controller
def keyPressed(app, event):
    if not app.isGameOver:
        if event.key == 'p':
            toggleGamePause(app)
        elif event.key == 'Down':
            moveFallingPiece(app, +1, 0)
        elif event.key == 'Left':
            moveFallingPiece(app, 0, -1)
        elif event.key == 'Right':
            moveFallingPiece(app, 0, +1)
        elif event.key == 'Up':
            rotateFallingPiece(app)
        elif event.key == 'b':
            toggleGameMode(app)
    
        if app.isBonusMode:
            if event.key == 'Space':
                dropFallingPiece(app)
            elif event.key == 'c':
                toggleRotateMode(app)
    
    if event.key == 'r':
        appStarted(app)

def timerFired(app):
    if not app.isGameOver:
        if not app.gamePaused:
            if not moveFallingPiece(app, +1, 0):
                placeFallingPiece(app)
                removeFullRows(app)
                if app.isBonusMode:
                    generateRandomPiece(app)
                    removeFullRows(app)
                newFallingPiece(app)
                if not fallingPieceIsLegal(app):
                    # game over
                    app.isGameOver = True

# top-down functions to support controller
def newFallingPiece(app):
    gameBlkIdx = 0
    if app.isBonusMode:
        gameBlkIdx = len(app.tetrisPieces)
    else:
        gameBlkIdx = app.SETTING["NORMAL_BLK_IDX"]
    app.randomIndex = random.randint(0, gameBlkIdx - 1)
    app.fallingPiece = app.tetrisPieces[app.randomIndex]
    
    app.fpRowBlks = len(app.fallingPiece)
    app.fpColBlks = len(app.fallingPiece[0])
    app.fpRowIdx = 0
    app.fpColIdx = app.cols // 2 - app.fpColBlks // 2

def moveFallingPiece(app, drow, dcol):
    app.fpRowIdx += drow
    app.fpColIdx += dcol
    
    # restore if fails
    if not fallingPieceIsLegal(app):
        app.fpRowIdx -= drow
        app.fpColIdx -= dcol
        return False
    
    return True
    
def fallingPieceIsLegal(app):
    if app.fpRowIdx < 0:
        return False
    if app.fpRowIdx + app.fpRowBlks > app.rows:
        return False
    if app.fpColIdx < 0:
        return False
    if app.fpColIdx + app.fpColBlks > app.cols:
        return False
    
    for i in range(app.fpRowBlks):
        for j in range(app.fpColBlks):
            if app.fallingPiece[i][j]:
                row = app.fpRowIdx + i
                col = app.fpColIdx + j
                if app.board[row][col] != app.emptyColor:
                    return False
    
    return True

def rotateFallingPiece(app):
    # backup falling piece info
    fp = app.fallingPiece
    fpRowIdx = app.fpRowIdx
    fpColIdx = app.fpColIdx
    fpRowBlks = app.fpRowBlks
    fpColBlks = app.fpColBlks
    
    # transpose 2d-list
    app.fallingPiece = [[row[i] for row in fp] for i in range(fpColBlks)]
    # upside down 2d-list if counter-clockwised
    if not app.rotateClockwise:
        app.fallingPiece = [row for row in app.fallingPiece[::-1]]
    
    # update falling piece block size
    app.fpRowBlks = len(app.fallingPiece)
    app.fpColBlks = len(app.fallingPiece[0])
    
    # update falling piece position
    app.fpRowIdx = fpRowIdx + fpRowBlks // 2 - app.fpRowBlks // 2
    app.fpColIdx = fpColIdx + fpColBlks // 2 - app.fpColBlks // 2
    
    # restore if fails
    if not fallingPieceIsLegal(app):
        app.fallingPiece = fallingPiece
        app.fpRowIdx, app.fpColIdx = fpRowIdx, fpColIdx
        app.fpRowBlks, app.fpColBlks = fpRowBlks, fpColBlks
    
def placeFallingPiece(app):
    for i in range(app.fpRowBlks):
        for j in range(app.fpColBlks):
            if app.fallingPiece[i][j]:
                row = app.fpRowIdx + i
                col = app.fpColIdx + j
                app.board[row][col] = app.tetrisPieceColors[app.randomIndex]

def removeFullRows(app):
    # fetch all lines without emptyColor
    fullRows = [row for row in app.board if not app.emptyColor in row]
    cntFullRows = len(fullRows)
    if cntFullRows > 0:
        # remove these rows from board
        [app.board.remove(row) for row in fullRows]
    
        # generate emptyColor lines with the same shape of lines removed
        newBoard = [[app.emptyColor] * app.cols for i in range(cntFullRows)]
    
        # stack emptyColor rows on board which full rows removed
        newBoard.extend(app.board)
        app.board = newBoard

        # full rows removed
        updateFullRows(app, cntFullRows)
        
        # scoring
        updateScore(app, cntFullRows)
        
        # update difficulties
        updateDroppingSpeed(app)
        
        return cntFullRows

    return 0

def updateFullRows(app, rows):
    app.fullRows += rows
    
def updateScore(app, rows):
    basicRowScore = app.SETTING["BASIC_SCORES_PER_ROW"]
    weight = round(math.sqrt(app.level), 2)
    app.score += rows * int(basicRowScore * weight)

# feature: bonus mode toggle by pressing 'r'
def toggleGameMode(app):
    app.isBonusMode = not app.isBonusMode

# feature: hard drop by pressing 'Space' when in bonus mode
def dropFallingPiece(app):
    while moveFallingPiece(app, +1, 0):
        pass

# feature: rotate mode toggle by pressing 'c' when in bonus mode
def toggleRotateMode(app):
    app.rotateClockwise = not app.rotateClockwise

# feature: difficulty, raising dropping speed with level up, up to MAX_LEVEL
def updateDroppingSpeed(app):
    level = (app.fullRow - 1) // app.SETTING["LINES_PER_LEVEL_UP"] + 1
    app.level = min(level, app.SETTING["MAX_LEVEL"])
    # y = ax + b, which x: [1 ... 10], y: [1 ... 0.2]
    # then, a = - 0.8 / 9, b = 9.8 / 9
    a = - 0.8 / 9
    b = 9.8 / 9
    alpha = round(a * app.level + b, 2)
    basicTimerDelay = app.SETTING["TIMER_DELAY"]
    app.timerDelay = int(basicTimerDelay * alpha)
    
    # non-linear version
    # y = a * e ^ x + b, which x: [1 ... 10], y: [1 ... 0.2]
    # then, a = - 0.8 / (e - e ^ 10), b = 1 - 0.8 / (1 - e ^ 9)
#     a = 0.8 / (math.e - math.pow(math.e, 10))
#     b = 1 - 0.8 / (1 - math.pow(math.e, 9))
#     alpha = round(a * math.pow(math.e, app.level) + b, 2)
#     basicTimerDelay = app.SETTING["TIMER_DELAY"]
#     app.timerDelay = int(basicTimerDelay * alpha)

# feature: difficulty, generating random pieces
def generateRandomPiece(app, threshold=0.95):
    heightIdxs = getBoardHeightIdxs(app)
    for i in range(app.cols):
        if heightIdxs[i] > 0:
            r = random.random()
            if r > threshold:
                blkRow = heightIdxs[i] - 1
                app.board[blkRow][i] = 'black'

def getBoardHeightIdxs(app):
    heightIdxs = [0] * app.cols
    for col in range(app.cols):
        heightIdxs[col] = getHeightIdxByCol(app, col)
    return heightIdxs

def getHeightIdxByCol(app, col):
    for i in range(app.rows):
        if app.board[i][col] != app.emptyColor:
            return i
    return 0

# feature: pause game (but not pause parent app) by pressing 'p'
def toggleGamePause(app):
    app.gamePaused = not app.gamePaused


# draw views
def redrawAll(app, canvas):
    # draw background
    canvas.create_rectangle(0, 0, app.width, app.height, fill="orange", width=0)
    
    # draw board
    drawBoard(app, canvas)
    
    # draw status board
    drawStatusBoard(app, canvas)
    
    # draw falling piece
    drawFallingPiece(app, canvas)
    
    # draw game over
    drawGameOver(app, canvas)
    
    # draw pause
    drawGamePause(app, canvas)

def drawCell(app, canvas, row, col, fill):
    left = col * app.cellSize + app.margin
    top = row * app.cellSize + app.margin
    right = left + app.cellSize
    bottom = top + app.cellSize
    width = app.SETTING["CELL_WIDTH"]
    canvas.create_rectangle(left, top, right, bottom, fill=fill, width=width)

def drawBoard(app, canvas):
    # draw cells
    for i in range(app.rows):
        for j in range(app.cols):
            drawCell(app, canvas, i, j, app.board[i][j])

def drawFallingPiece(app, canvas):
    for i in range(app.fpRowBlks):
        for j in range(app.fpColBlks):
            if app.fallingPiece[i][j]:
                row = app.fpRowIdx + i
                col = app.fpColIdx + j
                fill = app.tetrisPieceColors[app.randomIndex]
                drawCell(app, canvas, row, col, fill)

def drawStatusBoard(app, canvas):
    # upper left: level
    drawLevel(app, canvas)
    # upper middle: score
    drawScore(app, canvas)
    # bottom left
    drawBonusMode(app, canvas)

def drawLevel(app, canvas):
    x = app.margin
    y = app.margin / 2
    txt = '%s: %d' % (app.MESSAGE["LEVEL"], app.level)
    font = 'Arial %d bold' % (app.margin / 2)
    canvas.create_text(x, y, text=txt, font=font, fill='blue')

def drawScore(app, canvas):
    x = app.width / 2
    y = app.margin / 2
    txt = '%s: %d' % (app.MESSAGE["SCORE"], app.score)
    font = 'Arial %d bold' % (app.margin / 2)
    canvas.create_text(x, y, text=txt, font=font, fill='blue')

def drawBonusMode(app, canvas):
    if app.isBonusMode:
        x = app.margin
        y = app.height - app.margin / 2
        status = app.MESSAGE["ON"] if app.isBonusMode else app.MESSAGE["OFF"]
        txt = '%s: %s' % (app.MESSAGE["BONUS_MODE"], status)
        font = 'Arial %d bold' % (app.margin / 2)
        canvas.create_text(x, y, text=txt, font=font, fill='red')

def drawGameOver(app, canvas):
    if app.isGameOver:
        left = app.margin
        top = app.margin + app.cellSize * 2
        right = app.margin + app.cellSize * app.cols
        bottom = app.margin + app.cellSize * 4
        canvas.create_rectangle(left, top, right, bottom, fill='black')
        
        x = app.width / 2
        y = app.margin + app.cellSize * 3
        txt = app.MESSAGE["GAME_OVER"]
        font = 'Arial %d bold' % app.cellSize
        canvas.create_text(x, y, text=txt, font=font, fill='yellow')

def drawGamePause(app, canvas):
    if app.gamePaused:
        left = app.margin
        top = app.margin + app.cellSize * 2
        right = app.margin + app.cellSize * app.cols
        bottom = app.margin + app.cellSize * 4
        canvas.create_rectangle(left, top, right, bottom, fill='white')
        
        x = app.width / 2
        y = app.margin + app.cellSize * 3
        txt = app.MESSAGE["GAME_PAUSE"]
        font = 'Arial %d bold' % app.cellSize
        canvas.create_text(x, y, text=txt, font=font, fill='red')

#################################################
# main
#################################################

def main():
    cs112_f19_week7_linter.lint()
    playTetris()

if __name__ == '__main__':
    main()
