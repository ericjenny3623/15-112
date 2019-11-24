import math


def withinThreshold(value, goal, epsilon):
    return math.abs(value-goal) <= epsilon


def sideFromLawOfSines(a, sinA, sinB):
    return (a * sinB / sinA)


def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5


def limit(x, max, min):
    assert max > min, "Max not greater than min"
    if x > max:
        return max
    elif x < min:
        return min
    else:
        return x


class Twist():

    def __init__(self, x=0.0, y=0.0, heading=0.0, r=0.0):
        self.setPosition(x, y, heading, r)

    def smartUpdateOrientation(self, heading, r):
        if heading != 0.0:
            headingNew = heading
            rNew = math.radians(heading)
        elif r != 0.0:
            rNew = r
            headingNew = math.degrees(r)
        else:
            rNew = 0.0
            headingNew = 0.0
        return headingNew, rNew

    def updateDeltas(self, deltaX, deltaY, deltaHeading=0.0, deltaR=0.0):
        self.x += deltaX
        self.y += deltaY
        deltaHeading, deltaR = self.smartUpdateOrientation(
            deltaHeading, deltaR)
        self.heading += deltaHeading
        self.r += deltaR

    def setPosition(self, x=None, y=None, heading=0.0, r=0.0):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.heading, self.r = self.smartUpdateOrientation(heading, r)
