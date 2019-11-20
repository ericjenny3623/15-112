#################################################
# hw10.py
#
# Your name: Eric Jenny
# Your andrew id: ejenny
#################################################

import decimal
import cs112_f19_week10_linter
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


def alternatingSum(L):
    if len(L) == 0:
        return 0
    else:
        return L[0] - alternatingSum(L[1:])


def onlyEvenDigits(L):
    if len(L) == 0:
        return []
    else:
        return [trimOddDigits(L[0])] + onlyEvenDigits(L[1:])


def trimOddDigits(n):
    if n < 10:
        return n if n % 2 == 0 else 0
    else:
        separator = 10**getPowerOfTen(n)
        firstDigit = n//separator
        remainder = n % separator
        previousDigitsTrimmed = trimOddDigits(remainder)
        if previousDigitsTrimmed == 0:
            newScale = 1
        else:
            newScale = 10**(getPowerOfTen(previousDigitsTrimmed) + 1)

        if firstDigit % 2 == 0:
            return firstDigit*newScale + previousDigitsTrimmed
        else:
            return previousDigitsTrimmed


def getPowerOfTen(num):
    return math.floor(math.log10(num))


def powersOf3ToN(n):
    x = n/3
    if x < (1/3):
        return []
    else:
        largestPowerOf3 = 3**(math.floor(math.log(x, 3))+1)
        return powersOf3ToN(largestPowerOf3) + [largestPowerOf3]


def binarySearchValues(L, item):
    values = binarySearchValuesRecursive(L, 0, len(L), item)
    return values


def binarySearchValuesRecursive(L, low, high, target):
    mid = (high+low)//2
    midValue = L[mid]
    if midValue == target or low >= high-1:
        return [(mid, L[mid])]
    elif target > midValue:
        return [(mid, L[mid])] + \
            binarySearchValuesRecursive(L, mid+1, high, target)
    elif target < midValue:
        return [(mid, L[mid])] + \
            binarySearchValuesRecursive(L, low, mid, target)
    else:
        return None


def secondLargest(L):
    if len(L) < 2:
        return None
    largestIndex = largestValueIndex(L)
    L.pop(largestIndex)
    return L[largestValueIndex(L)]


def largestValueIndex(L):
    if len(L) == 1:
        return 0
    else:
        prevLargestIndex = largestValueIndex(L[1:])+1
        if L[prevLargestIndex] > L[0]:
            return prevLargestIndex
        else:
            return 0

#################################################
# Test Functions
#################################################


def testAlternatingSum():
    print('Testing alternatingSum()...', end='')
    assert(alternatingSum([1, 2, 3, 4, 5]) == 1-2+3-4+5)
    assert(alternatingSum([]) == 0)
    print('Passed!')


def testSecondLargest():
    print('Testing secondLargest()...', end='')
    assert(secondLargest([1, 2, 3, 4, 5]) == 4)
    assert(secondLargest([4, 3]) == 3)
    assert(secondLargest([4, 4, 3]) == 4)
    assert(secondLargest([-3, -4]) == -4)
    assert(secondLargest([4]) == None)
    assert(secondLargest([]) == None)
    print('Passed!')


def testOnlyEvenDigits():
    print('Testing onlyEvenDigits()...', end='')
    assert(onlyEvenDigits([43, 23265, 17, 58344]) == [4, 226, 0, 844])
    assert(onlyEvenDigits([]) == [])
    # assert(onlyEvenDigits([1, 2, 3, 45, 678, 80, 90, 801, 902]) ==
    #    [0, 2, 0, 4, 68, 80, 0, 80, 2])
    print('Passed!')


def testPowersOf3ToN():
    print('Testing powersOf3ToN()...', end='')
    assert(powersOf3ToN(10.5) == [1, 3, 9])
    assert(powersOf3ToN(27) == [1, 3, 9, 27])
    assert(powersOf3ToN(26.999) == [1, 3, 9])
    assert(powersOf3ToN(-1) == [])
    print(powersOf3ToN(2187))
    assert(powersOf3ToN(2187) == [1, 3, 9, 27, 81, 243, 729, 2187])
    print('Passed!')


def testBinarySearchValues():
    print('Testing binarySearchValues()...', end='')
    assert(binarySearchValues(['a', 'c', 'f', 'g', 'm', 'q'], 'c') ==
           [(2, 'f'), (0, 'a'), (1, 'c')])
    assert(binarySearchValues(['a', 'c', 'f', 'g', 'm', 'q'], 'n') ==
           [(2, 'f'), (4, 'm'), (5, 'q')])
    print('Passed!')

#################################################
# testAll and main
#################################################


def testAll():
    testAlternatingSum()
    testOnlyEvenDigits()
    testPowersOf3ToN()
    testBinarySearchValues()
    testSecondLargest()


def main():
    cs112_f19_week10_linter.lint()
    testAll()


if (__name__ == '__main__'):
    main()
