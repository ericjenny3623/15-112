#################################################
# hw2.py
#
# Your name: Eric Jenny
# Your andrew id: ejenny
#################################################

import cs112_f19_week2_linter
import math
from tkinter import *
import random

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

def integral(f, a, b, N):
    width = (b-a)/N
    integral = 0
    for i in range(N):
        x1 = a + (width*i) 
        x2 = x1 + width
        y1 = f(x1)
        y2 = f(x2)
        integral += getTrapezoidArea(y1, y2, width)
    return integral        

def getTrapezoidArea(y1, y2, width):
    return width * (y1 + y2)/2

def nthSmithNumber(n):
    count = -1
    i = 1
    while count < n:
        i += 1
        if checkSmith(i):
            count += 1
    return i

def checkSmith(x):
    digitSum = sumDigits(x)
    factorSum = sumPrimeFactors(x)
    if digitSum == factorSum:
        print (x)
    return digitSum == factorSum

def sumDigits(x):
    sum = 0
    while x>0:
        sum += x%10
        x //= 10
    return sum

def sumPrimeFactors(x):
    sum = 0
    ogX = x
    while x > 1:
        f = 2
        while x%f != 0:
            f += 1
        if f == ogX:
            sum += f + 1
        else:
            sum += sumDigits(f)
        x /= f
    return sum

def drawPattern1(points, canvas, width, height):
    kW = width/points
    kH = height/points
    for i in range(0, points):
        canvas.create_line(i*kW, 0, width, height-i*kH)
        canvas.create_line(0, i*kH, width-i*kW, height)
        canvas.create_line(width-i*kW, 0, 0, height-i*kH)
        canvas.create_line(i*kW, height, width, i*kH)

def drawPattern2(points, canvas, width, height):
    kW = width/points/2
    kH = height/points/2
    xM = width/2
    yM = height/2
    for i in range(0, points):
        canvas.create_line(xM, i*kH, xM+i*kW, height/2)
        canvas.create_line(xM, yM+i*kH, width-i*kW, yM)
        canvas.create_line(xM-i*kW, yM, xM, height-i*kH)
        canvas.create_line(xM, yM-i*kH, i*kW, yM)

def drawPattern3(points, canvas, width, height):
    isTriangle = True
    kH = height/points
    for n in range(points):
        if isTriangle:
            drawTriangles(canvas, points, width, n*kH, kH)
        else:
            drawSquares(canvas, points, width, n*kH, kH)
        isTriangle = not isTriangle

def drawTriangles(canvas, n, width, yStart, yHeight):
    canvas.create_line(0, yStart, width, yStart)
    print(yStart, width)
    kW = width/n
    for i in range(n):
        print("yuh")
        leftX = i*kW
        canvas.create_line(leftX, yStart, leftX+kW/2, yStart+yHeight)
        canvas.create_line(leftX+kW/2, yStart+yHeight, leftX+kW, yStart)


def drawSquares(canvas, n, width, yStart, yHeight):
    canvas.create_line(0, yStart, width, yStart)
    kW = width/n
    for i in range(n):
        leftX = i*kW
        canvas.create_line(leftX, yStart, leftX, yStart+yHeight)

def drawPattern4(canvas, width, height):
    y = 0
    n = 1
    while y < height:
        y += n
        n += (n*0.3)/5
        canvas.create_line(0, y, width, y)

# def drawDashs(canvas, fill, width, height):
#     x = 0
#     while x < width:
#         canvas,create_line(x, height, )

def playPig():
    print("""Welcome to Banana Pig, a console based
     implementation of the classic dice game. 
     Instructions are for chumps, lets just play!""")
    score1, score2 = 0, 0
    while True: #ik this is bad practice but im low on time
        score1 = turn("Banana", score1)
        score2 = turn("Lemon", score2)

        if score1 == -1 or score2 == -1:
            print("Okay, stopping")
            break
        elif score1 == -2 or score2 == -2:
            print("Resetting scores.")
            score1, score2 = 0, 0


def turn(player, score):
    tempScore = 0
    while tempScore + score < 100:
        choice = input (f"{player} what would you like to do? ")
        if "h" in choice:
            print(f"  Okay. You added {tempScore} to your score",
                  f"for a total of {tempScore + score}")
            return tempScore + score
        elif "r" in choice:
            roll = rollDice()
            print(f"  You rolled {roll}", end= "")
            if roll == 1:
                print(f". How unfortunate :(")
                return 0
            else:
                tempScore += roll
                print(f" for a total score this turn of {tempScore}")
        elif "stop" in choice or "q" in choice:
            return -1 # -1 to indicate forced stop
        else:
            print("Huh? ")
    print(f"*** Congrats! you ({player}) won!! ***")
    return -2 # indicates win

def rollDice():
    return random.randint(1, 6)

#################################################
# Bonus/Optional functions for you to write
#################################################

def bonusCarrylessMultiply(x1, x2):
    return 42

def bonusPlay112(game):
    return 42

#################################################
# Test Functions
#################################################

def f1(x): return 42
def i1(x): return 42*x 
def f2(x): return 2*x  + 1
def i2(x): return x**2 + x
def f3(x): return 9*x**2
def i3(x): return 3*x**3
def f4(x): return math.cos(x)
def i4(x): return math.sin(x)
def testIntegral():
    print('Testing integral()...', end='')
    epsilon = 10**-4
    assert(almostEqual(integral(f1, -5, +5, 1), (i1(+5)-i1(-5)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f1, -5, +5, 10), (i1(+5)-i1(-5)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f2, 1, 2, 1), 4,
                      epsilon=epsilon))
    assert(almostEqual(integral(f2, 1, 2, 250), (i2(2)-i2(1)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f3, 4, 5, 250), (i3(5)-i3(4)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f4, 1, 2, 250), (i4(2)-i4(1)),
                      epsilon=epsilon))
    print("Passed!")

def testNthSmithNumber():
    print('Testing nthSmithNumber()... ', end='')
    assert(nthSmithNumber(0) == 4)
    assert(nthSmithNumber(1) == 22)
    assert(nthSmithNumber(2) == 27)
    assert(nthSmithNumber(3) == 58)
    assert(nthSmithNumber(4) == 85)
    assert(nthSmithNumber(5) == 94)
    print('Passed.')

def runDrawPattern1(points, width=300, height=300):
    root = Tk()
    root.resizable(width=False, height=False) # non-resizable
    canvas = Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    drawPattern1(points, canvas, width, height)
    root.mainloop()
    print("bye!")

def runDrawPattern2(points, width=300, height=300):
    root = Tk()
    root.resizable(width=False, height=False) # non-resizable
    canvas = Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    drawPattern2(points, canvas, width, height)
    root.mainloop()
    print("bye!")

def runDrawPattern3(points, width=300, height=300):
    root = Tk()
    root.resizable(width=False, height=False) # non-resizable
    canvas = Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    drawPattern3(points, canvas, width, height)
    root.mainloop()
    print("bye!")

def runDrawPattern4(width=300, height=300):
    root = Tk()
    root.resizable(width=False, height=False) # non-resizable
    canvas = Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    drawPattern4(canvas, width, height)
    root.mainloop()
    print("bye!")

def testDrawPatterns():
    print('** Note: You need to manually test drawPatterns()')
    print('Calling runDrawPattern1(5, 400, 400):')
    runDrawPattern1(5, 400, 400)
    print('Calling runDrawPattern1(10, 800, 400):')
    runDrawPattern1(10, 800, 400)
    print('Calling runDrawPattern2(5, 400, 400):')
    runDrawPattern2(5, 400, 400)
    print('runDrawPattern2(10, 800, 400):')
    runDrawPattern2(10, 800, 400)
    print('runDrawPattern3(5, 400, 400):')
    runDrawPattern3(5, 400, 400)
    print('runDrawPattern3(10, 800, 400)')
    runDrawPattern3(10, 800, 400)
    print('runDrawPattern4(600, 600)')
    runDrawPattern4(600, 600)

def testPlayPig():
    print('** Note: You need to manually test playPig()')

def testBonusCarrylessMultiply():
    print("Testing bonusCarrylessMultiply()...", end="")
    assert(bonusCarrylessMultiply(643, 59) == 417)
    assert(bonusCarrylessMultiply(6412, 387) == 807234)
    print("Passed!")

def testBonusPlay112():
    print("Testing bonusPlay112()... ", end="")
    assert(bonusPlay112( 5 ) == "88888: Unfinished!")
    assert(bonusPlay112( 521 ) == "81888: Unfinished!")
    assert(bonusPlay112( 52112 ) == "21888: Unfinished!")
    assert(bonusPlay112( 5211231 ) == "21188: Unfinished!")
    assert(bonusPlay112( 521123142 ) == "21128: Player 2 wins!")
    assert(bonusPlay112( 521123151 ) == "21181: Unfinished!")
    assert(bonusPlay112( 52112315142 ) == "21121: Player 1 wins!")
    assert(bonusPlay112( 523 ) == "88888: Player 1: move must be 1 or 2!")
    assert(bonusPlay112( 51223 ) == "28888: Player 2: move must be 1 or 2!")
    assert(bonusPlay112( 51211 ) == "28888: Player 2: occupied!")
    assert(bonusPlay112( 5122221 ) == "22888: Player 1: occupied!")
    assert(bonusPlay112( 51261 ) == "28888: Player 2: offboard!")
    assert(bonusPlay112( 51122324152 ) == "12212: Tie!")
    print("Passed!")

#################################################
# testAll and main
#################################################

def testAll():
    testIntegral()
    testNthSmithNumber()
    testDrawPatterns()
    testPlayPig()
    # playPig()
    #testBonusCarrylessMultiply()
    #testBonusPlay112()

def main():
    cs112_f19_week2_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
