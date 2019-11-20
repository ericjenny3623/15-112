# Drive the robot according to user key inputs
# The user can drag and drop paths
# Have the robot be able to follow a few paths(even if it’s not your final algorithm)


from cmu_112_graphics import *
from tkinter import *
from robot import RobotModel
import Utils
import math


class SimulationApp(App):

    def appStarted(self):
        self._fieldImage = self.loadImage("2019-field-blue.png")
        self.fieldImageScaled = ImageTk.PhotoImage(self._fieldImage)
        self.setAppDims()
        self.FIELD_REAL_WIDTH = 8.23  # meters
        self.FIELD_REAL_HEIGHT = 9  # 16.46

        self.robot = RobotModel(1, 1)
        self._robotImage = self.scaleImage(self.loadImage("steve.jpg"), 0.6)
        self.leftVoltage, self.rightVoltage = 0.0, 0.0
        self.forwardVoltage, self.turnVotlage = 0.0, 0.0

        self.waypoints = []
        self.waypointRadius = 20
        self.selectedWaypoint = None

        self.timerDelay = 30  # milliseconds
        self.timer = 0
        self.releaseDelay = 0.1
        self.upKey = KeyLatch(self.releaseDelay)
        self.downKey = KeyLatch(self.releaseDelay)
        self.rightKey = KeyLatch(self.releaseDelay)
        self.leftKey = KeyLatch(self.releaseDelay)

    def timerFired(self):
        deltaTime = self.timerDelay/1000.0
        self.timer += deltaTime
        self.robot.updateVoltage(
            self.leftVoltage, self.rightVoltage, deltaTime)
        self.robot.updatePositionWithVelocity(deltaTime)

        avgVoltage = (self.leftVoltage + self.rightVoltage) / 2.0
        turnVoltage = 2.0
        if self.upKey.getIsActive(self.timer):
            avgVoltage += 9.0
        elif self.downKey.getIsActive(self.timer):
            avgVoltage -= 0.9
        else:
            turnVoltage = 4.0
            if avgVoltage > 0.0:
                avgVoltage -= 2.0
                if avgVoltage < 0.0:
                    avgVoltage = 0.0
            elif avgVoltage < 0.0:
                avgVoltage += 2.0
                if avgVoltage > 0.0:
                    avgVotlage = 0.0

        self.leftVoltage = self.limitVoltage(avgVoltage, 10.0)
        self.rightVoltage = self.limitVoltage(avgVoltage, 10.0)

        if self.rightKey.getIsActive(self.timer):
            self.leftVoltage += turnVoltage
            self.rightVoltage -= turnVoltage
        elif self.leftKey.getIsActive(self.timer):
            self.leftVoltage -= turnVoltage
            self.rightVoltage += turnVoltage
        print(self.robot.center.velocity)

    def limitVoltage(self, voltage, max):
        if voltage > max:
            voltage = max
        elif voltage < -max:
            voltage = -max
        return voltage

    def redrawAll(self, canvas):
        canvas.create_image(self.width/2, self.height/2,
                            image=self.fieldImageScaled)
        robotAppX, robotAppY = self.realWorldToAppCoords(
            self.robot.center.x, self.robot.center.y)
        r = 30
        rotatedRobot = self._robotImage.rotate(-self.robot.center.heading)
        canvas.create_image(robotAppX, robotAppY,
                            image=ImageTk.PhotoImage(rotatedRobot))

        r = self.waypointRadius
        i = 0
        for waypoint in self.waypoints:
            x, y = self.realWorldToAppCoords(waypoint.x, waypoint.y)
            canvas.create_oval(x+r, y+r,
                               x-r, y-r,
                               fill="yellow")
            canvas.create_text(x, y, anchor="c", text=f"{i}")
            i += 1

    def keyPressed(self, event):
        key = event.key
        if key == "Up":
            self.upKey.lastEventRelease = False
        elif key == "Down":
            self.downKey.lastEventRelease = False
        elif key == "Right":
            self.rightKey.lastEventRelease = False
        elif key == "Left":
            self.leftKey.lastEventRelease = False
        else:
            None

    def keyReleased(self, event):
        key = event.key
        if key == "Up":
            self.upKey.lastEventRelease = True
            self.upKey.timeLastRelease = self.timer
        elif key == "Down":
            self.downKey.lastEventRelease = True
            self.downKey.timeLastRelease = self.timer
        elif key == "Right":
            self.rightKey.lastEventRelease = True
            self.rightKey.timeLastRelease = self.timer
        elif key == "Left":
            self.leftKey.lastEventRelease = True
            self.leftKey.timeLastRelease = self.timer
        else:
            None

    def mousePressed(self, event):
        for waypoint in self.waypoints:
            appWaypointX, appWaypointY = self.realWorldToAppCoords(
                waypoint.x, waypoint.y)
            if Utils.distance(appWaypointX, appWaypointY, event.x, event.y) < self.waypointRadius:
                self.selectedWaypoint = waypoint
                self.cursorX, self.cursorY = event.x, event.y

        if self.selectedWaypoint is None:
            x, y = self.appToRealWorldCoords(event.x, event.y)
            newWaypoint = Waypoint(x, y)
            self.waypoints.append(newWaypoint)

    def mouseDragged(self, event):
        dX = event.x - self.cursorX
        dY = event.y - self.cursorY
        if self.selectedWaypoint is not None:
            appWaypointX, appWaypointY = self.realWorldToAppCoords(
                self.selectedWaypoint.x, self.selectedWaypoint.y)
            appWaypointX += dX
            appWaypointY += dY
            waypointX, waypointY = self.appToRealWorldCoords(
                appWaypointX, appWaypointY)
            self.selectedWaypoint.x, self.selectedWaypoint.y = waypointX, waypointY
        self.cursorX, self.cursorY = event.x, event.y

    def mouseReleased(self, event):
        self.selectedWaypoint = None

    def realWorldToAppCoords(self, x, y):
        newX = (self.width/2) + (self.width/self.FIELD_REAL_WIDTH*x)
        newY = (self.height) - (self.height/self.FIELD_REAL_HEIGHT*y)
        return int(newX), int(newY)

    def appToRealWorldCoords(self, x, y):
        newX = (x - self.width/2) / (self.width/self.FIELD_REAL_WIDTH)
        newY = (self.height - y) / (self.height/self.FIELD_REAL_HEIGHT)
        return newX, newY

    def setAppDims(self):
        root = self._root
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        imageWidth, imageHeight = self._fieldImage.size
        if screenHeight/imageHeight < screenWidth/imageWidth:
            scaleFactor = screenHeight/imageHeight*0.9
        else:
            scaleFactor = screenWidth/imageWidth*0.9

        self.height = int(imageHeight * scaleFactor)
        self.width = int(imageWidth * scaleFactor)
        self.sizeChanged()
        scaledFieldImage = self.scaleImage(self._fieldImage, scaleFactor)
        self.fieldImageScaled = ImageTk.PhotoImage(scaledFieldImage)


class Waypoint():

    def __init__(self, x, y):
        self.x = x
        self.y = y


class KeyLatch():

    def __init__(self, delay):
        self.timeLastRelease = -delay
        self.delay = delay
        self.lastEventRelease = True

    def getIsActive(self, time):
        if self.lastEventRelease == False:
            return True
        else:
            if time - self.timeLastRelease < self.delay:
                return True
            else:
                return False


if __name__ == "__main__":
    SimulationApp(width=1758, height=1944)
