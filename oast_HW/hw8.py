#################################################
# hw8.py
#
# Your name: Eric Jenny
# Your andrew id: ejenny
#################################################

"""
# 1A: Swaps the first and last element of the list
def slow1(lst):  # N is the length of the list lst
    assert(len(lst) >= 2)
    a = lst.pop()    # O(1)
    b = lst.pop(0)   # O(n)
    lst.insert(0, a)  # O(n)
    lst.append(b)    # O(1)
    ## O(n)
# 1C:
def fast1(lst):
    temp = lst[0]  # O(1)
    lst[0] = lst[len(lst)-1]  # O(1)
    lst[len(lst)-1] = temp  # O(1)
# 1D: O(1)


# 2A: Counts how many unique elements there are in list
def slow2(lst):  # N is the length of the list lst
    counter = 0                   # O(1)
    for i in range(len(lst)):     # n Loops
        if lst[i] not in lst[:i]:  # O(n)
            counter += 1          # O(1)
    return counter                # O(1)
    ## O(n**2)
# 2C:
def fast2(lst):
    quickSet = set(lst)         # O(n)
    count = 0                   # O(1)
    for e in quickSet:          # n loops
        count += 1              # O(1)
    return count                # O(1)
    ## O(n)
# 2D: O(n)


# 3A: returns the lowercase letter in the string that appears the most
#      if there is a tie, the letter that is earlier in the alphabet
def slow3(s):  # N is the length of the string s
    maxLetter = ""                              # O(1)
    maxCount = 0                                # O(1)
    for c in s:                                 # n Loops
        for letter in string.ascii_lowercase:   # 26 Loops
            if c == letter:                     # O(1)
                if s.count(c) > maxCount or \
                   s.count(c) == maxCount and \
                   c < maxLetter:               # O(n)
                    maxCount = s.count(c)       # O(n)
                    maxLetter = c               # O(1)
    return maxLetter                            # O(1)
    ## O(n**2)
# 3C:
def fast3(s):
    a = ord("a")                            # O(1)
    counts = [0 for i in range(26)]         # O(1)
    for c in s:                             # n loops
        letterID = ord(c) - a               # O(1)
        if letterID >= 0 or letterID < 26:  # O(1)
            counts[letterID] += 1            # O(1)
    max = 0                                 # O(1)
    maxIndex = -1                           # O(1)
    i = 0                                   # O(1)
    for count in counts:                    # n loops
        if count > max:                     # O(1)
            maxIndex = i                    # O(1)
        i += 1                              # O(1)
    if maxIndex == -1:                      # O(1)
        return ""                           # O(1)
    else:                                   # O(1)
        return chr(a + maxIndex)            # O(1)
    ## O(n)
# 3D: O(n)


# 4A: returns the greatest difference between an element in a
#       and an element in b if the element is a > element in b
def slow4(a, b): # a and b are lists with the same length N
    assert(len(a) == len(b))
    result = abs(a[0] - b[0])    # O(1)
    for c in a:                  # n Loops
        for d in b:              # n Loops
            delta = abs(c - d)   # O(1)
            if (delta > result): # O(1)
                result = delta   # O(1)
    return result                # O(1)
    ## O(n**2)
# 4C:
def fast4(a, b):
    maxA, minA = a[0], a[0]     # O(1)
    for c in a:                 # n loops
        if c > maxA:            # O(1)
            maxA = c            # O(1)
        if c < minA:            # O(1)
            minA = c            # O(1)

    maxB, minB = b[0], b[0]     # O(1)
    for d in b:                 # O(n)
        if d > maxB:            # O(1)
            maxB = d            # O(1)
        if d < minB:            # O(1)
            minB = d            # O(1)

    aB = abs(maxA - minB)       # O(1)
    bA = abs(maxB - minA)       # O(1)
    if aB > bA:                 # O(1)
        return aB               # O(1)
    else:                       # O(1)
        return bA               # O(1)
    ## O(n)
# 4D: O(n)
"""

import string

# 1A: Swaps the first and last element of the list
def slow1(lst):  # N is the length of the list lst
    assert(len(lst) >= 2)
    a = lst.pop()    # O(1)
    b = lst.pop(0)   # O(n)
    lst.insert(0, a)  # O(n)
    lst.append(b)    # O(1)
    ## O(n)
# 1C:
def fast1(lst):
    temp = lst[0]  # O(1)
    lst[0] = lst[len(lst)-1]  # O(1)
    lst[len(lst)-1] = temp  # O(1)
# 1D: O(1)


# 2A: Counts how many unique elements there are in list
def slow2(lst):  # N is the length of the list lst
    counter = 0                   # O(1)
    for i in range(len(lst)):     # n Loops
        if lst[i] not in lst[:i]:  # O(n)
            counter += 1          # O(1)
    return counter                # O(1)
    ## O(n**2)
# 2C:
def fast2(lst):
    quickSet = set(lst)         # O(n)
    count = 0                   # O(1)
    for e in quickSet:          # n loops
        count += 1              # O(1)
    return count                # O(1)
    ## O(n)
# 2D: O(n)


# 3A: returns the lowercase letter in the string that appears the most
#      if there is a tie, the letter that is earlier in the alphabet
def slow3(s):  # N is the length of the string s
    maxLetter = ""                              # O(1)
    maxCount = 0                                # O(1)
    for c in s:                                 # n Loops
        for letter in string.ascii_lowercase:   # 26 Loops
            if c == letter:                     # O(1)
                if s.count(c) > maxCount or \
                   s.count(c) == maxCount and \
                   c < maxLetter:               # O(n)
                    maxCount = s.count(c)       # O(n)
                    maxLetter = c               # O(1)
    return maxLetter                            # O(1)
    ## O(n**2)
# 3C:
def fast3(s):
    a = ord("a")                            # O(1)
    counts = [0 for i in range(26)]         # O(1)
    for c in s:                             # n loops
        letterID = ord(c) - a               # O(1)
        if letterID >= 0 and letterID < 26:  # O(1)
            counts[letterID] += 1           # O(1)
    max = 0                                 # O(1)
    maxIndex = -1                           # O(1)
    i = 0                                   # O(1)
    for count in counts:                    # n loops
        if count > max:                     # O(1)
            maxIndex = i                    # O(1)
            max = count                     # O(1)
        i += 1                              # O(1)
    if maxIndex == -1:                      # O(1)
        return ""                           # O(1)
    else:                                   # O(1)
        return chr(a + maxIndex)            # O(1)
    ## O(n)
# 3D: O(n)


# 4A: returns the greatest difference between an element in a
#       and an element in b if the element is a > element in b
def slow4(a, b): # a and b are lists with the same length N
    assert(len(a) == len(b))
    result = abs(a[0] - b[0])    # O(1)
    for c in a:                  # n Loops
        for d in b:              # n Loops
            delta = abs(c - d)   # O(1)
            if (delta > result): # O(1)
                result = delta   # O(1)
    return result                # O(1)
    ## O(n**2)
# 4C:
def fast4(a, b):
    maxA, minA = a[0], a[0]     # O(1)
    for c in a:                 # n loops
        if c > maxA:            # O(1)
            maxA = c            # O(1)
        if c < minA:            # O(1)
            minA = c            # O(1)

    maxB, minB = b[0], b[0]     # O(1)
    for d in b:                 # O(n)
        if d > maxB:            # O(1)
            maxB = d            # O(1)
        if d < minB:            # O(1)
            minB = d            # O(1)

    aB = abs(maxA - minB)       # O(1)
    bA = abs(maxB - minA)       # O(1)
    if aB > bA:                 # O(1)
        return aB               # O(1)
    else:                       # O(1)
        return bA               # O(1)
    ## O(n)
# 4D: O(n)

import decimal
import cs112_f19_week8_linter
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


def getPairSum(lst, target):
    """ Takes a list of integers and a target value (also an integer),
    and if there is a pair of numbers in the given list that add up to
    the given target number, returns that pair as a tuple; otherwise,
    it returns None.
    """
    quickSet = set(lst)
    for x in lst:
        compliment = target-x
        if compliment in quickSet:
            return (x, compliment)
    return None


def containsPythagoreanTriple(lst):
    """ Takes a list of positive integers and returns True if there
    are 3 values (a, b, c) anywhere in the list such that (a, b, c)
    form a Pythagorean Triple.
    """
    squares = [x**2 for x in lst]
    for x in squares:
        if getPairSum(squares, x) is not None:
            return True
    return False


def movieAwards(oscarResults):
    """ Takes a set of tuples, where each tuple holds the name of a
    category and the name of the winning movie, then returns a
    dictionary mapping each movie to the number of the awards that it won.
    """
    winners = {}
    for categoryWinner in oscarResults:
        movie = categoryWinner[1]
        if movie in winners:
            winners[movie] += 1
        else:
            winners[movie] = 1
    return winners


def friendsOfFriends(d):
    """ Takes such a dictionary mapping people to sets of friends and
    returns a new dictionary mapping all the same people to sets of
    their friends-of-friends.
    """
    friendsOfFriends = {}
    for friendKey in d:
        friendSet = d[friendKey]
        friendsOfFriendsSet = set()
        for friend in friendSet:
            for friendsOfFriend in d[friend]:
                if friendsOfFriend != friendKey \
                  and friendsOfFriend not in friendsOfFriendsSet \
                  and friendsOfFriend not in friendSet:
                    friendsOfFriendsSet.add(friendsOfFriend)
        friendsOfFriends[friendKey] = friendsOfFriendsSet
    return friendsOfFriends


#################################################
# Test Functions
#################################################

def test1():
    l1 = [1, 2, 3, 4, 5, 6]
    l2 = ["a", "b", "c", "d", "e"]
    assert(fast1(l1) == slow1(l1))
    assert(fast1(l2) == slow1(l2))


def test2():
    l1 = [1, 2, 3, 4, 5, 6]
    l2 = ["a", "a", "a", "b", "b"]
    assert(fast2(l1) == slow2(l1))
    assert(fast2(l2) == slow2(l2))


def test3():
    s1 = "abcdefa"
    s2 = "AAABBC"
    assert(fast3(s1) == slow3(s1))
    assert(fast3(s2) == slow3(s2))


def test4():
    l1 = [10, 20, 30, 40, 50, 60]
    l2 = [0, 1, 2, 3, 4, 5]
    assert(fast4(l1, l2) == slow4(l1, l2))


def testO():
    test1()
    test2()
    test3()
    test4()


def testGetPairSum():
    print("Testing getPairSum... ", end="")
    assert(getPairSum([5, 2], 7) in [(5, 2), (2, 5)])
    assert(getPairSum([10, -1, 1, -8, 3, 1], 2)

           in [(10, -8), (-8, 10), (-1, 3), (3, -1), (1, 1)])
    assert(getPairSum([10, -1, 1, -8, 3, 1], 10) == None)
    print("passed!")


def testContainsPythagoreanTriple():
    print("Testing containsPythagoreanTriple... ", end="")
    assert(containsPythagoreanTriple([1, 3, 6, 2, 5, 1, 4]) == True)
    assert(containsPythagoreanTriple([5, 12, 13]) == True)
    assert(containsPythagoreanTriple([1, 2, 3]) == False)
    print("passed!")


def testMovieAwards():
    print("Testing movieAwards... ", end="")
    in1 = {
            ("Best Picture", "Green Book"),
            ("Best Actor", "Bohemian Rhapsody"),
            ("Best Actress", "The Favourite"),
            ("Film Editing", "Bohemian Rhapsody"),
            ("Best Original Score", "Black Panther"),
            ("Costume Design", "Black Panther"),
            ("Sound Editing", "Bohemian Rhapsody"),
            ("Best Director", "Roma")
          }
    out1 = {
            "Black Panther" : 2,
            "Bohemian Rhapsody" : 3,
            "The Favourite" : 1,
            "Green Book" : 1,
            "Roma" : 1
           }
    assert(movieAwards(in1) == out1)
    print("passed!")


def testFriendsOfFriends():
    d = { }
    d["jon"] = set(["arya", "tyrion"])
    d["tyrion"] = set(["jon", "jaime", "pod"])
    d["arya"] = set(["jon"])
    d["jaime"] = set(["tyrion", "brienne"])
    d["brienne"] = set(["jaime", "pod"])
    d["pod"] = set(["tyrion", "brienne", "jaime"])
    d["ramsay"] = set()
    o1 = {
        'tyrion': {'arya', 'brienne'},
        'pod': {'jon'},
        'brienne': {'tyrion'},
        'arya': {'tyrion'},
        'jon': {'pod', 'jaime'},
        'jaime': {'pod', 'jon'},
        'ramsay': set()
    }
    assert(friendsOfFriends(d) == o1)


#################################################
# testAll and main
#################################################


def testAll():
    testGetPairSum()
    testContainsPythagoreanTriple()
    testMovieAwards()
    testFriendsOfFriends()

def main():
    cs112_f19_week8_linter.lint()
    testAll()
    testO()


if __name__ == '__main__':
    main()
