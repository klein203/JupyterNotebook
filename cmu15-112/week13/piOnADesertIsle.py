# piOnADesertIsle.py

import random, math

def randomFloatInRange(lo, hi):
    return lo + (hi - lo)*random.random()

def inUnitCircle(x,y):
    return (x**2 + y**2 <= 1)

def findPi(throws):
    throwsInCircle = 0
    for throw in range(throws):
        x = randomFloatInRange(-1, +1)
        y = randomFloatInRange(-1, +1)
        if inUnitCircle(x,y):
            throwsInCircle += 1
    return 4.0 * throwsInCircle / throws

for k in range(1,7):
    throws = 10**k
    piGuess = findPi(throws)
    accuracy = 100 * (1 - abs(piGuess - math.pi) / math.pi)
    print("10**%d throws --> %f (accuracy: %f%%)" %
          (k, piGuess, accuracy))
    