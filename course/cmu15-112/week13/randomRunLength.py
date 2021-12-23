# randomRunLength.py

# Q: We will say that a "run" of random numbers continues
#    until you pick one that is smaller than the previous one.
#    That last number ends the run, and is also counted in the run
#    (so the shortest possible run length is 2).
#    With this definition, what is the expected length of
#    a run of random numbers?

# A: See code below.

import random

def randomRunLength():
    val = random.random()
    runLength = 1
    while True:
        nextVal = random.random()
        runLength += 1
        if (nextVal < val): return runLength
        val = nextVal

# Or, if you prefer...
def randomRunLength():
    vals = [ random.random(), random.random() ]
    while (vals[-2] < vals[-1]): vals.append(random.random())
    return (len(vals))

def averageRandomRunLength(trials):
    totalRunLength = 0
    for trial in range(trials):
        totalRunLength += randomRunLength()
    return totalRunLength / trials

for k in range(1,6):
    trials = 10**k
    print("10**%d trials --> %f" %
          (k, averageRandomRunLength(trials)))
