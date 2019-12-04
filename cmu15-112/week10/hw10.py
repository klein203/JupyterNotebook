#################################################
# hw10.py
#
# Your name:
# Your andrew id:
#################################################

import cs112_f19_week10_linter
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

def alternatingSum(L):
    def alternatingSumHelper(L, depth):
        if L == [ ]:
            return 0
        else:
            op = 1
            if depth % 2 == 0:
                op = -1
            return alternatingSumHelper(L[:-1], depth - 1) + op * L[-1]

    return alternatingSumHelper(L, len(L))

def onlyEvenDigits(L):
    def onlyEvenDigit(digit):
        if digit < 0:
            return onlyEvenDigit(abs(digit))
        elif digit % 2 == 1:
            return onlyEvenDigit(digit // 10)
        elif digit < 10:
            return digit
        else:
            return digit % 10 + onlyEvenDigit(digit // 10) * 10
    
    if L == [ ]:
        return [ ]
    else:
        return [onlyEvenDigit(L[0])] + onlyEvenDigits(L[1:])
    
def powersOf3ToN(n):
    def powersOf3ToNHelper(n, a=3, b=0):
        import math
        if a ** b > n:
            return [ ]
        else:
            return [a ** b] + powersOf3ToNHelper(n, a, b + 1)
    
    return powersOf3ToNHelper(n)

def binarySearchValues(L, item):
    def binarySearchValuesHelper(L, lo, hi, item):
        mid = (lo + hi) // 2
        if lo > hi:
            return [ ]
        elif L[mid] == item:
            return [(mid, L[mid])]
        elif L[mid] < item:
            return [(mid, L[mid])] + binarySearchValuesHelper(L, mid + 1, hi, item)
        else:
            return [(mid, L[mid])] + binarySearchValuesHelper(L, lo, mid - 1, item)

    return binarySearchValuesHelper(L, 0, len(L) - 1, item)

def secondLargest(L):
    def secondLargestHelper(L):
        if L == [ ]:
            return 

    if len(L) <= 2:
        return None
    else:
        return secondLargestHelper(L)

#################################################
# Test Functions
#################################################

def testAlternatingSum():
    print('Testing alternatingSum()...', end='')
    assert(alternatingSum([1,2,3,4,5]) == 1-2+3-4+5)
    assert(alternatingSum([ ]) == 0)
    print('Passed!')

def testSecondLargest():
    print('Testing secondLargest()...', end='')
    assert(secondLargest([1,2,3,4,5]) == 4)
    assert(secondLargest([4,3]) == 3)
    assert(secondLargest([4,4,3]) == 4)
    assert(secondLargest([-3,-4]) == -4)
    assert(secondLargest([4]) == None)
    assert(secondLargest([ ]) == None)
    print('Passed!')

def testOnlyEvenDigits():
    print('Testing onlyEvenDigits()...', end='')
    assert(onlyEvenDigits([43, 23265, 17, 58344]) == [4, 226, 0, 844])
    assert(onlyEvenDigits([ ]) == [ ])
    print('Passed!')

def testPowersOf3ToN():
    print('Testing powersOf3ToN()...', end='')
    assert(powersOf3ToN(10.5) == [1, 3, 9])
    assert(powersOf3ToN(27) == [1, 3, 9, 27])
    assert(powersOf3ToN(26.999) == [1, 3, 9])
    assert(powersOf3ToN(-1) == [ ])
    print('Passed!')

def testBinarySearchValues():
    print('Testing binarySearchValues()...', end='')
    assert(binarySearchValues(['a', 'c', 'f', 'g', 'm', 'q'], 'c') ==
           [(2, 'f'), (0, 'a'), (1, 'c')])
    assert(binarySearchValues(['a', 'c', 'f', 'g', 'm', 'q'], 'n') ==
           [(2, 'f'), (4, 'm'), (5, 'q')])
    print('Passed!')

#################################################
# testAll and main
#################################################

def testAll():
    testAlternatingSum()
    testOnlyEvenDigits()
    testPowersOf3ToN()
    testBinarySearchValues()
    testSecondLargest()

def main():
#     cs112_f19_week10_linter.lint()
    testAll()

if (__name__ == '__main__'):
    main()
