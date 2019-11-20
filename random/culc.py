# sum = 0
# for n in range(1, 11):
# sum += 1/(n**4)
# print(sum)


# import math

# sum = 0
# for n in range(1, 11):
#     an = (math.exp(1/n))/(n**4)
#     sum += an
#     print(n, round(an, 4), round(sum, 4))


# import math

# pi = math.pi
# fcs = [500, 1000, 5000, 9000]
# dt = 1/(18000*2)
# for fc in fcs:
#     alpha = (1 - math.sin(2*pi*fc*dt))/(math.cos(2*pi*fc*dt))
#     print(round(alpha, 2))


# aN = 1
# sN = 0.0
# n = 0
# while abs(aN) > 0.000001:
#     aN = (-1)**n * (0.3)**(4*n + 3) / (4*n + 3)
#     sN += aN
#     print(n, aN, sN)
#     n += 1


sN = 0.0
for n in range(1, 1000):
    sN += n**2 / 2**n

print(sN)
