#################################################
# hw9.py
#
# Your name: Eric Jenny
# Your andrew id: ejenny
#################################################

import math
from cmu_112_graphics import *
from tkinter import *
import random
import cs112_f19_week9_linter


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


#################################################
# Side Scroller
#################################################

class CollideableImage():
    """ Helper class to keep track of an image with a collision box,
    speed, and an explosion action.
    """

    def __init__(self, sprites, centerX, centerY, dX, dY):
        self.sprites = sprites
        self.spriteIndex = 0
        self.updateBoxSize()
        self.width, self.height = self.getSprite().size
        self.centerX = centerX
        self.centerY = centerY
        self.dX = dX
        self.dY = dY
        self.collided = False
        self.expired = False
        self.updateCount = 0

    def getSprite(self):
        """ Helper function which returns the current sprite of the animation.
        Override based on format of spritesheet
        """
        return self.sprites[self.spriteIndex]

    def updateBoxSize(self):
        """ Sets self.boxWidth and self.boxHeight to the size of the sprite.
        Override by calling super and scaling those values
        """
        self.boxWidth, self.boxHeight = self.getSprite().size

    def update(self):
        """ Called periodically to update the images centerX and centerY.
        """
        self.centerX += self.dX
        self.centerY += self.dY
        self.updateCount += 1

    def checkCollision(self, other):
        """ returns True if there has been collision with other object
        """
        if isinstance(other, CollideableImage):
            if abs(self.centerX-other.centerX) < \
                (self.boxWidth+other.boxWidth)/2 \
               and abs(self.centerY-other.centerY) < \
                    (self.boxHeight+other.boxHeight)/2:
                return True
        else:
            return False

    def getDrawInfo(self):
        """ Returns, centerX, centerY, and image converted to a
        ImageTk PhotoImage
        """
        return self.centerX, self.centerY, ImageTk.PhotoImage(self.getSprite())

    def explode(self):
        """ Essentially abstract function. Override to implement behavior.
        """
        if not self.collided:
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

    def getSprite(self):
        return self.sprites[self.spriteMode][self.spriteIndex]

    def update(self):
        super().update()
        self.spriteIndex += 1

        if (self.collided): # if collided, expire the spaceship after the
                            # animation is complete
            if self.spriteIndex >= Spaceship.numSprites:
                self.expired = True
                self.spriteIndex = Spaceship.numSprites - 1

        if self.spriteIndex >= Spaceship.numSprites:
            self.spriteIndex = 0

    def updateBoxSize(self):
        super().updateBoxSize()
        self.boxWidth *= self.boxXScale
        self.boxHeight *= self.boxYScale

    def fireLaser(self, container):
        """ Adds a new projectile object with this spaceship's
        projectile properties to given container
        """
        laser = Projectile(self.projectile,
                           self.centerX, self.centerY,
                           self.dX+self.projectileSpeed+self.dX, 0,
                           self.projectileRange)
        container.append(laser)

    def explode(self):
        if not self.collided:
            self.collided = True
            self.spriteIndex = 0
            self.spriteMode = 1


class Alienship(Spaceship):
    url = "https://i.imgur.com/lCRRDCr.png"

    def __init__(self, sprites, centerX, centerY, dX, dY,
                 projectile, fireInterval, objectID,
                 projectileSpeed=25, projectileRange=1000):
        super().__init__(sprites, centerX, centerY, dX, dY, projectile)
        self.fireInterval = fireInterval

    def checkFire(self):
        """ Called by parent class to check whether enough updates have
        occured to fire again
        """
        return self.updateCount % self.fireInterval == 0

    def __hash__(self):
        return hash(f"Alien{self.objectID}")


class SpaceGame(Mode):

    def appStarted(self):
        self.scroll = 0
        self.scrollSpeed = 10
        self.loadImages()
        return super().appStarted()

    def timerFired(self):
        self.scroll += self.scrollSpeed

        if self.bX1 + (self.bWidth/2) < self.scroll - self.width:
            self.bX1 = self.bX2 + self.bWidth
        if self.bX2 + (self.bWidth/2) < self.scroll - self.width:
            self.bX2 = self.bX1 + self.bWidth

    def redrawAll(self, canvas):
        canvas.create_image(self.bX1-self.scroll,
                            self.bY, image=self.background)
        canvas.create_image(self.bX2-self.scroll,
                            self.bY, image=self.background)

    def loadImages(self):
        self.loadBackground()
        self.loadCursor()

    def loadSpaceShip(self, typeSpaceship):
        """ Loads spaceship image from given class of spaceships url.
        Spaceships have two rows, the top row being the normal flying mode,
        and bottom being the explosion animation mode.
        """
        url = typeSpaceship.url
        sprites = []
        startX, startY, width, height = typeSpaceship.spriteDims
        spriteStrip = self.loadImage(url)
        for mode in range(typeSpaceship.modes):
            modeSprites = []
            for i in range(typeSpaceship.numSprites):
                sprite = spriteStrip.crop((startX+(width*i),
                                           startY+(mode*height),
                                           startX+(width*(i+1)),
                                           startY+((mode+1)*height)))
                modeSprites.append(sprite)
            sprites.append(modeSprites)
        return sprites

    def loadBackground(self):
        """ Loads background image and sets the two background scrolling
        x variables to init values.
        """
        url = "https://i.imgur.com/kpiz17a.gif"
        backgroundImage = self.loadImage(url)
        self.bWidth = backgroundImage.size[0]
        self.background = ImageTk.PhotoImage(backgroundImage)
        self.bX1 = self.bWidth/2
        self.bX2 = self.bWidth/2*3
        self.bY = self.height/2

    def loadCursor(self):
        """ Loads cursor image and sets position to the middle of the screen.
        """
        url = "https://i.imgur.com/Kqt3rsP.png"
        self.cursor = ImageTk.PhotoImage(self.loadImage(url))
        self.cursorX = self.width/2
        self.cursorY = self.height/2


class SplashScreenMode(SpaceGame, Mode):

    def appStarted(self):
        super().appStarted()

    def redrawAll(self, canvas):
        super().redrawAll(canvas)
        font = 'Arial 26 bold'
        canvas.create_text(self.width/2, 150, font=font, fill="yellow",
                           text='Welcome to Space Game!')
        font = "Arial 15 bold"
        canvas.create_text(self.width/2, 250, font=font, fill="yellow",
                           text='Press any key for the game!',)

    def keyPressed(self, event):
        self.app.setActiveMode(self.app.gameMode)


class GameMode(SpaceGame, Mode):
    def appStarted(self):
        super().appStarted()
        self.score = 0
        self.gameOver = False
        self.levelInterval = 10
        self.spawnInterval = 400
        self.fireInterval = 20
        self.spaceship = Spaceship(self.loadSpaceShip(Spaceship),
                                   0, self.height/2,
                                   self.scrollSpeed, 0,
                                   self.loadImage(Projectile.blueLaserURL))
        self.spaceship.centerX = self.spaceship.width
        self.enemySpaceShip = self.loadSpaceShip(Alienship)
        self.spaceshipLasers = []
        self.enemyEntities = []
        self.enemyProjectiles = []
        self.objectID = 0

    def timerFired(self):
        super().timerFired()

        self.spaceship.update()
        for laser in self.spaceshipLasers:
            laser.update()
            if laser.expired:
                self.spaceshipLasers.remove(laser)

        for enemyLaser in self.enemyProjectiles:
            enemyLaser.update()
            if enemyLaser.expired:
                self.enemyProjectiles.remove(enemyLaser)
            if self.spaceship.checkCollision(enemyLaser):
                self.gameOver = True
                enemyLaser.expired = True
                self.spaceship.explode()

        for alien in self.enemyEntities:
            alien.update()
            if alien.expired:
                self.enemyEntities.remove(alien)
                continue
            elif alien.collided:
                continue

            if self.spaceship.checkCollision(alien):
                self.gameOver = True
                newSpeed = self.spaceship.dX + alien.dX
                self.spaceship.dX = newSpeed
                alien.dX = newSpeed
                alien.explode()
                self.spaceship.explode()
            for laser in self.spaceshipLasers:
                if alien.checkCollision(laser):
                    self.spaceshipLasers.remove(laser)
                    alien.explode()
                    self.score += 1
            if alien.checkFire():
                alien.fireLaser(self.enemyProjectiles)
            if alien.centerX < self.scroll:
                self.gameOver = True
            elif alien.centerX + alien.boxWidth < self.scroll:
                self.enemyEntities.remove(alien)

        if self.scroll % self.spawnInterval == 0:
            for x in range(self.score//self.levelInterval + 1):
                self.spawnEnemy()

    def mousePressed(self, event):
        print(event.y)
        self.cursorY0 = event.y

    def mouseDragged(self, event):
        self.bY += (event.y - self.cursorY0)
        self.cursorY0 = event.y
        print(f'mouseDragged at {(event.x, event.y)}', self.bY)


    def mouseMoved(self, event):
        self.cursorX = event.x
        self.cursorY = event.y
        self.spaceship.centerY = event.y

    def keyPressed(self, event):
        key = event.key
        if (key == 'h'):
            self.app.setActiveMode(self.app.helpMode)
        elif key == "Space":
            self.spaceship.fireLaser(self.spaceshipLasers)
        elif key == "S":
            self.superhelp()
        else:
            None

        self.checkBounds()

    def checkBounds(self):
        if self.spaceship.centerY < 0:
            self.spaceship.centerY = 0
        elif self.spaceship.centerY > self.height:
            self.spaceship.centerY = self.height

    def redrawAll(self, canvas):
        super().redrawAll(canvas)
        self.drawAllEntities(canvas, self.spaceshipLasers)
        self.drawAllEntities(canvas, self.enemyProjectiles)
        self.drawAllEntities(canvas, self.enemyEntities)

        x, y, image = self.spaceship.getDrawInfo()
        canvas.create_image(x-self.scroll, y, image=image)

        canvas.create_image(self.cursorX, self.cursorY, image=self.cursor)

        font = 'Arial 26 bold'
        canvas.create_text(0, 0, text=f"Score: {self.score}",
                           anchor="nw", fill="yellow")
        if self.gameOver:
            font = 'Arial 26 bold'
            canvas.create_text(self.width/2, self.height/2,
                               text='Game Over!', font=font, fill="yellow")

    def drawAllEntities(self, canvas, container):
        for entity in container:
            x, y, image = entity.getDrawInfo()
            canvas.create_image(x-self.scroll, y, image=image)

    def spawnEnemy(self):
        alienship = Alienship(self.enemySpaceShip,
                              0, 0,
                              -self.scrollSpeed, 0,
                              self.loadImage(Projectile.redLaserURL),
                              self.fireInterval,
                              self.objectID)
        alienship.centerX = self.width+self.scroll+alienship.width
        alienship.centerY = random.randint(alienship.height/2,
                                           self.height-(alienship.height/2))
        self.objectID += 1
        self.enemyEntities.append(alienship)

    def superhelp(self):
        print("""
        This was originally intended to be a crappy space invader.
        You get points by shooting the spawned enemies using spacebar
        and positioning in front of them using the mouse.
        You die and lose if one of their (red) lasers hits you,
        if you collide with their ship, or if they pass you.
        You can also drag the scrolling background up and down for
        more scenery.
        I have a hash method for the alienships, however I realized
        too late that my current method of looping through a container
        of the alienships and removing some produces an error.
        """)


class HelpMode(SpaceGame, Mode):
    def redrawAll(self, canvas):
        super().redrawAll(canvas)
        font = 'Arial 26 bold'
        canvas.create_text(self.width/2, 150, fill="yellow",
                           font=font, anchor="center",
                           text='Help')
        font = 'Arial 16 bold'
        canvas.create_text(self.width/2, self.height/2, fill="yellow",
                           font=font, anchor="center",
                           text=("Mouse- Spaceship Movement\n"
                                 "Spacebar- Fire\n"
                                 "Enemies are randomly spawned at an\n"
                                 "increasing amount, good luck\n"))
        canvas.create_text(self.width/2, self.height/2+200, fill="yellow",
                           font=font, anchor="center",
                           text='Press any key to return to the game!')

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
    app = MyModalApp(width=1000, height=1000)


def main():
    cs112_f19_week9_linter.lint()
    testBirdClasses()
    runCreativeSidescroller()


if __name__ == "__main__":
    main()
