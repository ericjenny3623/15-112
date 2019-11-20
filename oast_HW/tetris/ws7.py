
###############################################################################
# Writing Session 7, Coding Portion: [19 pts]

# Do not edit these lines:
#   user: 'ejenny@andrew.cmu.edu' (do not edit this!)
#   downloaded at: '2019-10-11 11:36:25' (do not edit this!)
#   downloaded ip: '128.237.157.147' (do not edit this!)
#   security code: '32302115223725195751ENGQRZABPFTFX2GMW2IFW' (do not edit this!)

# Note #1: If you are not in a proctored writing-session lab, close this file
# immediately and email koz@cmu.edu and mdtaylor@andrew.cmu.edu to let
# us know that this occurred.

# Note #2: Do not edit this header, only edit the code below the header.

# Note #3: Select-all and copy this entire file, all of it, exactly as it
# is here, paste it into your ws7.py starter file, then edit it, and submit
# that edited file to Autolab while you are still in the proctored
# writing-session lab.

# Starting from the starter code below, write an animation
# according to these rules:

# 1. Moving a Dot with Arrows and Wraparound
# Add a blue dot of radius 10, initially in the middle of the canvas
# that moves vertically in response to
# up and down arrows (not left and right arrows), 13 pixels per arrow press,
# and uses wraparound, so if any part of the dot would extend beyond an edge,
# instead the entire dot appears just inside the opposite edge.

# 2. Bouncing Square
# Add a yellow bouncing 20x20 square.  It should start anyhwere you wish on
# the canvas, moving with dx=5 and dy=10.  The square should bounce
# back-and-forth in both the x and y dimensions.  Here, the square may extend
# partly beyond an edge, at which point it should bounce back in the opposing
# direction (so you do not have to adjust the square to exactly sit against an
# edge, just bounce when it extends beyond an edge).  Do not use OOP here to
# store the square or its location.

# 3. Adding and Deleting Shapes with OOP
# Note: for this part only, you need to use a class Dot that stores the cx, cy
# locations of each green dot.  With that, each time the user clicks the mouse,
# draw a new green dot of radius 10 in that location (so there are more green
# dots as the user repeatedly presses the mouse).  To do this, add a Dot
# instance to the list app.dots.  Note that you do not have to delete any
# green dots.

###############################################################################

from cmu_112_graphics import *
from tkinter import *


def appStarted(app):
    app.circleX = app.width/2
    app.circleY = app.height/2
    app.circleRadius = 10
    app.circleColor = "blue"

    app.squareHalfSize = 10
    app.squareX = app.width*0.2
    app.squareY = app.height*0.6
    app.squareDx = 5
    app.squareDy = 10
    app.squareColor = "yellow"

    app.dots = []
    app.dotRadius = 10
    app.dotColor = "green"


def keyPressed(app, event):
    key = event.key
    if key == "Up":
        app.circleY -= 13
    elif key == "Down":
        app.circleY += 13

    circleYMin = app.circleRadius
    circleYMax = app.height-app.circleRadius
    app.circleY = wrapLimit(circleYMin, circleYMax, app.circleY)


def mousePressed(app, event):
    app.dots.append(Dot(event.x, event.y))


def timerFired(app):
    squareYMin = app.squareHalfSize
    squareYMax = app.height-app.squareHalfSize
    if app.squareY != wrapLimit(squareYMin, squareYMax, app.squareY):
        app.squareDy *= -1

    squareXMin = app.squareHalfSize
    squareXMax = app.width-app.squareHalfSize
    if app.squareX != wrapLimit(squareXMin, squareXMax, app.squareX):
        app.squareDx *= -1

    app.squareX += app.squareDx
    app.squareY += app.squareDy


def wrapLimit(min, max, x):
    if x < min:
        x = max
    elif x > max:
        x = min
    return x


def redrawAll(app, canvas):
    drawCircle(app, canvas)
    drawSquare(app, canvas)
    drawDots(app, canvas)


def drawCircle(app, canvas):
    x, y = app.circleX, app.circleY
    r = app.circleRadius
    color = app.circleColor
    canvas.create_oval(x+r, y+r, x-r, y-r, fill=color)


def drawSquare(app, canvas):
    x, y = app.squareX, app.squareY
    r = app.squareHalfSize
    color = app.squareColor
    canvas.create_rectangle(x+r, y+r, x-r, y-r, fill=color)


def drawDots(app, canvas):
    for dot in app.dots:
        x, y = dot.cx, dot.cy
        r = app.dotRadius
        color = app.dotColor
        canvas.create_oval(x+r, y+r, x-r, y-r, fill=color)


class Dot:
    def __init__(self, x, y):
        self.cx = x
        self.cy = y


runApp(width=400, height=150)  # 400x150
