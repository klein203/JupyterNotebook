#################################################
# hw8.py
#
# Your name:
# Your andrew id:
#################################################

import cs112_f19_week8_linter
import math, copy

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

def getPairSum(lst, target):
    import copy
    pair = [0, 0]
    for i in range(len(lst)):
        c = copy.deepcopy(lst)
        pair[0] = lst[i]
        pair[1] = target - pair[0]
        
        c.remove(pair[0])
        if pair[1] in c:
            return tuple(pair)

    return None

def containsPythagoreanTriple(lst):
    l = [x ** 2 for x in lst]
    l.sort()
    for i in range(len(l)):
        for j in range(i + 1, len(l) - 1):
            if (l[i] + l[j]) in l[j + 1:len(l)]:
                return True
    return False

def movieAwards(oscarResults):
    winners = set()
    winnerCount = dict()

    for ele in oscarResults:
        (_, winner) = ele
        if winner not in winners:
            winners.add(winner)
            winnerCount[winner] = 0
        
        winnerCount[winner] += 1
    return winnerCount

def friendsOfFriends(d):
    friendsOfFriends = dict()
    for person in d:
        friendsOfPerson = d[person]
        fof = set()
        for f in friendsOfPerson:
            [fof.add(x) for x in d[f] if x != person and x not in friendsOfPerson]
        
        friendsOfFriends[person] = fof

    return friendsOfFriends
    
    
#################################################
# Test Functions
#################################################

# ADD YOUR OWN TEST FUNCTIONS!!!
def testGetPairSum():
    print("Testing getPairSum()...", end="")
    assert(getPairSum([1], 1) == None)
    assert(getPairSum([5, 2], 7) in [ (5, 2), (2, 5) ])
    assert(getPairSum([10, -1, 1, -8, 3, 1], 2) in [ (10, -8), (-8, 10), (-1, 3), (3, -1), (1, 1) ])
    assert(getPairSum([10, -1, 1, -8, 3, 1], 10) == None)
    print("Passed!")

def testContainsPythagoreanTriple():
    print("Testing containsPythagoreanTriple()...", end="")
    assert(containsPythagoreanTriple([1, 3, 6, 2, 5, 1, 4]) == True)
    assert(containsPythagoreanTriple([1, 3, 6, 2, 1, 4]) == False)
    assert(containsPythagoreanTriple([4, 3, 5]) == True)
    assert(containsPythagoreanTriple([1]) == False)
    print("Passed!")

def testMovieAwards():
    print("Testing movieAwards()...", end="")
    assert(movieAwards({
        ("Best Picture", "Green Book"), 
        ("Best Actor", "Bohemian Rhapsody"),
        ("Best Actress", "The Favourite"),
        ("Film Editing", "Bohemian Rhapsody"),
        ("Best Original Score", "Black Panther"),
        ("Costume Design", "Black Panther"),
        ("Sound Editing", "Bohemian Rhapsody"),
        ("Best Director", "Roma")
    }) == {
        "Black Panther" : 2,
        "Bohemian Rhapsody" : 3,
        "The Favourite" : 1,
        "Green Book" : 1,
        "Roma" : 1
    })
    print("Passed!")

def testFriendsOfFriends():
    print("Testing friendsOfFriends()...", end="")
    d = { }
    d["jon"] = set(["arya", "tyrion"])
    d["tyrion"] = set(["jon", "jaime", "pod"])
    d["arya"] = set(["jon"])
    d["jaime"] = set(["tyrion", "brienne"])
    d["brienne"] = set(["jaime", "pod"])
    d["pod"] = set(["tyrion", "brienne", "jaime"])
    d["ramsay"] = set()
    assert(friendsOfFriends(d) == {
        'tyrion': {'arya', 'brienne'}, 
        'pod': {'jon'}, 
        'brienne': {'tyrion'}, 
        'arya': {'tyrion'}, 
        'jon': {'pod', 'jaime'}, 
        'jaime': {'pod', 'jon'}, 
        'ramsay': set()
    })
    print("Passed!")

#################################################
# testAll and main
#################################################

def testAll():
    testGetPairSum()
    testContainsPythagoreanTriple()
    testMovieAwards()
    testFriendsOfFriends()

def main():
    cs112_f19_week8_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
