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
    'I can work solo on hw11': 42,
    'I can work with one partner on hw11': 42,
    ("I must list my hw11 partner's name and andrewId at the top" +
     "of my hw11.py file that I submit"): 42,
    'I can switch hw11 partners and then work with a new partner': 42,
    'My hw11 partner must be in 112 this semester': 42,
    'My hw11 partner must be in the same lecture or section as me': 42,
    "I can look at my hw11 partner's code": 42,
    "I can copy some of hw11 partner's code": 42,
    "I can help my hw11 partner debug their code": 42,
    "I can electronically transfer some of my code to my hw11 partner": 42,
    ("I can tell my hw11 partner line-by-line, character-by-character " +
     "what to type so their code is nearly-identical to mine."): 42,
    }

def findLargestFile(path):
    return 42

def evalPrefixNotation(L):
    return 42

def solveABC(constraints, aPosition):
    return 42

def flatten(L):
    # This is bonus!
    return 42

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
    cs112_f19_week11_linter.lint()
    testAll()

if (__name__ == '__main__'):
    main()
