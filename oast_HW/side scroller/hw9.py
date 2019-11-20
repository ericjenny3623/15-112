#################################################
# hw9.py
#
# Your name: Eric Jenny
# Your andrew id: ejenny
#################################################

import math

class Bird():

    def __init__(self, birdName):
        self.name = birdName
        self.eggCount = 0

    def fly(self):
        return "I can fly!"

    def countEggs(self):
        return self.eggCount

    def layEgg(self):
        self.eggCount += 1

    def __repr__(self):
        if self.eggCount == 1:
            eggWord = "egg"
        else:
            eggWord = "eggs"
        return f"{self.name} has {self.eggCount} {eggWord}"

    def __eq__(self, other):
        if isinstance(other, Bird):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    isMigrating = False

    @staticmethod
    def startMigrating():
        Bird.isMigrating = True

    @staticmethod
    def stopMigrating():
        Bird.isMigrating = False


class Penguin(Bird):

    def fly(self):
        return "No flying for me."

    def swim(self):
        return "I can swim!"


class MessengerBird(Bird):

    def __init__(self, birdName, message):
        super().__init__(birdName)
        self.message = message

    def deliverMessage(self):
        return self.message


# ignore_rest (The autograder ignores all code below here)

def getLocalMethods(clss):
    import types
    # This is a helper function for the test function below.
    # It returns a sorted list of the names of the methods
    # defined in a class. It's okay if you don't fully understand it!
    result = []
    for var in clss.__dict__:
        val = clss.__dict__[var]
        if (isinstance(val, types.FunctionType)):
            result.append(var)
    return sorted(result)


def testBirdClasses():
    print("Testing Bird classes...", end="")
    # A basic Bird has a species name, can fly, and can lay eggs
    bird1 = Bird("Parrot")
    assert(type(bird1) == Bird)
    assert(isinstance(bird1, Bird))
    assert(bird1.fly() == "I can fly!")
    assert(bird1.countEggs() == 0)
    assert(str(bird1) == "Parrot has 0 eggs")
    bird1.layEgg()
    assert(bird1.countEggs() == 1)
    assert(str(bird1) == "Parrot has 1 egg")
    bird1.layEgg()
    assert(bird1.countEggs() == 2)
    assert(str(bird1) == "Parrot has 2 eggs")
    tempBird = Bird("Parrot")
    assert(bird1 == tempBird)
    tempBird = Bird("Wren")
    assert(bird1 != tempBird)
    nest = set()
    assert(bird1 not in nest)
    assert(tempBird not in nest)
    nest.add(bird1)
    assert(bird1 in nest)
    assert(tempBird not in nest)
    nest.remove(bird1)
    assert(bird1 not in nest)
    assert(getLocalMethods(Bird) == ['__eq__', '__hash__', '__init__',
                                     '__repr__', 'countEggs',
                                     'fly', 'layEgg'])

    # A Penguin is a Bird that cannot fly, but can swim
    bird2 = Penguin("Emperor Penguin")
    assert(type(bird2) == Penguin)
    assert(isinstance(bird2, Penguin))
    assert(isinstance(bird2, Bird))
    assert(not isinstance(bird1, Penguin))
    assert(bird2.fly() == "No flying for me.")
    assert(bird2.swim() == "I can swim!")
    bird2.layEgg()
    assert(bird2.countEggs() == 1)
    assert(str(bird2) == "Emperor Penguin has 1 egg")
    assert(getLocalMethods(Penguin) == ['fly', 'swim'])

    # A MessengerBird is a Bird that carries a message
    bird3 = MessengerBird("War Pigeon", "Top-Secret Message!")
    assert(type(bird3) == MessengerBird)
    assert(isinstance(bird3, MessengerBird))
    assert(isinstance(bird3, Bird))
    assert(not isinstance(bird3, Penguin))
    assert(not isinstance(bird2, MessengerBird))
    assert(not isinstance(bird1, MessengerBird))
    assert(bird3.deliverMessage() == "Top-Secret Message!")
    assert(str(bird3) == "War Pigeon has 0 eggs")
    assert(bird3.fly() == "I can fly!")

    bird4 = MessengerBird("Homing Pigeon", "")
    assert(bird4.deliverMessage() == "")
    bird4.layEgg()
    assert(bird4.countEggs() == 1)
    assert(getLocalMethods(MessengerBird) == ['__init__', 'deliverMessage'])

    # Note: all birds are migrating or not (together, as one)
    assert(bird1.isMigrating == bird2.isMigrating == bird3.isMigrating == False)
    assert(Bird.isMigrating == False)

    bird1.startMigrating()
    assert(bird1.isMigrating == bird2.isMigrating == bird3.isMigrating == True)
    assert(Bird.isMigrating == True)

    Bird.stopMigrating()
    assert(bird1.isMigrating == bird2.isMigrating == bird3.isMigrating == False)
    assert(Bird.isMigrating == False)
    print("Done!")


testBirdClasses()


#################################################
# Side Scroller
#################################################

from cmu_112_graphics import *
from tkinter import *
import random

class CollideableImage():

    def __init__(self, sprites, centerX, centerY, dX, dY):
        self.sprites = sprites
        self.spriteIndex = 0
        self.updateBoxSize()
        self.centerX = centerX
        self.centerY = centerY
        self.dX = dX
        self.dY = dY
        self.collided = False
        self.expired = False
        self.updateCount = 0

    def getSprite(self):
        return self.sprites[self.spriteIndex]

    def updateBoxSize(self):
        self.boxWidth, self.boxHeight = self.getSprite().size

    def update(self):
        self.centerX += self.dX
        self.centerY += self.dY
        self.updateCount += 1

    def checkCollision(self, other):
        """ returns True if there has been collision and calls explode()
        """
        if isinstance(other, CollideableImage):
            if abs(self.centerX - other.centerX) < (self.boxWidth + other.boxWidth) \
               or abs(self.centerY - other.centerY) < (self.boxHeight + other.boxHeight):
                self.explode()
                return False
        else:
            return False

    def getDrawInfo(self):
        return self.centerX, self.centerY, ImageTk.PhotoImage(self.getSprite())

    def explode(self):
        self.collided = True


class Projectile(CollideableImage):
    blueLaserURL = "https://i.imgur.com/5KC3aJv.png"
    redLaserURL = "https://i.imgur.com/TzaM3lY.png"

    def __init__(self, sprites, centerX, centerY, dX, dY, range):
        super().__init__(sprites, centerX, centerY, dX, dY)
        self.originalX = centerX
        self.range = range

    def update(self):
        super().update()
        if abs(self.originalX-self.centerX) > self.range:
            self.expired = True

    def getSprite(self):
        return self.sprites


class Spaceship(CollideableImage):
    url = "https://i.imgur.com/GgizqEw.png"
    modes = 2
    numSprites = 12
    spriteDims = (0, 0, 192, 192)
    projectileRange = 1000
    boxXScale = 0.5
    boxYScale = 0.9

    def __init__(self, sprites, centerX, centerY, dX, dY,
                 projectile, projectileSpeed=25, projectileRange=1000):
        self.spriteMode = 0
        super().__init__(sprites, centerX, centerY, dX, dY)
        self.projectile = projectile
        self.projectileSpeed = math.copysign(projectileSpeed, dX)
        self.projectileRange = projectileRange
        self.projectiles = []

    def getSprite(self):
        return self.sprites[self.spriteMode][self.spriteIndex]

    def update(self):
        super().update()
        self.spriteIndex += 1

        if (self.collided):
            if self.spriteIndex >= Spaceship.numSprites:
                self.expired = True
                self.spriteIndex = Spaceship.numSprites - 1

        if self.spriteIndex >= Spaceship.numSprites:
            self.spriteIndex = 0

    def fire(self):
        self.projectiles.append(Projectile(self.projectiles,
                                           self.centerX + 50, self.centerY,
                                           self.dX+self.projectileSpeed, 0,
                                           self.projectileRange))

    def fireLaser(self, container):
        laser = Projectile(self.projectile,
                           self.centerX, self.centerY,
                           self.dX+self.projectileSpeed+self.dX, 0,
                           self.projectileRange)
        container.append(laser)

    def explode(self):
        super().explode()
        self.spriteIndex = 0
        self.spriteMode = 1


class Alienship(Spaceship):
    url = "https://i.imgur.com/lCRRDCr.png"

    def __init__(self, sprites, centerX, centerY, dX, dY,
                 projectile, projectileSpeed=25, projectileRange=1000):
        super().__init__(sprites, centerX, centerY, dX, dY, projectile)



class SpaceGame():

    def loadSpaceShip(self, typeSpaceship):
        url = typeSpaceship.url
        sprites = []
        startX, startY, width, height = typeSpaceship.spriteDims
        spriteStrip = self.loadImage(url)
        for mode in range(typeSpaceship.modes):
            modeSprites = []
            for i in range(typeSpaceship.numSprites):
                sprite = spriteStrip.crop((startX+(width*i), startY+(mode*height),
                                          startX+(width*(i+1)), startY+((mode+1)*height)))
                modeSprites.append(sprite)
            sprites.append(modeSprites)
        return sprites


class SplashScreenMode(Mode):

    def appStarted(self):
        super().appStarted()

    def redrawAll(self, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(self.width/2, 150, text='This demos a ModalApp!', font=font)
        canvas.create_text(self.width/2, 200, text='This is a modal splash screen!', font=font)
        canvas.create_text(self.width/2, 250, text='Press any key for the game!', font=font)

    def keyPressed(self, event):
        self.app.setActiveMode(self.app.gameMode)


class GameMode(Mode, SpaceGame):
    def appStarted(self):
        self.score = 0
        self.scrollSpeed = 15
        self.scroll = 0
        self.spaceship = Spaceship(self.loadSpaceShip(Spaceship),
                              self.width/2, self.height/2,
                              self.scrollSpeed, 0,
                              self.loadImage(Projectile.blueLaserURL))
        self.enemySpaceShip = self.loadSpaceShip(Alienship)
        self.spaceshipLasers = []
        self.enemyEntities = []
        self.enemyProjectiles = []

    def timerFired(self):
        self.scroll += self.scrollSpeed

        self.spaceship.update()
        print(self.spaceship.centerX, self.scroll)
        for laser in self.spaceshipLasers:
            laser.update()
            if laser.expired:
                self.spaceshipLasers.remove(laser)

        for laser in self.enemyProjectiles:
            laser.update()
            if laser.expired:
                self.enemyProjectiles.remove(laser)

        for alien in self.enemyEntities:
            alien.update()

    def mousePressed(self, event):
        None

    def keyPressed(self, event):
        key = event.key
        if (key == 'h'):
            self.app.setActiveMode(self.app.helpMode)
        elif key == "Up":
            self.spaceship.centerY += -7
        elif key == "Down":
            self.spaceship.centerY += 7
        elif key == "Space":
            self.spaceship.fireLaser(self.spaceshipLasers)
        elif key == "s":
            self.spawnEnemy()
        elif key == "q":
            self.spaceship.explode()
            for enemy in self.enemyEntities:
                enemy.explode()
        else:
            for enemy in self.enemyEntities:
                enemy.fireLaser(self.enemyProjectiles)


    def redrawAll(self, canvas):
        self.drawAllEntities(canvas, self.spaceshipLasers)
        self.drawAllEntities(canvas, self.enemyProjectiles)
        self.drawAllEntities(canvas, self.enemyEntities)

        x, y, image = self.spaceship.getDrawInfo()
        canvas.create_image(x-self.scroll, y, image=image)

    def drawAllEntities(self, canvas, container):
        for entity in container:
            x, y, image = entity.getDrawInfo()
            canvas.create_image(x-self.scroll, y, image=image)

    def spawnEnemy(self):
        alienship = Alienship(self.enemySpaceShip,
                              self.width/2+self.scroll, self.height/2,
                              -self.scrollSpeed, 0,
                              self.loadImage(Projectile.redLaserURL))
        self.enemyEntities.append(alienship)


class HelpMode(Mode):
    def redrawAll(self, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(self.width/2, 150, text='This is the help screen!', font=font)
        canvas.create_text(self.width/2, 250, text='(Insert helpful message here)', font=font)
        canvas.create_text(self.width/2, 350, text='Press any key to return to the game!', font=font)

    def keyPressed(self, event):
        self.app.setActiveMode(self.app.gameMode)


class MyModalApp(ModalApp):

    def appStarted(self):
        self.splashScreenMode = SplashScreenMode()
        self.gameMode = GameMode()
        self.helpMode = HelpMode()
        self.setActiveMode(self.splashScreenMode)
        self.timerDelay = 50


def runCreativeSidescroller():
    app = MyModalApp(width=2000, height=2000)


runCreativeSidescroller()
