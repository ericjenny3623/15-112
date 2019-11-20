# adapted from simple-text-adventure-game.py
class Room(object):
    def __init__(self,
                name, minAppetite,
                thoughts="eh", enviHunger=0,
                person="Do not eat here", askHunger = 0):
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
        print(f'\nYou are in the {self.room.name.lower()} and have a hunger of {self.hunger}')
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


def playSimpleGame():
    # Make the Rooms
    entrance = Room('Entrance', 1000,
                    "What are you gonna eat, napkins like Terry?", 0,
                    "Resnik is nasty bro", 0)
    cafe = Room('Resnik Cafe', 25,
                "This looks pretty cool and that smell of fried food is appetizing.", 3,
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
                 "I swear I have seen that same slice of pizza out for 3 days now", -3)
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


playSimpleGame()
