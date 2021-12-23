# birthdayProblem.py

import random

def trialSucceeds(numberOfPeopleInRoom):
    # run only ONE trial and return True on success.
    # one trial means:
    # Put the given # of people in a room
    # and return true if any 2 share any birthday
    seenBirthdays = set()
    for person in range(numberOfPeopleInRoom):
        birthday = random.randint(1,365)
        if (birthday in seenBirthdays):
            return True
        seenBirthdays.add(birthday)
    return False

def birthdayOdds(numberOfPeopleInRoom, trials):
    successes = 0
    for trial in range(trials):
        if trialSucceeds(numberOfPeopleInRoom) == True:
            successes += 1
    return 1.0 * successes / trials

def solveBirthdayProblem(trials):
    for peopleInRoom in range(2,366):
        if (birthdayOdds(peopleInRoom, trials) >= 0.5):
            return peopleInRoom

for k in range(1,5):
    trials = 10**k
    print("10**%d trials --> %f" %
          (k, solveBirthdayProblem(trials)))