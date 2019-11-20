import Utils
import math


class RobotModel():

    def __init__(self, x, y):
        self.center = Utils.Twist(x, y, 0.0)
        self.leftSide, self.rightSide = self.DrivetrainSide(), self.DrivetrainSide()
        self.WHEEL_BASE = 0.67  # Meters

    def setPosition(self, x, y, heading):
        self.x, self.y, self.heading = x, y, heading

    def zero(self):
        self.leftSide.velocity = 0.0
        self.leftSide.acceleration = 0.0
        self.rightSide.velocity = 0.0
        self.rightSide.acceleration = 0.0

    def updateVoltage(self, leftVoltage, rightVoltage, time):
        self.leftSide.updateVoltage(leftVoltage, time)
        self.rightSide.updateVoltage(rightVoltage, time)

    def updatePositionWithVelocity(self, deltaTime):
        if self.leftSide.velocity != self.rightSide.velocity:
            radius = self.radiusICC(
                self.WHEEL_BASE, self.leftSide.velocity, self.rightSide.velocity)
            omega = self.velocityICC(
                self.WHEEL_BASE, self.leftSide.velocity, self.rightSide.velocity)
            theta = omega * (deltaTime)
            sinTheta = math.sin(theta)
            alpha = ((math.pi) - theta) / 2.0
            sinAlpha = math.sin(alpha)

            movement = Utils.sideFromLawOfSines(radius, sinAlpha, sinTheta)
        else:
            omega, theta = 0.0, 0.0
            movement = -(self.leftSide.velocity +
                         self.rightSide.velocity) / 2.0 * deltaTime

        movementAngle = self.center.r + theta
        sine = math.sin(movementAngle)
        cosine = math.cos(movementAngle)
        movementX = -movement * sine
        movementY = -movement * cosine
        self.center.updateDeltas(movementX, movementY, deltaR=-theta)

        self.center.velocity = (
            self.leftSide.velocity + self.rightSide.velocity) / 2.0
        self.center.angularVelocity = -math.degrees(theta) / deltaTime

        # print(self.leftSide.velocity, self.rightSide.velocity)

    def radiusICC(self, wheelBase, left, right):
        return -(wheelBase / 2) * (left + right) / (right - left)

    def velocityICC(self, wheelBase, left, right):
        return (right - left) / wheelBase

    class DrivetrainSide():

        def __init__(self):
            self.acceleration, self.velocity = 0.0, 0.0
            self.coast = False
            self.DRIVETRAIN_FRICTION = 115  # Newtons
            self.GEAR_RATIO = 10.75 / 1.0  # Motor to wheel output ratio
            self.WHEEL_RADIUS = 0.0774  # Meters
            self.PSUEDO_MASS = 30  # kg
            self.motors = [CIMMotor(), CIMMotor()]

        def updateSpeed(self, newVel, time):
            deltaVelocity = self.velocity - newVel
            self.acceleration = deltaVelocity / time
            self.velocity = newVel

        def updateVoltage(self, voltage, time):
            motorSpeed = self.wheelSpeedToMotorSpeed(self.velocity)
            totalTorque = 0.0
            for motor in self.motors:
                totalTorque += motor.outputTorque(voltage,
                                                  motorSpeed) * self.GEAR_RATIO

            if self.coast and Utils.withinThreshold(voltage, 0.0, 0.05):
                totalTorque = 0.0

            wheelGrossForce = totalTorque / self.WHEEL_RADIUS

            wheelNetForce = self.frictionModel(wheelGrossForce, self.velocity)
            wheelGroundForce = self.tractionModel(wheelNetForce)

            # This should be rotational inertia, but this is decent for now
            newAcceleration = wheelGroundForce / self.PSUEDO_MASS
            # Trapezoidal integration
            self.velocity += (newAcceleration + self.acceleration) / 2 * time
            self.acceleration = newAcceleration

        def frictionModel(self, force, speed):
            if speed == 0.0:
                netForce = force
            elif speed < 0.0:
                netForce = force + self.DRIVETRAIN_FRICTION
            elif speed > 0.0:
                netForce = force - self.DRIVETRAIN_FRICTION
            else:
                netForce = 0.0
            return netForce

        def tractionModel(self, force):
            staticTraction = self.PSUEDO_MASS*1.3*9.8
            kineticTraction = self.PSUEDO_MASS*0.5*9.8
            if force > staticTraction:
                force = kineticTraction
            elif force < -staticTraction:
                force = -kineticTraction
            return force

        def wheelSpeedToMotorSpeed(self, speed):
            wheelCircum = self.WHEEL_RADIUS * 2 * math.pi
            wheelRevs = speed / wheelCircum * 60.0
            motorRevs = wheelRevs * self.GEAR_RATIO
            return motorRevs


class Motor():

    def __init__(self, stallTorque, freeSpeed, stallCurrent, freeCurrent):
        self.STALL_TORQUE = stallTorque  # N.m
        self.FREE_SPEED = freeSpeed  # RPM
        self.STALL_CURRENT = stallCurrent  # Amps
        self.FREE_CURRENT = freeCurrent  # Amps
        self.MAX_VOLTAGE = 12.0  # Volts
        self.kSlopeTorque = -self.STALL_TORQUE/self.FREE_SPEED
        self.kSlopeCurrent = -(self.STALL_CURRENT -
                               self.FREE_CURRENT) / self.FREE_SPEED

    def outputTorque(self, voltage, speed):
        stallTorque = self.STALL_TORQUE * (voltage / self.MAX_VOLTAGE)
        torque = (speed * self.kSlopeTorque) + stallTorque
        return torque

    def torqueToVoltage(self, torque, speed):
        return (torque - (speed*self.kSlopeTorque))*self.MAX_VOLTAGE/self.STALL_TORQUE
        # Just solved for voltage using outputTorque equation

    def currentToVoltage(self, current, speed):
        return (current - (speed*self.kSlopeCurrent))*self.MAX_VOLTAGE/self.STALL_CURRENT


class CIMMotor(Motor):

    def __init__(self):
        super().__init__(2.41, 5330, 130.1, 3.8)


cim = CIMMotor()
print(cim.kSlopeTorque)
