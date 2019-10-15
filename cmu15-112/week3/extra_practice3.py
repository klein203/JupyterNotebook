#################################################
# extra_practice3.py
#################################################

import cs112_f19_week3_linter
import math
from tkinter import *
import string

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
################################################

def vowelCount(s):
    return 42

def interleave(s1, s2):
    return 42

def longestCommonSubstring(s1, s2):
    return 42

def leastFrequentLetters(s):
    return 42

def sameChars(s1, s2):
    return 42

def areAnagrams(s1, s2):
    return 42

def replace(s1, s2, s3):
    return 42

def wordWrap(text, width):
    return 42

#################################################
# Test Functions
#################################################

def testVowelCount():
    print("Testing vowelCount()...", end="")
    assert(vowelCount("abcdefg") == 2)
    assert(vowelCount("ABCDEFG") == 2)
    assert(vowelCount("") == 0)
    assert(vowelCount("This is a test.  12345.") == 4)
    assert(vowelCount(string.ascii_lowercase) == 5)
    assert(vowelCount(string.ascii_lowercase*100) == 500)
    assert(vowelCount(string.ascii_uppercase) == 5)
    assert(vowelCount(string.punctuation) == 0)
    assert(vowelCount(string.whitespace) == 0)
    print("Passed!")

def testInterleave():
    print("Testing interleave()...", end="")
    assert(interleave("abcdefg", "abcdefg") == "aabbccddeeffgg")
    assert(interleave("abcde", "abcdefgh") == "aabbccddeefgh")
    assert(interleave("abcdefgh","abcde") == "aabbccddeefgh")
    assert(interleave("Smlksgeneg n a!", "a ie re gsadhm") ==
                      "Sam likes green eggs and ham!")
    assert(interleave("","") == "")
    print("Passed!")

def testLongestCommonSubstring():
    print("Testing longestCommonSubstring()...", end="")
    assert(longestCommonSubstring("abcdef", "abqrcdest") == "cde")
    assert(longestCommonSubstring("abcdef", "ghi") == "")
    assert(longestCommonSubstring("", "abqrcdest") == "")
    assert(longestCommonSubstring("abcdef", "") == "")
    assert(longestCommonSubstring("abcABC", "zzabZZAB") == "AB")
    print("Passed!")

def testLeastFrequentLetters():
    print("Testing leastFrequentLetters()...", end="")
    assert(leastFrequentLetters("abc def! GFE'cag!!!") == "bd")
    assert(leastFrequentLetters("abc def! GFE'cag!!!".lower()) == "bd")
    assert(leastFrequentLetters("abc def! GFE'cag!!!".upper()) == "bd")
    assert(leastFrequentLetters("") == "")
    assert(leastFrequentLetters(string.punctuation) == "")
    assert(leastFrequentLetters(string.whitespace) == "")
    assert(leastFrequentLetters(string.ascii_lowercase) ==
                                string.ascii_lowercase)
    assert(leastFrequentLetters(string.ascii_uppercase) ==
                                string.ascii_lowercase)
    noq = string.ascii_lowercase.replace('q','')
    nor = string.ascii_lowercase.replace('r','')
    nos = string.ascii_lowercase.replace('s','')
    assert(leastFrequentLetters(string.ascii_lowercase + noq) == "q")
    assert(leastFrequentLetters(nor + string.ascii_lowercase) == "r")
    assert(leastFrequentLetters(nos + nor + " aaa " + 5*string.ascii_lowercase)
                                == "rs")
    print("Passed!")

def testSameChars():
    print("Testing sameChars()...", end="")
    assert(sameChars("abcabcabc", "cba") == True)
    assert(sameChars("abcabcabc", "cbad") == False)
    assert(sameChars("abcabcabc", "cBa") == False)
    assert(sameChars(42,"The other parameter is not a string") == False)
    assert(sameChars("","") == True)
    print("Passed!")

def testAreAnagrams():
    print("Testing areAnagrams()...", end="")
    assert(areAnagrams("", "") == True)
    assert(areAnagrams("abCdabCd", "abcdabcd") == True)
    assert(areAnagrams("abcdaBcD", "AAbbcddc") == True)
    assert(areAnagrams("abcdaabcd", "aabbcddcb") == False)
    print("Passed!")

def testReplace():
    print('Testing replace()...', end='')
    assert(replace('abc', 'd', 'e') == 'abc'.replace('d', 'e'))
    assert(replace('abc', 'b', 'e') == 'abc'.replace('b', 'e'))
    assert(replace('abcb abc', 'b', 'e') == 'abcb abc'.replace('b', 'e'))
    assert(replace('abcb abc', 'ab', 'abd') == 'abcb abc'.replace('ab', 'abd'))
    print('Passed!')

def testWordWrap():
    print('Testing wordWrap()...', end='')
    assert(wordWrap("abc", 3) == "abc")
    assert(wordWrap("abc",2) == "ab\nc") 
    assert(wordWrap("abcdefghij", 4)  ==  """\
abcd
efgh
ij""")
    assert(wordWrap("a b c de fg",  4)  ==  """\
a-b
c-de
fg""")
    print('Passed!')

#################################################
# testAll and main
#################################################

def testAll():
    testVowelCount()
    testInterleave()
    testLongestCommonSubstring()
    testLeastFrequentLetters()
    testSameChars()
    testAreAnagrams()
    testReplace()
    testWordWrap()

def main():
    cs112_f19_week3_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
