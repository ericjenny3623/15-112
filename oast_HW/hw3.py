#################################################
# hw3.py
#
# Your name: Eric Jenny
# Your andrew id: ejenny
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
import string

def isWhitespace(c):
    """ returns true if c is a whitespace character """
    return c in string.whitespace

def patternedMessage(msg, pattern):
    msg = formatMessage(msg)
    pattern = formatPattern(pattern)
    patternedMessage = ""
    index = 0
    for c in pattern:
        if isWhitespace(c):
            patternedMessage += c
        else:
            patternedMessage += msg[index]
            index += 1
            index %= len(msg)
    return patternedMessage

def formatMessage(s):
    """ Takes an input of string s and removes whitespace characters.
    """
    formatted = ""
    for c in s:
        if not isWhitespace(c):
            formatted += c
    return formatted

def formatPattern(s):
    reverse = s[::-1]
    for c in s:
        if c == "\n":
            s = s[1:]
        else:
            break
    for c in reverse:
        if c == "\n":
            s = s[:-1]
        else:
            break
    return s

#################################################
# encodeRightLeftRouteCipher + decodeRightLeftRouteCipher
#################################################

def encodeRightLeftRouteCipher(text, rows):
    cols = math.ceil(len(text)/rows)
    encoded = str(rows)
    extraLetterIndex = 25
    for r in range(rows):
        for c in range(cols):
            if r%2 == 0:
                index = r + c*rows
            else:
                index = r + rows*cols - (c+1)*rows
            if index > len(text)-1:
                encoded += string.ascii_lowercase[extraLetterIndex]
                extraLetterIndex -= 1
                extraLetterIndex % 26
            else:
                encoded += text[index] 
    return encoded

def decodeRightLeftRouteCipher(cipher):
    return 42

#################################################
# drawSimpleTortoiseProgram
#################################################

def drawSimpleTortoiseProgram(program, canvas, width, height):
    cursorX = width/2
    cursorY = height/2
    cursorR = 0 # heading in degrees, postive being ccw, and 0 being east
    cursorC = "none"
    color = "color"
    left = "left"
    right = "right"
    move = "move"
    canvas.create_text(10, 0, 
                       text=program, 
                       fill="grey", 
                       anchor=NW, 
                       font="Roboto 10")
    for line in program.splitlines():
        line = removeComments(line)
        if color in line:
            cursorC = getValue(line, color)
        if move in line:
            dist = int(getValue(line, move))
            cursorX, cursorY = drawMovement(canvas,
                                            dist, 
                                            cursorX, 
                                            cursorY, 
                                            cursorR, 
                                            cursorC)
        if left in line:
            cursorR -= int(getValue(line, left))
        if right in line:
            cursorR += int(getValue(line, right))

def drawMovement(canvas, d, x, y, r, c):
    lineWidth = 4
    endX = x + math.cos(math.radians(r))*d
    endY = y + math.sin(math.radians(r))*d
    if not "none" in c:
        canvas.create_line(x, y, endX, endY, fill=c, width=lineWidth)
    return endX, endY

def getValue(line, command):
    startIndex = line.find(command)+len(command)
    endIndex = 0
    for n in range(startIndex+1, len(line)):
        if isWhitespace(line[n]):
            break
        endIndex = n
    return line[startIndex+1:n+1]

def removeComments(line):
    index = line.find("#")
    if index == 0:
        return ""
    elif index != -1:
        return line[:index-1]
    else:
        return line

#################################################
# drawNiceRobot
#################################################

def drawNiceRobot(canvas, width, height):
    imageR = 1.7
    trimmedWidth, trimmedHeight = getMaxDimensions(width, height, imageR, 10)
    xOffset = (width-trimmedWidth)/2
    yOffset = (height-trimmedHeight)/2
    canvas.create_rectangle(xOffset-1,
                            yOffset-1,
                            width-xOffset+1,
                            height-yOffset+1)

    perspectiveAngle = math.radians(25)

 
    nWheels = 4
    wheelRadiusR = 0.2
    wheelDistR = 0.18
    firstWheelX = 0.2
    firstWheelY = 0.6
    bodyLengthR = 0.7
    bodyHeightR = 0.3
    bodyStartX = firstWheelX - 0.05
    bodyStartY = firstWheelY - 0.05

    x1 = (bodyStartX*trimmedWidth) + xOffset
    y1 = (bodyStartY*trimmedHeight) + yOffset
    x2 = x1 + (math.cos(perspectiveAngle)*bodyLengthR*trimmedWidth)
    y2 = y1 + (math.sin(perspectiveAngle)*bodyLengthR*trimmedWidth)
    x3 = x1
    y3  = y1 - (bodyHeightR*trimmedHeight)
    x4 = x2
    y4 = y2 - (bodyHeightR*trimmedHeight)
    canvas.create_polygon(x1, y1, x3, y3, x4, y4, x2, y2, fill="blue")

    x5 = x3 + (0.1*trimmedWidth)
    y5 = y3 + (0.1*trimmedHeight)
    x6 = x5 + (math.cos(perspectiveAngle)*bodyLengthR*trimmedWidth)
    y6 = y5 + (math.sin(perspectiveAngle)*bodyLengthR*trimmedWidth)
    canvas.create_polygon(x3, y3, x2, y2, x5, y5, x6, y6, fill="blue")

    for n in range(nWheels):
        centerXR = firstWheelX + n*wheelDistR*math.cos(perspectiveAngle)
        centerYR = firstWheelY + n*wheelDistR*math.sin(perspectiveAngle)
        drawPerspectiveCircle(canvas, centerXR, centerYR,
                             wheelRadiusR, perspectiveAngle,
                             trimmedWidth, trimmedHeight,
                             xOffset, yOffset,
                             "grey")
        drawPerspectiveCircle(canvas, centerXR, centerYR,
                             wheelRadiusR/2, perspectiveAngle,
                             trimmedWidth, trimmedHeight,
                             xOffset, yOffset,
                             "black")

def drawPerspectiveCircle(canvas,
                         centerXR, centerYR, 
                         radius, perspectiveAngle,
                         scaleX, scaleY, 
                         xOffset, yOffset, 
                         color):
    x1R = centerXR - (radius*math.sin(perspectiveAngle))
    y1R = centerYR - (radius*math.cos(perspectiveAngle))
    x2R = centerXR + (radius*math.sin(perspectiveAngle))
    y2R = centerYR + (radius*math.cos(perspectiveAngle))
    x1 = x1R*scaleX + xOffset
    y1 = y1R*scaleY + yOffset
    x2 = x2R*scaleX + xOffset
    y2 = y2R*scaleY + yOffset
    canvas.create_oval(x1, y1, x2, y2, fill=color)

def getMaxDimensions(width, height, ratio, border = 0):
    """ Returns the maxium dimensions of a to scale image given a preset
    width and height. Ratio is defined as the actual images width/height.
    """
    if width < height*ratio:
        trimmedHeight = width/ratio - border
    else:
        trimmedHeight = height-(ratio*border)
    return trimmedHeight*ratio, trimmedHeight

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
    # assert(encodeRightLeftRouteCipher("WEATTACKATDAWN",4) ==
    #                                   "4WTAWNTAEACDzyAKT")
    # assert(encodeRightLeftRouteCipher("WEATTACKATDAWN",3) ==
    #                                   "3WTCTWNDKTEAAAAz") 
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
    # testDecodeRightLeftRouteCipher()
    testDrawSimpleTortoiseProgram()
    testDrawNiceRobot()
    # testBonusTopLevelFunctionNames()
    # testBonusGetEvalSteps()

def main():
    cs112_f19_week3_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
