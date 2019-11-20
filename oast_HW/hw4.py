#################################################
# hw4.py
#
# Your name: Eric Jenny
# Your andrew id: ejenny
#################################################


import decimal
import cs112_f19_week4_linter
import math
import copy

#################################################
# Helper functions
#################################################


def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)


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
# bestScrabbleScore
#################################################


def bestScrabbleScore(dictionary, letterScores, hand):
    scores = [] # list where each element i has the score of
                # the corresponding ith element in dictionary
    for word in dictionary: # checks scores for each word
        legalWord = checkWord(word, hand)
        if not legalWord: # illegal words have score of 0
            scores.append(0)
        else:
            scores.append(getScore(word, letterScores))

    maxScore = 0 # if no words are legal maxScore will remain at 0
    maxes = [] # words with the current max score
    i = 0 # used to keep track of the word corresponding with score
    for score in scores:
        if score > maxScore: # new max, reset the maxes
            maxScore = score
            maxes = [dictionary[i]]
        elif score == maxScore: # duplicate max, add to list
            maxes.append(dictionary[i])
        i += 1

    if maxScore == 0:
        return None
    elif len(maxes) > 1:
        return (maxes, maxScore)
    else:
        return (maxes[0], maxScore)

    return 42


def checkWord(word, hand):
    """
    Checks each character in a word against a list of characters ('hand').
    Each character in the hand can only be used once so it is removed
    after being checked.
    Returns false if there is not a unique character in 'hand' for every
    character in 'word'.
    """
    copy = hand[:]
    for c in word:
        if c in copy:
            copy.remove(c)
        else:
            return False
    return True


def getScore(word, letterScores):
    """
    Checks the score of a word given a list defining the score for each letter
    a-z (by corresponding index 0-25).
    """
    score = 0
    aIndex = ord('a')
    for c in word:
        index = ord(c) - aIndex
        score += letterScores[index]
    return score


#################################################
# Person class
#################################################

class Person(object):

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.friends = None

    def addFriend(self, friend):
        """
        Adds a friend to this instances list of friends, if the new friend
        is not already in the list and is not this instance.
        """
        if self.friends is None:
            self.friends = [friend]
        elif friend in self.friends or friend is self:
            pass
        else:
            self.friends.append(friend)

    def getName(self):
        """ Returns this instances name, a string
        """
        return self.name

    def getAge(self):
        """ Returns this instances name, an int
        """
        return self.age

    def getFriends(self):
        """ Returns this instances friends, a list of other unique
        person objects.
        """
        return self.friends

    pass

#################################################
# playMyTextAdventureGame
#################################################
################################################################################
"""
1. If kitchen is a Room instance, what is kitchen.exits[2]?
    - east
2. When we call room.setExit('South', otherRoom), how does the setExit method
  convert the direction name 'South' into the index 1?
    - setExit calls getDirection(South) which returns 1 through the elif block
3. Say we did not include the last line of the Room constructor, the one that
  sets self.items = [ ]. Eventually, our code would crash. What player action
  would make the code crash, and what precise Python error would we get?
    - It would break on the first refernce to a rooms .items object, which is at
      line 201 where the code tries to append a pitcher to the non-existent
      kitchen.items list and therefore crashes on "'Room' object has no
      attribute 'items'"
4. Why does room.getAvailableDirNames use the string join method?
    - to easily convert the list of human intended direction names to a comma
      separated human intended output to be printed to the user
5. What is the difference between an item's name and its shortName?
    - The shortName is used in the code as a unique identifier for an item type.
      item.name is used for a human inteded description of the item.
6. What is game.inventory?
    - The items the players "person" is carrying
7. Why does game.getCommand use the string split method?
    - to break the command into a list with the "verb" and "noun" of the command
8. How are we able to use game.findItem from both game.doGet (where we look
  through the items in the current room) and also in game.doPut (where we look
  through the items in the player's inventory)?
    - findItem is passed the list of items to look through and so this is
      different between the findItem calls from doGet and doPut
9. In this version of the game, the player cannot carry more than 2 items. In
  which method is this enforced, and precisely how is it enforced?
    - in doGet, if the length of invertory (equivalent to number of items
      carried) is equal to 2, the item is not added to the inventory
10. How does game.doDrink tell if the glass is full or not?
    - doDrink checks glass.name to see if the word 'full' is in it
"""

class Room(object):
    def __init__(self,
                 name, minAppetite,
                 thoughts="eh", enviHunger=0,
                 person="Do not eat here", askHunger=0):
        self.name = name
        self.exits = []
        self.items = []
        self.minAppetite = minAppetite
        self.recommendation = person
        self.recommendationHungerEffect = askHunger
        self.thoughts = thoughts
        self.environmentHungerEffect = enviHunger

    def setExit(self, direction, room):
        self.exits.append((direction.lower(), room))

    def getExit(self, dirName):
        dirName = dirName.lower()
        for exitRoom in self.exits:
            if dirName in exitRoom[0]:
                return exitRoom[1]
        return None

    def getAvailableDirNames(self):
        availableDirections = []
        for exitRoom in self.exits:
            availableDirections.append(f"{exitRoom[1].name} ({exitRoom[0]})")
        if (availableDirections == []):
            return 'You are very stuck and cannot go anywhere'
        else:
            return ', '.join(availableDirections)


# adapted from simple-text-adventure-game.py
class Game(object):
    def __init__(self, name, goal, startingRoom):
        self.name = name
        self.goal = goal
        self.room = startingRoom
        self.commandCounter = 0
        self.hunger = 0
        self.gameOver = False

    def getCommand(self):
        self.commandCounter += 1
        response = input(f'[{self.commandCounter}] Your command --> ')
        print()
        if (response == ''):
            response = 'help'
        responseParts = response.split(' ')
        command = responseParts[0]
        target = '' if (len(responseParts) == 1) else responseParts[1]
        return command, target

    def play(self):
        print(f'Welcome to {self.name}!')
        print(f'Your goal: {self.goal}!')
        print('Just press enter for help.')
        while (not self.gameOver):
            self.doLook()
            command, target = self.getCommand()
            if (command == 'help'):
                self.doHelp()
            elif (command == "superhelp"):
                self.doSuperHelp()
            elif (command == 'look'):
                self.doLook()
            elif (command == 'go'):
                self.doGo(target)
            elif (command == "quit"):
                self.gameOver = True
            elif (command == "order"):
                self.doEat()
            elif (command == "use-phone"):
                self.doEat(True)
            elif (command == "ask"):
                self.doAskPerson()
            else:
                print(f'Unknown command: {command}. Enter "help" for help.')
        print('Goodbye!')

    def doHelp(self):
        print('''
Welcome to this terrible game!  Here are some commands I know:
    help (print this message)
    look (see what's around you)
    go [direction]
    order
    ask rando
    quit
Have fun!''')

    def doSuperHelp(self):
        print("""
You enter the building with a hunger of 0.
In order to eat, the min appetite of the place you order (command 'order')
must be less than your current appetite (hunger).
As you enter places your appetite will change.
You can ask people too (command 'ask') but be careful because most
reviews make you want to eat less.
Your best bet is to wander to and from places that increase your hunger until
you give up, but asking some rando in one place will tell you a cheat code
to actually eat food...
        """)

    def doLook(self):
        print(
            f'''\nYou are in the {self.room.name.lower()}
 and have a hunger of {self.hunger}''')
        print(
            f'You can go to these places: {self.room.getAvailableDirNames()}')
        print(f"You are thinking '{self.room.thoughts}'")
        print()

    def doGo(self, dirName):
        newRoom = self.room.getExit(dirName)
        if (newRoom == None):
            print(f'Sorry, I cannot go {dirName}.')
        else:
            self.room = newRoom
            self.hunger += self.room.environmentHungerEffect

    def doAskPerson(self):
        print(self.room.recommendation)
        self.hunger += self.room.recommendationHungerEffect

    def doEat(self, uberEats=False):
        if uberEats:
            print("Congrats, you got actual food")
            self.gameOver = True
        elif self.hunger > self.room.minAppetite:
            print("I guess this is a win, you ate!")
            self.gameOver = True
        else:
            print("You are not good enough to eat at a place this bad :(")
            self.hunger -= 4


def playMyTextAdventureGame():
    # Make the Rooms
    entrance = Room('Entrance', 1000,
                    "What are you gonna eat, napkins like Terry?", 0,
                    "Resnik is nasty bro", 0)
    cafe = Room('Resnik Cafe', 25,
                """This looks pretty cool and that smell of fried food
                is appetizing.""", 3,
                "I ordered 50 minutes ago and Im still waiting.", -1)
    innovation = Room('Innovation Kitchen', 40,
                      "Maybe I should eat healty today", 1,
                      "Holy shit the steak is dry.", -2)
    india = Room('Taste of India', 35,
                 "Damn I havent had spices or flavor since getting to CMU", 3,
                 """"It tastes good and one and a half pounds is basically
                 five, but it comes straight out right after. """, -2)
    eatingArea = Room('Sitting Area', 1000,
                      "These tables and kinda greasy", -1,
                      "Dude I loveeee the smell of chese", -2)
    pizza = Room('Generic Pizza Place', 60,
                 "Is pizza ever bad?", 1,
                 """I swear I have seen that same slice of pizza out for 3
                 days now""", -3)
    bathroom = Room("Bathrooms", 10000000,
                    "WHAT THE HELL DID I JUST WALK INTO", -5,
                    "Just uber eats with command 'use-phone'", -2)

    # Make the map (note: it need not be physically possible)
    entrance.setExit('North', eatingArea)
    entrance.setExit('East', cafe)
    entrance.setExit('West', innovation)
    innovation.setExit('East', entrance)
    innovation.setExit('West', india)
    india.setExit('East', innovation)
    cafe.setExit('West', entrance)
    cafe.setExit('North', eatingArea)
    eatingArea.setExit('Down', bathroom)
    eatingArea.setExit('South', entrance)
    eatingArea.setExit('West', pizza)
    pizza.setExit('East', eatingArea)
    bathroom.setExit('Up', eatingArea)

    # Make the game and play it
    game = Game('the Find Food in Resnik game',
                'eat food',
                entrance)
    game.play()


#################################################
# bonus: linearRegression
#################################################


def linearRegression(pointsList):
    return 42

#################################################
# bonus: runSimpleProgram
#################################################


def runSimpleProgram(program, args):
    return 42

#################################################
# Test Functions
#################################################


def testBestScrabbleScore():
    print("Testing bestScrabbleScore()...", end="")
    def dictionary1(): return ["a", "b", "c"]
    def letterScores1(): return [1] * 26
    def dictionary2(): return ["xyz", "zxy", "zzy", "yy", "yx", "wow"]
    def letterScores2(): return [1+(i % 5) for i in range(26)]
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("b")) ==
           ("b", 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("ace")) ==
           (["a", "c"], 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("b")) ==
           ("b", 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("z")) ==
           None)
    # x = 4, y = 5, z = 1
    # ["xyz", "zxy", "zzy", "yy", "yx", "wow"]
    #    10     10     7     10    9      -
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyz")) ==
           (["xyz", "zxy"], 10))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyzy")) ==
           (["xyz", "zxy", "yy"], 10))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyq")) ==
           ("yx", 9))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("yzz")) ==
           ("zzy", 7))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("wxz")) ==
           None)
    print("Passed!")


def testPersonClass():
    print('Testing Person Class...', end='')
    fred = Person('fred', 32)
    assert(isinstance(fred, Person))
    assert(fred.getName() == 'fred')
    assert(fred.getAge() == 32)
    assert(fred.getFriends() == None)

    wilma = Person('wilma', 35)
    assert(wilma.getName() == 'wilma')
    assert(wilma.getAge() == 35)
    assert(wilma.getFriends() == None)

    wilma.addFriend(fred)
    assert(wilma.getFriends() == [fred])
    assert(fred.getFriends() == None)
    wilma.addFriend(fred)
    assert(wilma.getFriends() == [fred])  # don't add twice!

    barney = Person('barney', 28)
    fred.addFriend(wilma)
    fred.addFriend(barney)
    assert(fred.getFriends() == [wilma, barney])

    fred.addFriend(barney)  # don't add twice
    fred.addFriend(fred)    # ignore self as a friend
    assert(fred.getFriends() == [wilma, barney])
    print('Passed!')


def testPlayMyTextAdventureGame():
    print('***************************************************')
    print('Testing playMyTextAdventureGame()...')
    print('This requires manual testing, so we will just run the game:')
    print('***************************************************')
    playMyTextAdventureGame()
    print('***************************************************')


def relaxedAlmostEqual(d1, d2):
    epsilon = 10**-3  # really loose here
    return abs(d1 - d2) < epsilon


def tuplesAlmostEqual(t1, t2):
    if (len(t1) != len(t2)):
        return False
    for i in range(len(t1)):
        if (not relaxedAlmostEqual(t1[i], t2[i])):
            return False
    return True


def testBonusLinearRegression():
    print("Testing bonus problem linearRegression()...", end="")

    ans = linearRegression([(1, 3), (2, 5), (4, 8)])
    target = (1.6429, 1.5, .9972)
    assert(tuplesAlmostEqual(ans, target))

    ans = linearRegression([(0, 0), (1, 2), (3, 4)])
    target = ((9.0/7), (2.0/7), .9819805061)
    assert(tuplesAlmostEqual(ans, target))

    # perfect lines
    ans = linearRegression([(1, 1), (2, 2), (3, 3)])
    target = (1.0, 0.0, 1.0)
    assert(tuplesAlmostEqual(ans, target))

    ans = linearRegression([(0, 1), (-1, -1)])
    target = (2.0, 1.0, 1.0)
    assert(tuplesAlmostEqual(ans, target))

    # horizontal lines
    ans = linearRegression([(1, 0), (2, 0), (3, 0)])
    target = (0.0, 0.0, 1.0)
    assert(tuplesAlmostEqual(ans, target))

    ans = linearRegression([(1, 1), (2, 1), (-1, 1)])
    target = (0.0, 1.0, 1.0)
    assert(tuplesAlmostEqual(ans, target))
    print("Passed!")


def testBonusRunSimpleProgram():
    print("Testing bonus problem runSimpleProgram()...", end="")
    largest = """! largest: Returns max(A0, A1)
                   L0 - A0 A1
                   JMP+ L0 a0
                   RTN A1
                   a0:
                   RTN A0"""
    assert(runSimpleProgram(largest, [5, 6]) == 6)
    assert(runSimpleProgram(largest, [6, 5]) == 6)

    sumToN = """! SumToN: Returns 1 + ... + A0
                ! L0 is a counter, L1 is the result
                L0 0
                L1 0
                loop:
                L2 - L0 A0
                JMP0 L2 done
                L0 + L0 1
                L1 + L1 L0
                JMP loop
                done:
                RTN L1"""
    assert(runSimpleProgram(sumToN, [5]) == 1+2+3+4+5)
    assert(runSimpleProgram(sumToN, [10]) == 10*11//2)
    print("Passed!")

#################################################
# testAll and main
#################################################


def testAll():
    testBestScrabbleScore()
    testPersonClass()
    testPlayMyTextAdventureGame()
    # testBonusLinearRegression()
    # testBonusRunSimpleProgram()


def main():
    cs112_f19_week4_linter.lint()
    testAll()


if __name__ == '__main__':
    main()
