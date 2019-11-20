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

import copy
import time
import string


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


def testSolveABC():
    print('Testing solveABC()...', end='')
    constraints = 'CHJXBOVLFNURGPEKWTSQDYMI'
    aLocation = (0, 4)
    board = solveABC(constraints, aLocation)
    solution = [['I', 'J', 'K', 'L', 'A'],
                ['H', 'G', 'F', 'B', 'M'],
                ['T', 'Y', 'C', 'E', 'N'],
                ['U', 'S', 'X', 'D', 'O'],
                ['V', 'W', 'R', 'Q', 'P']
                ]
    assert(board == solution)

    constraints = 'TXYNFEJOQCHIMBDSUWPGKLRV'
    aLocation = (2, 4)
    board = solveABC(constraints, aLocation)
    solution = [['V', 'U', 'S', 'O', 'P'],
                ['W', 'T', 'N', 'R', 'Q'],
                ['X', 'L', 'M', 'C', 'A'],
                ['K', 'Y', 'H', 'D', 'B'],
                ['J', 'I', 'G', 'F', 'E'],
                ]
    assert(board == solution)

    constraints = 'TXYNFEJOQCHIMBDSUPWGKLRV'  # swapped P and W
    aLocation = (2, 4)
    board = solveABC(constraints, aLocation)
    solution = None
    assert(board == solution)
    print('Passed!')


testSolveABC()
