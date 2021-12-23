# diceThrowing.py

# For correct answers, try here:
# http://www.ogmiosproject.org/articles/stattables.html

import random

def rollDie(sides):
    return random.randint(1,sides)

def trialSucceeds(dice, sides, total):
    # run only ONE trial and return True on success.
    # one trial means:
    # roll 2 dice and succeed if their sum is total
    dieTotal = 0
    for roll in range(dice):
        die = rollDie(sides)
        dieTotal += die
    return (dieTotal == total)

def diceOdds(dice, sides, total, trials):
    successes = 0
    for trial in range(trials):
        if trialSucceeds(dice, sides, total) == True:
            successes += 1
    return 1.0 * successes / trials

def printAllDiceOdds(dice, sides):
    # print the label line
    print("Trials", end="")
    for label in range(dice, dice*sides+1):
        print("%7d" % label, end="")
    print()
    # now compute and print results for different-sized trials
    for k in range(1,5):
        trials = 10**k
        print("%7d" % trials, end="")
        for total in range(dice, dice*sides+1):
            print("%6.2f " % (100*diceOdds(dice, sides, total, trials)),
                  end="")
        print()

printAllDiceOdds(3,3)
