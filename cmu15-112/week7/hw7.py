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
    rows, cols, cellSize, margin = 15, 10, 20, 25
#     rows, cols, cellSize, margin = 15, 10, 12, 2
    return (rows, cols, cellSize, margin)

def playTetris():
    (rows, cols, cellSize, margin) = gameDimensions()
    width, height = cols * cellSize + margin * 2, rows * cellSize + margin * 2
#     runApp(width=width, height=height)
    runApp(width=width, height=height, x=500, y=100)

# app start
def appStarted(app):
    app.timerDelay = 200
    app.isGameOver = False
    app.score = 0
    
    (app.rows, app.cols, app.cellSize, app.margin) = gameDimensions()
    # init cells
    app.emptyColor = "blue"
    app.board = [[app.emptyColor] * app.cols for i in range(app.rows)]
    
    # Seven "standard" pieces (tetrominoes)
    iPiece = [
        [  True,  True,  True,  True ]
    ]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    app.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    app.tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", 
                             "green", "orange"]
    
    newFallingPiece(app)
    
    # board test
#     app.board[0][0] = "red" # top-left is red
#     app.board[0][app.cols-1] = "white" # top-right is white
#     app.board[app.rows-1][0] = "green" # bottom-left is green
#     app.board[app.rows-1][app.cols-1] = "gray" # bottom-right is gray

# event driven, controller
def keyPressed(app, event):
    if not app.isGameOver:
        if event.key == 'Down':
            moveFallingPiece(app, +1, 0)
        elif event.key == 'Left':
            moveFallingPiece(app, 0, -1)
        elif (event.key == 'Right'):
            moveFallingPiece(app, 0, +1)
        elif (event.key == 'Up'):
            rotateFallingPiece(app)
    
    if (event.key == 'r'):
        appStarted(app)

def timerFired(app):
    if not app.isGameOver:
        if not moveFallingPiece(app, +1, 0):
            placeFallingPiece(app)
            removeFullRows(app)
            newFallingPiece(app)
            if not fallingPieceIsLegal(app):
                # game over
                app.isGameOver = True

# top-down functions to support controller
def newFallingPiece(app):
    app.randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
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

def rotateFallingPiece(app, mode="counterclockwise"):
    # backup falling piece info
    fp = app.fallingPiece
    fpRowIdx = app.fpRowIdx
    fpColIdx = app.fpColIdx
    fpRowBlks = app.fpRowBlks
    fpColBlks = app.fpColBlks
    
    # transpose
    app.fallingPiece = [[row[i] for row in fp] for i in range(fpColBlks)]
    # upside down
    if mode == "counterclockwise":
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
    rmLines = [row for row in app.board if not app.emptyColor in row]
    
    # remove these lines from board
    [app.board.remove(l) for l in rmLines]
    
    # generate emptyColor lines with the same shape of lines removed
    newLines = [[app.emptyColor] * app.cols for i in range(len(rmLines))]
    
    # stack
    app.board.insert(0, newLines)

    # scoring
    app.score += len(rmLines)


# draw views
def redrawAll(app, canvas):
    # draw background
    canvas.create_rectangle(0, 0, app.width, app.height, fill="orange", width=0)
    
    # draw board
    drawBoard(app, canvas)
    
    # draw score
    drawScore(app, canvas)
    
    # draw falling piece
    drawFallingPiece(app, canvas)
    
    # draw game over
    drawGameOver(app, canvas)

def drawCell(app, canvas, row, col, fill):
    left = col * app.cellSize + app.margin
    top = row * app.cellSize + app.margin
    right = left + app.cellSize
    bottom = top + app.cellSize
    canvas.create_rectangle(left, top, right, bottom, fill=fill, width=3)

def drawBoard(app, canvas):
    # draw cells
    for i in range(app.rows):
        for j in range(app.cols):
            drawCell(app, canvas, i, j, app.board[i][j])

def drawScore(app, canvas):
    x = app.width / 2
    y = app.margin / 2
    txt = 'Score: %d' % app.score
    font = 'Arial %d bold' % (app.margin / 2)
    canvas.create_text(x, y, text=txt, font=font, fill='blue')

def drawFallingPiece(app, canvas):
    for i in range(app.fpRowBlks):
        for j in range(app.fpColBlks):
            if app.fallingPiece[i][j]:
                row = app.fpRowIdx + i
                col = app.fpColIdx + j
                fill = app.tetrisPieceColors[app.randomIndex]
                drawCell(app, canvas, row, col, fill)

def drawGameOver(app, canvas):
    if app.isGameOver:
        left = app.margin
        top = app.margin + app.cellSize * 2
        right = app.margin + app.cellSize * app.cols
        bottom = app.margin + app.cellSize * 4
        canvas.create_rectangle(left, top, right, bottom, fill='black')
        
        x = app.width / 2
        y = app.margin + app.cellSize * 3
        font = 'Arial %d bold' % app.cellSize
        canvas.create_text(x, y, text='Game Over !', font=font, fill='yellow')

#################################################
# main
#################################################

def main():
    cs112_f19_week7_linter.lint()
    playTetris()

if __name__ == '__main__':
    main()
