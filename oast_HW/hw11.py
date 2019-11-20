#################################################
# hw11.py
#
# Your name: Eric Jenny
# Your andrew id: ejenny
#
# Your hw11 partner's name:
# Your hw11 partner's andrew id:
#
#################################################

import string
import time
import copy
import cs112_f19_week11_linter
import math, copy
import os

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

def confirmPolicies():
    # Replace each 42 with True or False according to the course policies.
    # If you are unsure, testConfirmPolicies() below contains the answers.
    # This is just to be sure you understand those policies!
    # We very much encourage you to collaborate, but we also want
    # you to do it right.  Be sure both of you are working closely together,
    # and both of you are contributing and learning the material well.
    # Have fun!!!!!
    return  {
    'I can work solo on hw11': True,
    'I can work with one partner on hw11': True,
    ("I must list my hw11 partner's name and andrewId at the top" +
     "of my hw11.py file that I submit"): True,
    'I can switch hw11 partners and then work with a new partner': False,
    'My hw11 partner must be in 112 this semester': True,
    'My hw11 partner must be in the same lecture or section as me': False,
    "I can look at my hw11 partner's code": True,
    "I can copy some of hw11 partner's code": False,
    "I can help my hw11 partner debug their code": True,
    "I can electronically transfer some of my code to my hw11 partner": False,
    ("I can tell my hw11 partner line-by-line, character-by-character " +
     "what to type so their code is nearly-identical to mine."):False,
    }


def findLargestFile(path, start=True):
    if os.path.isfile(path):
        return path, os.path.getsize(path)
    else:
        largestSize = 0
        largestPath = ""
        for filename in os.listdir(path):
            filepath = path + '/' + filename
            curFilepath, curSize = findLargestFile(filepath, False)
            if curSize > largestSize:
                largestSize = curSize
                largestPath = curFilepath
        if start:
            return largestPath
        else:
            return largestPath, largestSize


def evalPrefixNotation(L):
    a = L.pop(0)
    if isOperator(a):
        if isOperator(L[0]):
            b = evalPrefixNotation(L)
            c = evalPrefixNotation(L)
        else:
            b = L.pop(0)
            if isOperator(L[0]):
                c = evalPrefixNotation(L)
            else:
                c = L.pop(0)
        return operate(a, b, c)
    else:
        return a


def operate(a, b, c):
    if a == "+":
        return b + c
    elif a == "-":
        return b - c
    elif a == "*":
        return b * c
    else:
        return 0


def isOperator(a):
    if type(a) == int:
        return False
    else:
        if a == "+":
            return True
        elif a == "-":
            return True
        elif a == "*":
            return True
        else:
            raise Exception('Unknown operator: ' + a)


##############################################
# Generic backtracking-based puzzle solver
#
# Subclass this class to solve your puzzle
# using backtracking.
#
# To see how useful backtracking is, run with checkConstraints=True
# and again with checkConstraints=False
# You will see the number of total states go up (probably by a lot).
##############################################


class BacktrackingPuzzleSolver(object):
    def solve(self, checkConstraints=True, printReport=False):
        self.moves = []
        self.states = set()
        # If checkConstraints is False, then do not check the backtracking
        # constraints as we go (so instead do an exhaustive search)
        self.checkConstraints = checkConstraints
        # Be sure to set self.startArgs and self.startState in __init__
        self.startTime = time.time()
        self.solutionState = self.solveFromState(self.startState)
        self.endTime = time.time()
        if (printReport):
            self.printReport()
        return (self.moves, self.solutionState)

    def printReport(self):
        print()
        print('***********************************')
        argsStr = str(self.startArgs).replace(',)',
                                              ')')  # remove singleton comma
        print(f'Report for {self.__class__.__name__}{argsStr}')
        print('checkConstraints:', self.checkConstraints)
        print('Moves:', self.moves)
        print('Solution state: ', end='')
        if ('\n' in str(self.solutionState)):
            print()
        print(self.solutionState)
        print('------------')
        print('Total states:', len(self.states))
        print('Total moves: ', len(self.moves))
        millis = int((self.endTime - self.startTime)*1000)
        print('Total time:  ', millis, 'ms')
        print('***********************************')

    def solveFromState(self, state):
        if state in self.states:
            # we have already seen this state, so skip it
            return None
        self.states.add(state)
        if self.isSolutionState(state):
            # we found a solution, so return it!
            return state
        else:
            for move in self.getLegalMoves(state):
                # 1. Apply the move
                childState = self.doMove(state, move)
                # 2. Verify the move satisfies the backtracking constraints
                #    (only proceed if so)
                if ((self.stateSatisfiesConstraints(childState)) or
                        (not self.checkConstraints)):
                    # 3. Add the move to our solution path (self.moves)
                    self.moves.append(move)
                    # 4. Try to recursively solve from this new state
                    result = self.solveFromState(childState)
                    # 5. If we solved it, then return the solution!
                    if result != None:
                        return result
                    # 6. Else we did not solve it, so backtrack and
                    #    remove the move from the solution path (self.moves)
                    self.moves.pop()
            return None

    # You have to implement these:

    def __init__(self):
        # Be sure to set self.startArgs and self.startState here
        pass

    def stateSatisfiesConstraints(self, state):
        # return True if the state satisfies the solution constraints so far
        raise NotImplementedError

    def isSolutionState(self, state):
        # return True if the state is a solution
        raise NotImplementedError

    def getLegalMoves(self, state):
        # return a list of the legal moves from this state (but not
        # taking the solution constraints into account)
        raise NotImplementedError

    def doMove(self, state, move):
        # return a new state that results from applying the given
        # move to the given state
        raise NotImplementedError

##############################################
# Generic State Class
#
# Subclass this with the state required by your problem.
# Note that this is a bit hacky with __eq__, __hash__, and __repr__
# (it's fine for 112, but after 112, you should take the time to
# write better class-specific versions of these)
##############################################


class State(object):
    def __eq__(self, other): return (
        other != None) and self.__dict__ == other.__dict__

    # hack but works even with lists
    def __hash__(self): return hash(str(self.__dict__))
    def __repr__(self): return str(self.__dict__)


class BoardState(State):
    dim = 5

    def __init__(self, lastLetter, letterLocations):
        self.letterLocations = {}
        for c in string.ascii_uppercase:
            if c != "Z":
                self.letterLocations[c] = ()
        self.usedLocations = set()
        for letter in letterLocations:
            location = letterLocations[letter]
            self.letterLocations[letter] = location
            self.usedLocations.add(location)
        self.lastLetter = lastLetter

    def __repr__(self):
        board = self.returnList()
        return '\n'.join([' '.join(row) for row in board])

    def returnList(self):
        board = [(['-'] * self.dim) for row in range(self.dim)]
        for letter in self.letterLocations:
            location = self.letterLocations[letter]
            if location:
                board[location[0]][location[1]] = letter
        return board


class ABCSolver(BacktrackingPuzzleSolver):

    def __init__(self, constraintsString, aLocation):
        self.constraints = self.parseConstraints(constraintsString)
        self.constraints["A"] = [aLocation]
        self.startArgs = (constraintsString, aLocation)
        self.startState = BoardState("A", {"A": aLocation})

    def parseConstraints(self, constrStr):
        NW_Locations = [(x, x) for x in range(5)]
        SE_Locations = [(4-x, x) for x in range(5)]
        constraints = {}
        constraints[constrStr[0]] = NW_Locations
        constraints[constrStr[12]] = NW_Locations
        constraints[constrStr[6]] = SE_Locations
        constraints[constrStr[18]] = SE_Locations
        for j in range(5):
            topCol, bottomCol = j+1, 17-j
            constraints[constrStr[topCol]] = [(x, j) for x in range(5)]
            constraints[constrStr[bottomCol]] = [(x, j) for x in range(5)]
            rightRow, leftRow = j+7, 23-j
            constraints[constrStr[rightRow]] = [(j, x) for x in range(5)]
            constraints[constrStr[leftRow]] = [(j, x) for x in range(5)]

        return constraints

    def stateSatisfiesConstraints(self, state):
        # print("======================")
        # print(state)
        for letter in state.letterLocations:
            location = state.letterLocations[letter]
            if not location:
                continue
            if location not in self.constraints[letter]:
                return False
        return True

    def isSolutionState(self, state):
        if state.lastLetter == "Y" and self.stateSatisfiesConstraints(state):
            return True
        else:
            return False

    def getLegalMoves(self, state):
        moves = []
        for dRow in (-1, 0, 1):
            for dCol in (-1, 0, 1):
                if dRow == 0 and dCol == 0:
                    continue
                oldLocation = state.letterLocations[state.lastLetter]
                newRow = oldLocation[0] + dRow
                newCol = oldLocation[1] + dCol
                if newRow >= state.dim or newRow < 0:
                    continue
                elif newCol >= state.dim or newCol < 0:
                    continue
                elif (newRow, newCol) in state.usedLocations:
                    continue
                else:
                    moves.append((newRow, newCol))
        return moves

    def doMove(self, state, move):
        addedLetter = chr(ord(state.lastLetter)+1)
        newLetterLocations = state.letterLocations.copy()
        newLetterLocations[addedLetter] = move
        return BoardState(addedLetter, newLetterLocations)


def solveABC(constraints, aPosition):
    abc = ABCSolver(constraints, aPosition)
    moves, state = abc.solve(printReport=True)
    if state is not None:
        return state.returnList()
    else:
        return None


def flatten(L):
    # This is bonus!
    return 42

################################################
# ignore_rest:  place all your graphics and tests below here!
################################################

from cmu_112_graphics import *
from tkinter import *

class FreddyFractalViewer(App):
    def redrawAll(self, canvas):
        # self.teddyFace(canvas, self.width/2, self.height/2, self.width/4)
        self.fractalTeddy(canvas, self.width/2, self.height*0.7,
                            self.width/4, 7)


    def teddyFace(self, canvas, xC, yC, r):
        canvas.create_oval(xC+r, yC+r, xC-r, yC-r, fill="black")
        r2 = r*0.9
        canvas.create_oval(xC+r2, yC+r2, xC-r2, yC-r2, fill="red4")

        rM1 = r * 0.5
        yCM = yC + (r*0.35)
        canvas.create_oval(xC+rM1, yCM+rM1, xC-rM1, yCM-rM1, fill="black")
        rM2 = rM1*0.85
        canvas.create_oval(xC+rM2, yCM+rM2, xC-rM2, yCM-rM2, fill="wheat3")
        yCN = yCM - (r * 0.12)
        rN = r * 0.16
        canvas.create_oval(xC+rN, yCN+rN, xC-rN, yCN-rN, fill="black")

        rL = rM2 * 0.25
        yCL = yCM + (1.5 * rL)
        lipWidth = rL * 0.5
        canvas.create_arc(xC, yCL-rL, xC+(2*rL), yCL+rL,
                            start=180, extent=180,
                          fill="black", style=ARC, width=lipWidth)
        canvas.create_arc(xC, yCL-rL, xC-(2*rL), yCL+rL,
                          start=180, extent=180,
                          fill="black", style=ARC, width=lipWidth)



        eyeXShift = r * 0.35
        xCE1 = xC - eyeXShift
        xCE2 = xC + eyeXShift
        yCE = yC - (r * 0.35)
        rE = rN
        canvas.create_oval(xCE1+rE, yCE+rE, xCE1-rE, yCE-rE, fill="black")
        canvas.create_oval(xCE2+rE, yCE+rE, xCE2-rE, yCE-rE, fill="black")


    def fractalTeddy(self, canvas, xC, yC, r, level):
        self.teddyFace(canvas, xC, yC, r)
        if level == 0:
            return
        else:
            offset = 1.5*r/(2**0.5)
            r /= 2
            level -= 1
            yC -= offset
            xC1 = xC - offset
            xC2 = xC + offset
            self.fractalTeddy(canvas, xC1, yC, r, level)
            self.fractalTeddy(canvas, xC2, yC, r, level)
            return


def runFreddyFractalViewer():
    FreddyFractalViewer(width=400, height=400)




#################################################
# Test Functions
#################################################

def testConfirmPolicies():
    print('Testing confirmPolicies()...', end='')
    truePolicies = [
        'I can work solo on hw11',
        'I can work with one partner on hw11',
        ("I must list my hw11 partner's name and andrewId at the top" +
         "of my hw11.py file that I submit"),
        'My hw11 partner must be in 112 this semester',
        "I can look at my hw11 partner's code",
        "I can help my hw11 partner debug their code",
    ]
    falsePolicies = [
        'I can switch hw11 partners and then work with a new partner',
        'My hw11 partner must be in the same lecture or section as me',
        "I can copy some of hw11 partner's code",
        "I can electronically transfer some of my code to my hw11 partner",
        ("I can tell my hw11 partner line-by-line, character-by-character " +
         "what to type so their code is nearly-identical to mine."),
    ]
    policies = confirmPolicies()
    # True policies:
    for policy in truePolicies:
        assert(policies[policy] == True)
    # False policies (the opposite of these are actually policies)
    for policy in falsePolicies:
        assert(policies[policy] == False)
    print('Passed!')

def testFindLargestFile():
    print('Testing findLargestFile()...', end='')
    assert(findLargestFile('sampleFiles/folderA') ==
                           'sampleFiles/folderA/folderC/giftwrap.txt')
    assert(findLargestFile('sampleFiles/folderB') ==
                           'sampleFiles/folderB/folderH/driving.txt')
    assert(findLargestFile('sampleFiles/folderB/folderF') == '')
    print('Passed!')

def testEvalPrefixNotation():
    print('Testing evalPrefixNotation()...', end='')
    assert(evalPrefixNotation([42]) == 42)
    assert(evalPrefixNotation(['+', 3, 4]) == 7)
    assert(evalPrefixNotation(['-', 3, 4]) == -1)
    assert(evalPrefixNotation(['-', 4, 3]) == 1)
    assert(evalPrefixNotation(['+', 3, '*', 4, 5]) == 23)
    assert(evalPrefixNotation(['+', '*', 2, 3, '*', 4, 5]) == 26)
    assert(evalPrefixNotation(['*', '+', 2, 3, '+', 4, 5]) == 45)
    assert(evalPrefixNotation(['*', '+', 2, '*', 3, '-', 8, 7,
                               '+', '*', 2, 2, 5]) == 45)
    raisedAnError = False
    try:
        evalPrefixNotation(['^', 2, 3])
    except:
        raisedAnError = True
    assert(raisedAnError == True)
    print('Passed.')

def testSolveABC():
    print('Testing solveABC()...', end='')
    constraints = 'CHJXBOVLFNURGPEKWTSQDYMI'
    aLocation = (0,4)
    board = solveABC(constraints, aLocation)
    solution = [['I', 'J', 'K', 'L', 'A'],
                ['H', 'G', 'F', 'B', 'M'],
                ['T', 'Y', 'C', 'E', 'N'],
                ['U', 'S', 'X', 'D', 'O'],
                ['V', 'W', 'R', 'Q', 'P']
               ]
    assert(board == solution)

    constraints = 'TXYNFEJOQCHIMBDSUWPGKLRV'
    aLocation = (2,4)
    board = solveABC(constraints, aLocation)
    solution = [['V', 'U', 'S', 'O', 'P'],
                ['W', 'T', 'N', 'R', 'Q'],
                ['X', 'L', 'M', 'C', 'A'],
                ['K', 'Y', 'H', 'D', 'B'],
                ['J', 'I', 'G', 'F', 'E'],
               ]
    assert(board == solution)

    constraints = 'TXYNFEJOQCHIMBDSUPWGKLRV' # swapped P and W
    aLocation = (2,4)
    board = solveABC(constraints, aLocation)
    solution = None
    assert(board == solution)
    print('Passed!')

def testFlatten():
    print('Testing bonus flatten()...', end='')
    assert(flatten([1,[2]]) == [1,2])
    assert(flatten([1,2,[3,[4,5],6],7]) == [1,2,3,4,5,6,7])
    assert(flatten(['wow', [2,[[]]], [True]]) == ['wow', 2, True])
    assert(flatten([]) == [])
    assert(flatten([[]]) == [])
    assert(flatten(3) == 3)
    print('Passed!')

#################################################
# testAll and main
#################################################

def testAll():
    testConfirmPolicies()
    testFindLargestFile()
    testEvalPrefixNotation()
    testSolveABC()
    runFreddyFractalViewer()
    # testFlatten() # bonus

def main():
    cs112_f19_week11_linter.lint()
    testAll()

if (__name__ == '__main__'):
    main()
