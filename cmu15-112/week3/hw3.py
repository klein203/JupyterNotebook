#################################################
# hw3.py
#
# Your name:
# Your andrew id:
#################################################

import cs112_f19_week3_linter
import math
from tkinter import *

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

#################################################
# patternedMessage
#################################################

def patternedMessage(msg, pattern):
    import string
    
    def nextChar(msg):
        idx = 0
        l = len(msg)
        while True:
            yield msg[idx]
            idx = (idx + 1) % l
    
    ret = ''
    g = nextChar(msg.replace(' ', ''))
    omits = ['\n', '\r', ' ']
    p = pattern.strip()
    for i in range(len(p)):
        if p[i] in omits:
            ret += p[i]
        else:
            ret += next(g)
    
    return ret

#################################################
# encodeRightLeftRouteCipher + decodeRightLeftRouteCipher
#################################################

def encodeRightLeftRouteCipher(text, rows):
    import string
    import math
    
    def f(row, col, rows, cols):
        return col * rows + row
    
    cols = math.ceil(len(text) / rows)
    l = rows * cols
    
    # complete text
    text += string.ascii_lowercase[::-1][0:l - len(text)]
    text1d = [ch for ch in text]
    
    encode2d = [[''] * cols for i in range(rows)]
    for j in range(cols):
        for i in range(rows):
            if i % 2 == 0:
                encode2d[i][j] = text1d[f(i, j, rows, cols)]
            else:
                encode2d[i][cols - 1 - j] = text1d[f(i, j, rows, cols)]

    # start from row
    ret = str(rows)
    for row in encode2d:
        ret += ''.join(row)

    return ret

def decodeRightLeftRouteCipher(cipher):
    import re
    
    def f(l, rows, cols):
        return (l // cols, l % cols)

    r = re.compile("^[0-9]+")

    pos = None
    if r.search(cipher) is not None:
        pos = r.search(cipher).span()
    else:
        return None
    
    rows = int(cipher[pos[0]:pos[1]])
    
    text = cipher[pos[1]:]
    text1d = [ch for ch in text]
    
    l = len(text)
    cols = l // rows
    
    decode2d = [[''] * cols for i in range(rows)]
    for i in range(rows * cols):
        (row, col) = f(i, rows, cols)
        if row % 2 == 0:
            decode2d[row][col] = text1d[i]
        else:
            decode2d[row][cols - 1 - col] = text1d[i]
    
    ret = ''
    for j in range(cols):
        ret += ''.join([row[j] for row in decode2d])
    
    if ret.find('z') != -1:
        idx = ret.index('z')
        ret = ret[0:idx]
    
    return ret

#################################################
# drawSimpleTortoiseProgram
#################################################

def drawSimpleTortoiseProgram(program, canvas, width, height):
    import math
    
    glb = {
        'x': width // 2,
        'y': height // 2,
        'degree': 0, # to the east
        'color': 'none'
    }

    def changeColor(canvas, glb, color):
        if color in ['none', 'blue', 'red', 'green', 'orange', 'purple']:
            glb['color'] = color
    
    def changeDirection(canvas, glb, delta):
        glb['degree'] = (glb['degree'] + delta) % 360
    
    def move(canvas, glb, length):
        x = float(glb['x'])
        y = float(glb['y'])
        degree = float(glb['degree'])
        fill = glb['color']
        
        x1 = x + math.cos(math.radians(degree)) * length
        y1 = y + math.sin(math.radians(degree)) * length
        if fill != 'none':
            canvas.create_line(x, y, x1, y1, fill=fill)
        glb['x'] = x1
        glb['y'] = y1
    
    def callFunc(f, canvas, glb, *args):
        f(canvas, glb, *args)
    
    def parseCommand(s, canvas, glb):
        commands = ['color', 'move', 'left', 'right']
        args = s.split(" ")
        if args[0] in commands:
            if args[0] == commands[0]:
                callFunc(changeColor, canvas, glb, args[1])
            elif args[0] == commands[1]:
                callFunc(move, canvas, glb, float(args[1]))
            elif args[0] == commands[2]:
                callFunc(changeDirection, canvas, glb, -float(args[1]))
            elif args[0] == commands[3]:
                callFunc(changeDirection, canvas, glb, float(args[1]))
            else:
                pass
        else:
            return "error"
        
    def parseCommands(program, canvas, glb):
        import io
        
        buf = io.StringIO(program)
        while True:
            if buf.tell() == len(program):
                break
            
            s = buf.readline()
            
            s = s.strip()
            if s.find('#') != -1:
                s = s[0:s.index('#')]
            if s == '':
                continue
            
            parseCommand(s, canvas, glb)
        
        buf.close()

    parseCommands(program, canvas, glb)
    
#################################################
# drawNiceRobot
#################################################

def drawNiceRobot(canvas, width, height):
    canvas.create_text(width/2, height/2, text='<TBD: Draw your Robot here!>')

#################################################
# bonus/optional getEvalSteps
#################################################

def getEvalSteps(expr):
    return 42

#################################################
# bonus/optional topLevelFunctionNames
#################################################

def topLevelFunctionNames(code):
    return 42

#################################################
# Test Functions
#################################################

def testPatternedMessage():
    print("Testing patternedMessage()...", end="")
    assert(patternedMessage("abc def",   "***** ***** ****")   ==
           "abcde fabcd efab")
    assert(patternedMessage("abc def", "\n***** ***** ****\n") == 
           "abcde fabcd efab")
    parms = [
    ("Go Pirates!!!", """
***************
******   ******
***************
"""),
    ("Three Diamonds!","""
    *     *     *
   ***   ***   ***
  ***** ***** *****
   ***   ***   ***
    *     *     *
"""),
    ("Go Steelers!","""
                          oooo$$$$$$$$$$$$oooo
                      oo$$$$$$$$$$$$$$$$$$$$$$$$o
                   oo$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$o         o$   $$ o$
   o $ oo        o$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$o       $$ $$ $$o$
oo $ $ '$      o$$$$$$$$$    $$$$$$$$$$$$$    $$$$$$$$$o       $$$o$$o$
'$$$$$$o$     o$$$$$$$$$      $$$$$$$$$$$      $$$$$$$$$$o    $$$$$$$$
  $$$$$$$    $$$$$$$$$$$      $$$$$$$$$$$      $$$$$$$$$$$$$$$$$$$$$$$
  $$$$$$$$$$$$$$$$$$$$$$$    $$$$$$$$$$$$$    $$$$$$$$$$$$$$  '$$$
   '$$$'$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     '$$$
    $$$   o$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     '$$$o
   o$$'   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$       $$$o
   $$$    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$' '$$$$$$ooooo$$$$o
  o$$$oooo$$$$$  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$   o$$$$$$$$$$$$$$$$$
  $$$$$$$$'$$$$   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     $$$$'
 ''''       $$$$    '$$$$$$$$$$$$$$$$$$$$$$$$$$$$'      o$$$
            '$$$o     '$$$$$$$$$$$$$$$$$$'$$'         $$$
              $$$o          '$$'$$$$$$'           o$$$
               $$$$o                                o$$$'
                '$$$$o      o$$$$$$o'$$$$o        o$$$$
                  '$$$$$oo     '$$$$o$$$$$o   o$$$$'
                     '$$$$$oooo  '$$$o$$$$$$$$$'
                        '$$$$$$$oo $$$$$$$$$$
                                '$$$$$$$$$$$
                                    $$$$$$$$$$$$
                                     $$$$$$$$$$'
                                      '$$$'
""")]
    solns = [
"""
GoPirates!!!GoP
irates   !!!GoP
irates!!!GoPira
"""
,
"""
    T     h     r
   eeD   iam   ond
  s!Thr eeDia monds
   !Th   ree   Dia
    m     o     n
"""
,
"""
                          GoSteelers!GoSteeler
                      s!GoSteelers!GoSteelers!GoS
                   teelers!GoSteelers!GoSteelers!GoS         te   el er
   s ! Go        Steelers!GoSteelers!GoSteelers!GoSteel       er s! GoSt
ee l e rs      !GoSteeler    s!GoSteelers!    GoSteelers       !GoSteel
ers!GoSte     elers!GoSt      eelers!GoSt      eelers!GoSt    eelers!G
  oSteele    rs!GoSteele      rs!GoSteele      rs!GoSteelers!GoSteeler
  s!GoSteelers!GoSteelers    !GoSteelers!G    oSteelers!GoSt  eele
   rs!GoSteelers!GoSteelers!GoSteelers!GoSteelers!GoSteel     ers!
    GoS   teelers!GoSteelers!GoSteelers!GoSteelers!GoSteelers     !GoSt
   eele   rs!GoSteelers!GoSteelers!GoSteelers!GoSteelers!GoSt       eele
   rs!    GoSteelers!GoSteelers!GoSteelers!GoSteelers!Go Steelers!GoSteele
  rs!GoSteelers  !GoSteelers!GoSteelers!GoSteelers!GoS   teelers!GoSteelers
  !GoSteelers!G   oSteelers!GoSteelers!GoSteelers!Go     Steel
 ers!       GoSt    eelers!GoSteelers!GoSteelers!G      oSte
            elers     !GoSteelers!GoSteelers!         GoS
              teel          ers!GoSteel           ers!
               GoSte                                elers
                !GoSte      elers!GoSteele        rs!Go
                  Steelers     !GoSteelers!   GoStee
                     lers!GoSte  elers!GoSteeler
                        s!GoSteele rs!GoSteel
                                ers!GoSteele
                                    rs!GoSteeler
                                     s!GoSteeler
                                      s!GoS
"""
    ]
    parms = [("A-C D?", """
*** *** ***
** ** ** **
"""),
    ("A", "x y z"),
    ("The pattern is empty!", "")
    ]
    solns = [
"""
A-C D?A -CD
?A -C D? A-
""",
"A A A",
""
    ]
    for i in range(len(parms)):
        (msg,pattern) = parms[i]
        soln = solns[i]
        soln = soln.strip("\n")
        observed = patternedMessage(msg, pattern)
        #observed = patternedMessage(msg, pattern).strip("\n")
        #print "\n\n***********************\n\n"
        #print msg, pattern
        #print "<"+patternedMessage(msg, pattern)+">"
        #print "<"+soln+">"
        assert(observed == soln)
    print("Passed!")

def testEncodeRightLeftRouteCipher():
    print('Testing encodeRightLeftRouteCipher()...', end='')
    assert(encodeRightLeftRouteCipher("WEATTACKATDAWN",4) ==
                                      "4WTAWNTAEACDzyAKT")
    assert(encodeRightLeftRouteCipher("WEATTACKATDAWN",3) ==
                                      "3WTCTWNDKTEAAAAz") 
    assert(encodeRightLeftRouteCipher("WEATTACKATDAWN",5) ==
                                      "5WADACEAKWNATTTz") 
    print('Passed!')

def testDecodeRightLeftRouteCipher():
    print('Testing decodeRightLeftRouteCipher()...', end='')
    assert(decodeRightLeftRouteCipher("4WTAWNTAEACDzyAKT") ==
                                      "WEATTACKATDAWN")
    assert(decodeRightLeftRouteCipher("3WTCTWNDKTEAAAAz") ==
                                      "WEATTACKATDAWN") 
    assert(decodeRightLeftRouteCipher("5WADACEAKWNATTTz") ==
                                      "WEATTACKATDAWN") 
    text = "WEATTACKATDAWN"
    cipher = encodeRightLeftRouteCipher(text, 6)
    plaintext = decodeRightLeftRouteCipher(cipher)
    assert(plaintext == text)
    print('Passed!')

def runDrawNiceRobot(width=300, height=300):
    root = Tk()
    root.resizable(width=False, height=False) # non-resizable
    canvas = Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    drawNiceRobot(canvas, width, height)
    root.mainloop()
    print("bye!")

def runDrawSimpleTortoiseProgram(program, width, height):
    root = Tk()
    root.resizable(width=False, height=False) # non-resizable
    canvas = Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    drawSimpleTortoiseProgram(program, canvas, width, height)
    root.mainloop()
    print("bye!")

def testDrawSimpleTortoiseProgram():
    print("Testing drawSimpleTortoiseProgram()...")
    print("Since this is graphics, this test is not interactive.")
    print("Inspect each of these results manually to verify them.")
    runDrawSimpleTortoiseProgram("""
# This is a simple tortoise program
color blue
move 50

left 90

color red
move 100

color none # turns off drawing
move 50

right 45

color green # drawing is on again
move 50

right 45

color orange
move 50

right 90

color purple
move 100
""", 300, 400)

    runDrawSimpleTortoiseProgram("""
# Y
color red
right 45
move 50
right 45
move 50
right 180
move 50
right 45
move 50
color none # space
right 45
move 25

# E
color green
right 90
move 85
left 90
move 50
right 180
move 50
right 90
move 42
right 90
move 50
right 180
move 50
right 90
move 43
right 90
move 50  # space
color none
move 25

# S
color blue
move 50
left 180
move 50
left 90
move 43
left 90
move 50
right 90
move 42
right 90
move 50
""", 500, 500)
    print("Done!")

def testDrawNiceRobot():
    print('Calling runDrawRobot(400, 400):')
    runDrawNiceRobot(400, 400)
    print('Calling runDrawRobot(800, 800):')
    runDrawNiceRobot(800, 800)

def testBonusTopLevelFunctionNames():
    print("Testing topLevelFunctionNames()...", end="")

    # no fn defined
    code = """\
# This has no functions!
# def f(): pass
print("Hello world!")
"""
    assert(topLevelFunctionNames(code) == "")

    # f is redefined
    code = """\
def f(x): return x+42
def g(x): return x+f(x)
def f(x): return x-42
"""
    assert(topLevelFunctionNames(code) == "f.g")

    # def not at start of line
    code = """\
def f(): return "def g(): pass"
"""
    assert(topLevelFunctionNames(code) == "f")

    # g() is in triple-quotes (''')
    code = """\
def f(): return '''
def g(): pass'''
"""
    assert(topLevelFunctionNames(code) == "f")

    # g() is in triple-quotes (""")
    code = '''\
def f(): return """
def g(): pass"""
'''
    assert(topLevelFunctionNames(code) == "f")

    # triple-quote (''') in comment
    code = """\
def f(): return 42 # '''
def g(): pass # '''
"""
    assert(topLevelFunctionNames(code) == "f.g")

    # triple-quote (""") in comment
    code = '''\
def f(): return 42 # """
def g(): pass # """
'''
    assert(topLevelFunctionNames(code) == "f.g")

    # comment character (#) in quotes
    code = """\
def f(): return '#' + '''
def g(): pass # '''
def h(): return "#" + '''
def i(): pass # '''
def j(): return '''#''' + '''
def k(): pass # '''
"""
    assert(topLevelFunctionNames(code) == "f.h.j")
    print("Passed!")

def testBonusGetEvalSteps():
    print("Testing getEvalSteps()...", end="")
    assert(getEvalSteps("0") == "0 = 0")
    assert(getEvalSteps("2") == "2 = 2")
    assert(getEvalSteps("3+2") == "3+2 = 5")
    assert(getEvalSteps("3-2") == "3-2 = 1")
    assert(getEvalSteps("3**2") == "3**2 = 9")
    assert(getEvalSteps("31%16") == "31%16 = 15")
    assert(getEvalSteps("31*16") == "31*16 = 496")
    assert(getEvalSteps("32//16") == "32//16 = 2")
    assert(getEvalSteps("2+3*4") == "2+3*4 = 2+12\n      = 14")
    assert(getEvalSteps("2*3+4") == "2*3+4 = 6+4\n      = 10")
    assert(getEvalSteps("2+3*4-8**3%3") == """\
2+3*4-8**3%3 = 2+3*4-512%3
             = 2+12-512%3
             = 2+12-2
             = 14-2
             = 12""")
    assert(getEvalSteps("2+3**4%2**4+15//3-8") == """\
2+3**4%2**4+15//3-8 = 2+81%2**4+15//3-8
                    = 2+81%16+15//3-8
                    = 2+1+15//3-8
                    = 2+1+5-8
                    = 3+5-8
                    = 8-8
                    = 0""")
    print("Passed!")

#################################################
# testAll and main
#################################################

def testAll():
    testPatternedMessage()
    testEncodeRightLeftRouteCipher()
    testDecodeRightLeftRouteCipher()
    testDrawSimpleTortoiseProgram()
    testDrawNiceRobot()
    testBonusTopLevelFunctionNames()
    testBonusGetEvalSteps()

def main():
#     cs112_f19_week3_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
