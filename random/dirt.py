def ct1(x):
    for y in range(x, 2*x, 1+x//2):
        for z in range(3, 4):
            print("huh", end=".")
            x += 1
            if ((x + z) % 2 == 1):
                print("A", x, end=" ")
        for z in range(y, y-3, -2):
            print("B", z, end=" ")
    return y


print(ct1(4))
