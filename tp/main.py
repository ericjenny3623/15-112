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

        self.robot = RobotModel(1.0, 1.0, 0.0)
        self._robotImage = self.scaleImage(self.loadImage("steve.jpg"), 0.6)
        self.leftVoltage, self.rightVoltage = 0.0, 0.0
        self.forwardVoltage, self.turnVotlage = 0.0, 0.0

        self.waypoints = []
        self.waypointRadius = 30
        self.selectedWaypoint = None
        self.rotatingWaypoint = False

        self.timerDelay = 30  # milliseconds
        self.timer = 0
        self.releaseDelay = 0.1
        self.inputKeys = {"Up": KeyLatch(self.releaseDelay),
                          "Down": KeyLatch(self.releaseDelay),
                          "Right": KeyLatch(self.releaseDelay),
                          "Left": KeyLatch(self.releaseDelay)}


    def timerFired(self):
        deltaTime = self.timerDelay/1000.0
        self.timer += deltaTime
        self.robot.updateVoltage(
            self.leftVoltage, self.rightVoltage, deltaTime)
        self.robot.updatePositionWithVelocity(deltaTime)

        self.driveUsingKeys()


    def driveUsingKeys(self):
        avgVoltage = (self.leftVoltage + self.rightVoltage) / 2.0
        turnVoltage = 2.0
        if self.inputKeys["Up"].getIsActive(self.timer):
            avgVoltage += 0.9
        elif self.inputKeys["Down"].getIsActive(self.timer):
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

        self.leftVoltage = Utils.limit(avgVoltage, 10.0, -10.0)
        self.rightVoltage = Utils.limit(avgVoltage, 10.0, -10.0)

        if self.inputKeys["Right"].getIsActive(self.timer):
            self.leftVoltage += turnVoltage
            self.rightVoltage -= turnVoltage
        elif self.inputKeys["Left"].getIsActive(self.timer):
            self.leftVoltage -= turnVoltage
            self.rightVoltage += turnVoltage



    def redrawAll(self, canvas):
        canvas.create_image(self.width/2, self.height/2,
                            image=self.fieldImageScaled)
        robotAppX, robotAppY = self.realWorldToAppCoords(
            self.robot.center.x, self.robot.center.y)
        rotatedRobot = self._robotImage.rotate(-self.robot.center.heading)
        canvas.create_image(robotAppX, robotAppY,
                            image=ImageTk.PhotoImage(rotatedRobot))

        for i, waypoint in enumerate(self.waypoints):
            self.drawNode(canvas, waypoint, i)


    def keyPressed(self, event):
        key = event.key
        if key in self.inputKeys:
            self.inputKeys[key].lastEventRelease = False
        elif key == "Delete":
            if self.selectedWaypoint is not None:
                self.waypoints.remove(self.selectedWaypoint)
                self.selectedWaypoint = None
        else:
            None

    def keyReleased(self, event):
        key = event.key
        if key in self.inputKeys:
            self.inputKeys[key].lastEventRelease = True
            self.inputKeys[key].timeLastRelease = self.timer
        else:
            None

    def mousePressed(self, event):
        self.cursorX, self.cursorY = event.x, event.y
        self.selectedWaypoint = None
        for waypoint in self.waypoints:
            appWaypointX, appWaypointY = self.realWorldToAppCoords(
                waypoint.x, waypoint.y)
            if Utils.distance(appWaypointX, appWaypointY, event.x, event.y) < self.waypointRadius:
                self.selectedWaypoint = waypoint
                newAngle = math.degrees(-math.atan2(appWaypointX - event.x,
                                        appWaypointY - event.y))
                if abs(newAngle - self.selectedWaypoint.heading) < 30.0:
                    self.rotatingWaypoint = True
                else:
                    self.rotatingWaypoint = False

        if self.selectedWaypoint is None: # New waypoint
            x, y = self.appToRealWorldCoords(event.x, event.y)
            newWaypoint = Waypoint(x, y, 0.0)
            self.waypoints.append(newWaypoint)

    def mouseDragged(self, event):
        dX = event.x - self.cursorX
        dY = event.y - self.cursorY
        if self.selectedWaypoint is not None:
            appWaypointX, appWaypointY = self.realWorldToAppCoords(
                self.selectedWaypoint.x, self.selectedWaypoint.y)
            if self.rotatingWaypoint:
                newAngle = math.degrees(-math.atan2(appWaypointX - event.x,
                                                    appWaypointY - event.y))
                self.selectedWaypoint.setPosition(heading=newAngle)
            else:
                appWaypointX += dX
                appWaypointY += dY
                waypointX, waypointY = self.appToRealWorldCoords(
                    appWaypointX, appWaypointY)
                self.selectedWaypoint.x, self.selectedWaypoint.y = waypointX, waypointY
        self.cursorX, self.cursorY = event.x, event.y

    def mouseReleased(self, event):
        None

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

    def drawNode(self, canvas, node, i):
        r = self.waypointRadius
        x, y = self.realWorldToAppCoords(node.x, node.y)
        canvas.create_oval(x+r, y+r,
                            x-r, y-r,
                            fill="yellow")
        x1 = x + (r * 1.3 * math.sin(node.r))
        y1 = y - (r * 1.3 * math.cos(node.r))
        canvas.create_line(x, y, x1, y1, width=r/3, fill="gold")
        canvas.create_text(x, y, anchor="c", text=f"{i}")





class Waypoint(Utils.Twist):

    def __init__(self, x, y, heading):
        super().__init__(x, y, heading)



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
