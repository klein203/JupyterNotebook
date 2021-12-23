# betterDiceThrowing.py

# Here we improve on diceThrowing.py by realizing that we can
# compute the odds for all the totals at once, rather than
# repeating our trials for each possible total.

import random

def rollDie(sides):
    return random.randint(1,sides)

def rollDice(dice, sides):
    dieTotal = 0
    for roll in range(dice):
        die = rollDie(sides)
        dieTotal += die
    return dieTotal

def diceOdds(dice, sides):
    trials = 1000*100
    maxTotal = dice*sides
    successes = [0]*(maxTotal+1)
    for trial in range(trials):
        dieTotal = rollDice(dice, sides)
        successes[dieTotal] += 1
    odds = [1.0*count/trials for count in successes]
    return odds

def printAllDiceOdds(dice, sides):
    odds = diceOdds(dice, sides)
    for total in range(dice,dice*sides+1):
        print(total, "%6.2f" % (100*odds[total]))

printAllDiceOdds(3,3)