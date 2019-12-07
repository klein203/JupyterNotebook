#################################################
# hw11.py
#
# Your name:
# Your andrew id:
#
# Your hw11 partner's name:
# Your hw11 partner's andrew id:
#
#################################################

import cs112_f19_week11_linter
import math, copy
import os

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

def confirmPolicies():
    # Replace each 42 with True or False according to the course policies.
    # If you are unsure, testConfirmPolicies() below contains the answers.
    # This is just to be sure you understand those policies!
    # We very much encourage you to collaborate, but we also want
    # you to do it right.  Be sure both of you are working closely together,
    # and both of you are contributing and learning the material well.
    # Have fun!!!!! 
    return  {
    'I can work solo on hw11': True,
    'I can work with one partner on hw11': True,
    ("I must list my hw11 partner's name and andrewId at the top" +
     "of my hw11.py file that I submit"): True,
    'I can switch hw11 partners and then work with a new partner': False,
    'My hw11 partner must be in 112 this semester': True,
    'My hw11 partner must be in the same lecture or section as me': False,
    "I can look at my hw11 partner's code": True,
    "I can copy some of hw11 partner's code": False,
    "I can help my hw11 partner debug their code": True,
    "I can electronically transfer some of my code to my hw11 partner": False,
    ("I can tell my hw11 partner line-by-line, character-by-character " +
     "what to type so their code is nearly-identical to mine."): False,
    }

def findLargestFile(path):
    def findLargestFileWrapper(method):
        import functools
        top = {"path": "",
               "size": 0}
        @functools.wraps(method)
        def m(*args, **kwargs):
            ret = method(*args)
            
            if ret != None and ret > top["size"]:
                top["path"] = args[0]
                top["size"] = ret
            
            return top["path"]
        
        return m
    
    @findLargestFileWrapper
    def traversePath(path):
        if os.path.isfile(path):
            return os.path.getsize(path)
        else:
            for filename in os.listdir(path):
                traversePath(path + '/' + filename)
            return None
    
    return traversePath(path)

def evalPrefixNotation(L):
    def evalPrefixNotationHelper(L):
        if L == [ ]:
            return None
        else:
            operator = L.pop(0)
            if str(operator).isdigit():
                return operator
            elif operator in ['+', '-', '*']:
                s = "(%s%s%s)" % (evalPrefixNotationHelper(L), operator, evalPrefixNotationHelper(L))
                return eval(s)
            else:
                raise Exception('Unknown operator: ' + operator)
    
    return evalPrefixNotationHelper(L)

def solveABC(constraints, aPosition):
    from backtracking import BacktrackingPuzzleSolver, State
    
    class ABCPuzzleSolver(BacktrackingPuzzleSolver):
        def __init__(self, sCharacter, sPosition, constraints):
            self.n = 5
            self.startArgs = (sCharacter, sPosition, constraints) # for printReport
            self.startState = ABCState([sCharacter], [sPosition])
            self.constraints = self.initConstraints(constraints)

        def initConstraints(self, constraints):
            con = dict()
            if len(constraints) != 24:
                raise Exception('Constraints should be a 24 characters length string')

            for i in range(0, 24):
                ch = constraints[i]
                if i in [0, 12]:
                    con[ch] = self._initConstraints('DIAG_BACKSLASH')
                elif i in [6, 18]:
                    con[ch] = self._initConstraints('DIAG_SLASH')
                elif i < 6:
                    con[ch] = self._initConstraints('COL', col=i-1)
                elif i < 12:
                    con[ch] = self._initConstraints('ROW', row=i-7)
                elif i < 18:
                    con[ch] = self._initConstraints('COL', col=17-i)
                else: # i < 24
                    con[ch] = self._initConstraints('ROW', row=23-i)

            return con

        def _initConstraints(self, constraintType, row=None, col=None):
            if constraintType == 'ROW':
                return set([(row, i) for i in range(0, self.n)])
            elif constraintType == 'COL':
                return set([(i, col) for i in range(0, self.n)])
            elif constraintType == 'DIAG_BACKSLASH':
                return set([(i, i) for i in range(0, self.n)])
            elif constraintType == 'DIAG_SLASH':
                return set([(i, self.n - 1 - i) for i in range(0, self.n)])
            else:
                raise Exception('Undefined constraints type')

        def constraintMap(self, ch):
            return self.constraints[ch]

        def isSolutionState(self, state):
            if len(state.positions) < self.n ** 2:
                return False

            # check 'Y'
            character = state.characters[-1]
            position = state.positions[-1]
            return (position in self.constraintMap(character)) and (position not in state.positions[:-1])

        def getLegalMoves(self, state):
            # try to move to the adjacent cells (rows, cols or diagonals
            position = state.positions[-1]
            return self.adjacentCells(position)

        def adjacentCells(self, position):
            (row, col) = position
            delta = [-1, 0, +1]
            rows = [row + d for d in delta if row + d >= 0 and row + d < self.n]
            cols = [col + d for d in delta if col + d >= 0 and col + d < self.n]
            return [(r, c) for r in rows for c in cols if not (r == row and c == col)]

        def doMove(self, state, move):
            curCharacter = state.characters[-1]
            nextCharacter = chr(ord(curCharacter) + 1)

            newCharacters = state.characters + [nextCharacter]
            newPositions = state.positions + [move]
            return ABCState(newCharacters, newPositions)

        def stateSatisfiesConstraints(self, state):
            character = state.characters[-1]
            position = state.positions[-1]
            return (position in self.constraintMap(character)) and (position not in state.positions[:-1])

    class ABCState(State):
        def __init__(self, characters, positions):
            self.n = 5
            self.characters = characters
            self.positions = positions

        def __repr__(self):
            return '\n'.join([' '.join(row) for row in self.as2DList()])
        
        def as2DList(self):
            board = [ (['-'] * self.n) for row in range(self.n) ]
            for i in range(0, len(self.positions)):
                row, col = self.positions[i]
                board[row][col] = self.characters[i]
            return board
    
    (_, state) = ABCPuzzleSolver('A', aPosition, constraints).solve(checkConstraints=True, printReport=False)
    if state == None:
        return None
    else:
        return state.as2DList()

def flatten(L):
    def flattenHelper(L):
        if type(L) == list:
            if L == [ ]:
                return [ ]
            if type(L[0]) == list:
                return flattenHelper(L[0] + []) + flattenHelper(L[1:] + [])
            else:
                return [L[0]] + flattenHelper(L[1:] + [])
        else:
            return L
    
    return flattenHelper(L)

################################################
# ignore_rest:  place all your graphics and tests below here!
################################################

from cmu_112_graphics import *
from tkinter import *

class FreddyFractalViewer(App):
    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height/2,
                           text='<insert FreddyFractalViewer here>',
                           font='Arial 20 bold')

def runFreddyFractalViewer():
    FreddyFractalViewer(width=400, height=400)

#################################################
# Test Functions
#################################################

def testConfirmPolicies():
    print('Testing confirmPolicies()...', end='')
    truePolicies = [ 
        'I can work solo on hw11',
        'I can work with one partner on hw11',
        ("I must list my hw11 partner's name and andrewId at the top" +
         "of my hw11.py file that I submit"),
        'My hw11 partner must be in 112 this semester',
        "I can look at my hw11 partner's code",
        "I can help my hw11 partner debug their code",
    ]
    falsePolicies = [
        'I can switch hw11 partners and then work with a new partner',
        'My hw11 partner must be in the same lecture or section as me',
        "I can copy some of hw11 partner's code",
        "I can electronically transfer some of my code to my hw11 partner",
        ("I can tell my hw11 partner line-by-line, character-by-character " +
         "what to type so their code is nearly-identical to mine."),
    ]
    policies = confirmPolicies()
    # True policies:
    for policy in truePolicies:
        assert(policies[policy] == True)
    # False policies (the opposite of these are actually policies)
    for policy in falsePolicies:
        assert(policies[policy] == False)
    print('Passed!')

def testFindLargestFile():
    print('Testing findLargestFile()...', end='')
    assert(findLargestFile('sampleFiles/folderA') ==
                           'sampleFiles/folderA/folderC/giftwrap.txt')
    assert(findLargestFile('sampleFiles/folderB') ==
                           'sampleFiles/folderB/folderH/driving.txt')
    assert(findLargestFile('sampleFiles/folderB/folderF') == '')
    print('Passed!')

def testEvalPrefixNotation():
    print('Testing evalPrefixNotation()...', end='')
    assert(evalPrefixNotation([42]) == 42)
    assert(evalPrefixNotation(['+', 3, 4]) == 7)
    assert(evalPrefixNotation(['-', 3, 4]) == -1)
    assert(evalPrefixNotation(['-', 4, 3]) == 1)
    assert(evalPrefixNotation(['+', 3, '*', 4, 5]) == 23)
    assert(evalPrefixNotation(['+', '*', 2, 3, '*', 4, 5]) == 26)
    assert(evalPrefixNotation(['*', '+', 2, 3, '+', 4, 5]) == 45)
    assert(evalPrefixNotation(['*', '+', 2, '*', 3, '-', 8, 7,
                               '+', '*', 2, 2, 5]) == 45)
    raisedAnError = False
    try:
        evalPrefixNotation(['^', 2, 3])
    except:
        raisedAnError = True
    assert(raisedAnError == True)
    print('Passed.')

def testSolveABC():
    print('Testing solveABC()...', end='')
    constraints = 'CHJXBOVLFNURGPEKWTSQDYMI'
    aLocation = (0,4)
    board = solveABC(constraints, aLocation)
    solution = [['I', 'J', 'K', 'L', 'A'],
                ['H', 'G', 'F', 'B', 'M'],
                ['T', 'Y', 'C', 'E', 'N'],
                ['U', 'S', 'X', 'D', 'O'],
                ['V', 'W', 'R', 'Q', 'P']
               ]
    assert(board == solution)

    constraints = 'TXYNFEJOQCHIMBDSUWPGKLRV'
    aLocation = (2,4)
    board = solveABC(constraints, aLocation)
    solution = [['V', 'U', 'S', 'O', 'P'],
                ['W', 'T', 'N', 'R', 'Q'],
                ['X', 'L', 'M', 'C', 'A'],
                ['K', 'Y', 'H', 'D', 'B'],
                ['J', 'I', 'G', 'F', 'E'],
               ]
    assert(board == solution)

    constraints = 'TXYNFEJOQCHIMBDSUPWGKLRV' # swapped P and W
    aLocation = (2,4)
    board = solveABC(constraints, aLocation)
    solution = None
    assert(board == solution)
    print('Passed!')

def testFlatten():
    print('Testing bonus flatten()...', end='')
    assert(flatten([1,[2]]) == [1,2])
    assert(flatten([1,2,[3,[4,5],6],7]) == [1,2,3,4,5,6,7])
    assert(flatten(['wow', [2,[[]]], [True]]) == ['wow', 2, True])
    assert(flatten([]) == [])
    assert(flatten([[]]) == [])
    assert(flatten(3) == 3)
    print('Passed!')

#################################################
# testAll and main
#################################################

def testAll():
    testConfirmPolicies()
    testFindLargestFile()
    testEvalPrefixNotation()
    testSolveABC()
    runFreddyFractalViewer()
    testFlatten() # bonus

def main():
#     cs112_f19_week11_linter.lint()
    testAll()

if (__name__ == '__main__'):
    main()
