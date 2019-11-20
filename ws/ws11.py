
###############################################################################
# Writing Session 11, Coding Portion: [20 pts]

# Do not edit these lines:
#   user: 'ejenny@andrew.cmu.edu' (do not edit this!)
#   downloaded at: '2019-11-08 11:35:25' (do not edit this!)
#   downloaded ip: '128.237.157.146' (do not edit this!)
#   security code: '323022234674958254ENGQRZABPFTFX2GMW2IFW' (do not edit this!)

# Note #1: If you are not in a proctored writing-session lab, close this file
# immediately and email koz@cmu.edu and mdtaylor@andrew.cmu.edu to let
# us know that this occurred.

# Note #2: Do not edit this header, only edit the code below the header.

# Note #3: Select-all and copy this entire file, all of it, exactly as it
# is here, paste it into your ws11.py starter file, then edit it, and submit
# that edited file to Autolab while you are still in the proctored
# writing-session lab.

# Note #4: You will need to download the ws11_linter.py from here:
# http://www.cs.cmu.edu/~112/notes/ws11_linter.py

###############################################################################

#################################################
#
# Note: everywhere you need to write code has this line:
#        return 42 # YOU WRITE THIS
#
#################################################

import time
import turtle
import decimal
import ws11_linter
import math
import copy
import os

#################################################
# Helper functions
#################################################


def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)
# Replace this with code you select-all/copy-paste
# from the starter website.

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

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
        if (chr(10) in str(self.solutionState)):
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
    def __eq__(self, other): return ((other != None) and
                                     (self.__dict__ == other.__dict__))

    def __hash__(self): return hash(
        str(self.__dict__))  # hack but works w/lists

    def __repr__(self): return str(self.__dict__)

##############################################
# SubsetSumSolver and SubsetSumState
##############################################


class SubsetSumState(State):
    def __init__(self, remainingValues, partialSolution):
        # remainingValues: the values still left in L to consider using
        # partialSolution: the values we have already added to our solution
        self.remainingValues = remainingValues
        self.partialSolution = partialSolution

    def __repr__(self):
        return str(self.partialSolution)


class SubsetSumSolver(BacktrackingPuzzleSolver):
    def __init__(self, L, target):
        assert(min(L) > 0)  # assume all the values in L are positive
        self.L = L
        self.target = target
        self.startArgs = (L, target)  # for printReport
        self.startState = SubsetSumState(L, [])

    def stateSatisfiesConstraints(self, state):
        if sum(state.partialSolution) <= self.target:
            return True
        else:
            return False

    def isSolutionState(self, state):
        if sum(state.partialSolution) == self.target:
            return True
        else:
            return False

    def getLegalMoves(self, state):
        if len(state.remainingValues) > 1:
            return ["use", "skip"] #state.remainingValues
        else:
            return []

    def doMove(self, state, move):
        first = state.remainingValues[0]
        rest = state.remainingValues[1:]
        if (move == 'use'):
            newState = SubsetSumState(rest, state.partialSolution + [first])
        else:
            # move == 'skip'
            newState = SubsetSumState(rest, state.partialSolution)
        return newState

##############################################
# NQueensSolver and NQueensState
##############################################


class NQueensState(State):
    def __init__(self, n, queenPositions):
        self.n = n
        # queenPositions is a list of (row, col) positions of each queen
        self.queenPositions = queenPositions

    def __repr__(self):
        board = [(['-'] * self.n) for row in range(self.n)]
        for (row, col) in self.queenPositions:
            board[row][col] = 'Q'
        return chr(10).join([' '.join(row) for row in board])


class NQueensSolver(BacktrackingPuzzleSolver):
    def __init__(self, n):
        self.n = n
        self.startArgs = (n,)  # for printReport
        self.startState = NQueensState(n, [])

    @staticmethod
    def queensAttackEachOther(row1, col1, row2, col2):
        if row1 == row2 or col1 == col2:
            return True
        elif row1 - row2 == col1 - col2:
            return True
        elif row2 - row1 == col1 - col2:
            return True
        else:
            return False

    def stateSatisfiesConstraints(self, state):
        # The constraints are satisifed if no two queens can attack each other,
        # But we check this as we go, so we only have to check the last queen!
        (row1, col1) = state.queenPositions[-1]  # this is the last queen added
        for (row2, col2) in state.queenPositions[:-1]:
            if (self.queensAttackEachOther(row1, col1, row2, col2)):
                return False
        return True

    def isSolutionState(self, state):
        if (len(state.queenPositions) < self.n):
            return False
        # Confirm that no two queens attack each other, but we have to check all
        # pairs of queens (since we can call solver with checkConstraints=False)
        for i in range(self.n):
            (row1, col1) = state.queenPositions[i]
            for j in range(i):
                (row2, col2) = state.queenPositions[j]
                if (self.queensAttackEachOther(row1, col1, row2, col2)):
                    return False
        return True

    def getLegalMoves(self, state):
        col = len(state.queenPositions)
        return [(x, col) for x in range(self.n)]

    def doMove(self, state, move):
        newPositions = state.queenPositions + [move]
        return NQueensState(self.n, newPositions)

##############################################
# Memoized Fib
##############################################


fibResults = dict()


def fib(n):
    if n in fibResults:
        return fibResults[n]
    if n <= 1:
        fibResults[n] = 1
        return 1
    else:
        fibSum = fib(n-1) + fib(n-2)
        fibResults[n] = fibSum
        return fibSum


################################################
# ignore_rest:  place all your graphics and tests below here!
################################################

# This example uses turtle graphics, not Tkinter


def drawKochSide(length, level):
    if (level == 1):
        turtle.forward(length)
    else:
        length /= 3
        level -= 1
        drawKochSide(length, level)
        turtle.left(60)
        drawKochSide(length, level)
        turtle.right(120)
        drawKochSide(length, level)
        turtle.left(60)
        drawKochSide(length, level)
        # return 42  # YOU WRITE THIS
        # # Hint #1: the recursive calls to drawKochSide use length/3
        # # Hint #2: You will want to call turtle.right(120) and turtle.left(60)
        # #          in the right places
        # pass


def drawKochSnowflake(length, level):
    for step in range(3):
        drawKochSide(length, level)
        turtle.right(120)


def drawKochExamples():
    turtle.delay(1)
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-300, 100)
    turtle.pendown()
    turtle.pencolor('black')
    drawKochSide(300, 2)
    turtle.pencolor('blue')
    drawKochSnowflake(300, 3)
    turtle.done()

#################################################
# Test Functions
#################################################


def testSubsetSumSolver():
    print('Testing SubsetSumSolver...', end='')
    (moves, solution) = SubsetSumSolver([3, 6, 5, 2, 11, 7, 3], 15).solve()
    assert(sum(solution.partialSolution) == 15)
    (moves, solution) = SubsetSumSolver([3, 6, 5, 2, 11, 7, 3], 11).solve()
    assert(sum(solution.partialSolution) == 11)
    (moves, solution) = SubsetSumSolver([3, 6, 5, 2, 11, 7, 3], 4).solve()
    assert(solution == None)
    print('Passed!')


def testNQueensSolver():
    print('Testing NQueensSolver...', end='')

    (moves, solution) = NQueensSolver(1).solve()
    assert(moves == [(0, 0)])
    assert(str(solution) == 'Q')

    (moves, solution) = NQueensSolver(2).solve()
    assert(solution == None)

    (moves, solution) = NQueensSolver(4).solve()
    assert(moves == [(1, 0), (3, 1), (0, 2), (2, 3)])
    assert(str(solution) == '''- - Q -
Q - - -
- - - Q
- Q - -''')

    print('Passed!')


def testMemoizedFib(maxN=40):
    print('Testing memoized fib using fibResults dictionary...', end='')
    assert(fibResults == dict())
    k = fib(4)
    assert(fibResults == {0: 1, 1: 1, 2: 2, 3: 3, 4: 5})
    k = fib(7)
    assert(fibResults == {0: 1, 1: 1, 2: 2, 3: 3, 4: 5, 5: 8, 6: 13, 7: 21})
    print('Passed!')

#################################################
# testAll and main
#################################################


def testAll():
    testSubsetSumSolver()
    testNQueensSolver()
    testMemoizedFib()
    if (input('Call drawKochExamples? [y/n] ') == 'y'):
        drawKochExamples()


def main():
    ws11_linter.lint()
    testAll()


if (__name__ == '__main__'):
    main()
