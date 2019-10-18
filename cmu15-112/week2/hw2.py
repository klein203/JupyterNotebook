#################################################
# hw2.py
#
# Your name:
# Your andrew id:
#################################################

import cs112_f19_week2_linter
import math
from tkinter import *
import random

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

def integral(f, a, b, N):
    delta = (b - a) / N
    sum = 0
    for i in range(N):
        x_i = a + delta * i
        x_i_plus_1 = a + delta * (i + 1)
        sum += (f(x_i) + f(x_i_plus_1)) / 2 * delta
    return sum

def nthSmithNumber(n):
    def isPrime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        maxFactor = round(n ** 0.5)
        for factor in range(3, maxFactor + 1, 2):
            if n % factor == 0:
                return False
        return True
    
    def nPrime(n):
        factors = []
        for i in range(2, n + 1):
            if isPrime(i):
                factors.append(i)
        return factors
    
    def isSmithNumber(n):
        # calculate all factors less than n + 1
        factors = nPrime(n)
        
        # n should not be factor itself
        if len(factors) == 0 or n in factors:
            return False
        
        # calculate all digits of n
        nNum = 0
        for c in str(n):
            nNum += int(c)
        
        magicNums = []
        while True:
            if n in factors:
                magicNums.append(int(n))
                break
            else:
                for f in factors:
                    if n % f == 0:
                        magicNums.append(f)
                        n /= f
                        break
        
        # calculate all digits of magic numbers
        magicNum = 0
        for m in magicNums:
            for c in str(m):
                magicNum += int(c)
    
        return magicNum == nNum
    
    found = 0
    guess = -1
    while (found <= n):
        guess += 1
        if (isSmithNumber(guess)):
            found += 1
    return guess

def drawPattern1(points, canvas, width, height):
    def drawSinglePattern(canvas, x, y, width, height):
        # create_line(x1, y1, x2, y2) draws a line from (x1, y1) to (x2, y2)
        canvas.create_line(x, y, x + width, y + height)
        canvas.create_line(x + width, y, x, y + height)
    
    def drawPattern(points, canvas, width, height):
        if points < 2:
            return

        nWidth = width / (points - 1)
        nHeight = height / (points - 1)

        for row in range(points):
            for col in range(points):
                x = col * nWidth
                y = row * nHeight
                drawSinglePattern(canvas, x, y, nWidth, nHeight)
    
    drawPattern(points, canvas, width, height)

def drawPattern2(points, canvas, width, height):
    def drawAxis(canvas, width, height):
        canvas.create_line(width / 2, 0, width / 2, height)
        canvas.create_line(0, height / 2, width, height / 2)
    
    def drawSinglePattern(canvas, xAxis, yAxis, width, height):
        canvas.create_line(xAxis, height / 2, width / 2, yAxis)
        canvas.create_line(xAxis, height / 2, width / 2, height - yAxis)
        canvas.create_line(width - xAxis, height / 2, width / 2, yAxis)
        canvas.create_line(width - xAxis, height / 2, width / 2, height - yAxis)

    def drawPattern(points, canvas, width, height):
        if points < 2:
            return

        nWidth = width / (points - 1) / 2
        nHeight = height / (points - 1) / 2

        for i in range(1, points):
            xAxis = i * nWidth
            yAxis = height / 2 - i * nHeight
            drawSinglePattern(canvas, xAxis, yAxis, width, height)

    drawAxis(canvas, width, height)
    drawPattern(points, canvas, width, height)

def drawPattern3(points, canvas, width, height):
    def drawSingleSquarePattern(canvas, x, y, width, height):
        canvas.create_line(x, y, x + width, y)
        canvas.create_line(x + width, y, x + width, y + height)
        canvas.create_line(x + width, y + height, x, y + height)
        canvas.create_line(x, y + height, x, y)

    def drawSingleTrianglePattern(canvas, x, y, width, height):
        canvas.create_line(x, y, x + width, y)
        canvas.create_line(x + width, y, x + width / 2, y + height)
        canvas.create_line(x + width / 2, y + height, x, y)

    def drawPattern(points, canvas, width, height):
        if points < 2:
            return

        nWidth = width / (points - 1)
        nHeight = height / (points - 1)

        for row in range(points):
            for col in range(points):
                x = col * nWidth
                y = row * nHeight
                if row % 2 == 0:
                    drawSingleSquarePattern(canvas, x, y, nWidth, nHeight)
                else:
                    drawSingleTrianglePattern(canvas, x, y, nWidth, nHeight)

    drawPattern(points, canvas, width, height)

def drawPattern4(canvas, width, height):
    pass

def playPig():
    import random
    
    class Player(object):
        def __init__(self, name):
            self.name = name
            self.score = 0
        
        def hold(self, s):
            self.score += s
        
        def dice(self, minDice=1, maxDice=6):
            return random.randint(minDice, maxDice)
    
    class PigGame(object):
        def __init__(self, name):
            self.BLOCK_DICE = 1
            self.WINNING_SCORE = 20
            
            self.name = name
            self.players = []
            self.curPlayerIdx = 0
        
        def addPlayer(self, player):
            self.players.append(player)
        
        def nextPlayer(self):
            self.curPlayerIdx = (self.curPlayerIdx + 1) % len(self.players)
            return self.curPlayer
        
        @property
        def curPlayer(self):
            return self.players[self.curPlayerIdx]
        
        def winGame(self):
            return self.curPlayer.score >= self.WINNING_SCORE
        
        def play(self):
            nPlayers = int(input("Enter number of players:"))
            for i in range(1, nPlayers + 1):
                name = input("Enter name of player #%d:" % i)
                player = Player(name)
                self.addPlayer(player)

            print("Game start!")
            while True:
                print("Player %s\'s turn:" % (self.curPlayer.name))
                
                turnScore = 0
                while True:
                    dice = self.curPlayer.dice()
                    print("Dice! %d" % dice)
                    if dice == self.BLOCK_DICE:
                        print("Ooooops..., you hit the block dice and lose all your scores this turn :(")
                        break
                        
                    turnScore += dice
                    print("Total score: %d, This turn: %d, last dice: %d" % (self.curPlayer.score, turnScore, dice))
                    
                    cmd = input("press <enter> to go on, press <\'hold\'> to hold this turn")
                    if cmd == 'hold':
                        self.curPlayer.hold(turnScore)
                        print("You hold the turn, save all scores this turn, total score: %d" % (self.curPlayer.score))
                        break
                    elif cmd == '':
                        continue
                    else:
                        print("Something wrong here~")
                        continue

                if self.winGame():
                    print("Congratulations! Player [%s] wins the game!" % (self.curPlayer.name))
                    break
                else:
                    self.nextPlayer()

            print("Game end!")
            
            
    game = PigGame('Pig Game')
    game.play()
        
        
#     linesEntered = 0
#     while (True):
#         response = input("Enter a string (or 'done' to quit): ")
#         if (response == "done"):
#             break
#         print("  You entered: ", response)
#         linesEntered += 1
#     print("Bye!")
#     return linesEntered

# linesEntered = readUntilDone()
# print("You entered", linesEntered, "lines (not counting 'done').")
#     print('Not yet implemented!')

#################################################
# Bonus/Optional functions for you to write
#################################################

def bonusCarrylessMultiply(x1, x2):
    return 42

def bonusPlay112(game):
    return 42

#################################################
# Test Functions
#################################################

def f1(x): return 42
def i1(x): return 42*x 
def f2(x): return 2*x  + 1
def i2(x): return x**2 + x
def f3(x): return 9*x**2
def i3(x): return 3*x**3
def f4(x): return math.cos(x)
def i4(x): return math.sin(x)
def testIntegral():
    print('Testing integral()...', end='')
    epsilon = 10**-4
    assert(almostEqual(integral(f1, -5, +5, 1), (i1(+5)-i1(-5)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f1, -5, +5, 10), (i1(+5)-i1(-5)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f2, 1, 2, 1), 4,
                      epsilon=epsilon))
    assert(almostEqual(integral(f2, 1, 2, 250), (i2(2)-i2(1)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f3, 4, 5, 250), (i3(5)-i3(4)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f4, 1, 2, 250), (i4(2)-i4(1)),
                      epsilon=epsilon))
    print("Passed!")

def testNthSmithNumber():
    print('Testing nthSmithNumber()... ', end='')
    assert(nthSmithNumber(0) == 4)
    assert(nthSmithNumber(1) == 22)
    assert(nthSmithNumber(2) == 27)
    assert(nthSmithNumber(3) == 58)
    assert(nthSmithNumber(4) == 85)
    assert(nthSmithNumber(5) == 94)
    print('Passed.')

def runDrawPattern1(points, width=300, height=300):
    root = Tk()
    root.resizable(width=False, height=False) # non-resizable
    canvas = Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    drawPattern1(points, canvas, width, height)
    root.mainloop()
    print("bye!")

def runDrawPattern2(points, width=300, height=300):
    root = Tk()
    root.resizable(width=False, height=False) # non-resizable
    canvas = Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    drawPattern2(points, canvas, width, height)
    root.mainloop()
    print("bye!")

def runDrawPattern3(points, width=300, height=300):
    root = Tk()
    root.resizable(width=False, height=False) # non-resizable
    canvas = Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    drawPattern3(points, canvas, width, height)
    root.mainloop()
    print("bye!")

def runDrawPattern4(width=300, height=300):
    root = Tk()
    root.resizable(width=False, height=False) # non-resizable
    canvas = Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    drawPattern4(canvas, width, height)
    root.mainloop()
    print("bye!")

def testDrawPatterns():
    print('** Note: You need to manually test drawPatterns()')
    print('Calling runDrawPattern1(5, 400, 400):')
    runDrawPattern1(5, 400, 400)
    print('Calling runDrawPattern1(10, 800, 400):')
    runDrawPattern1(10, 800, 400)
    print('Calling runDrawPattern2(5, 400, 400):')
    runDrawPattern2(5, 400, 400)
    print('runDrawPattern2(10, 800, 400):')
    runDrawPattern2(10, 800, 400)
    print('runDrawPattern3(5, 400, 400):')
    runDrawPattern3(5, 400, 400)
    print('runDrawPattern3(10, 800, 400)')
    runDrawPattern3(10, 800, 400)
    print('runDrawPattern4(600, 600)')
    runDrawPattern4(600, 600)

def testPlayPig():
    print('** Note: You need to manually test playPig()')

def testBonusCarrylessMultiply():
    print("Testing bonusCarrylessMultiply()...", end="")
    assert(bonusCarrylessMultiply(643, 59) == 417)
    assert(bonusCarrylessMultiply(6412, 387) == 807234)
    print("Passed!")

def testBonusPlay112():
    print("Testing bonusPlay112()... ", end="")
    assert(bonusPlay112( 5 ) == "88888: Unfinished!")
    assert(bonusPlay112( 521 ) == "81888: Unfinished!")
    assert(bonusPlay112( 52112 ) == "21888: Unfinished!")
    assert(bonusPlay112( 5211231 ) == "21188: Unfinished!")
    assert(bonusPlay112( 521123142 ) == "21128: Player 2 wins!")
    assert(bonusPlay112( 521123151 ) == "21181: Unfinished!")
    assert(bonusPlay112( 52112315142 ) == "21121: Player 1 wins!")
    assert(bonusPlay112( 523 ) == "88888: Player 1: move must be 1 or 2!")
    assert(bonusPlay112( 51223 ) == "28888: Player 2: move must be 1 or 2!")
    assert(bonusPlay112( 51211 ) == "28888: Player 2: occupied!")
    assert(bonusPlay112( 5122221 ) == "22888: Player 1: occupied!")
    assert(bonusPlay112( 51261 ) == "28888: Player 2: offboard!")
    assert(bonusPlay112( 51122324152 ) == "12212: Tie!")
    print("Passed!")

#################################################
# testAll and main
#################################################

def testAll():
    testIntegral()
    testNthSmithNumber()
    testDrawPatterns()
    testPlayPig()
    #testBonusCarrylessMultiply()
    #testBonusPlay112()

def main():
    cs112_f19_week2_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
