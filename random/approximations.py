
# sum = 0
# n = 8
# a = 0
# b = 2
# delta = (b-a)/n
# precision = 6


# def f(x):
#     return 1 / (1 + x**6)


# def printf(x):
#     print(round(x, precision))


# for i in range(n):
#     x = delta*(i+0.5) + a
#     y = f(x)
#     sum += y
#     printf(y)
# printf(sum)
# printf(sum*delta)
# print("++++++++++++++++++++++")

# sum = 0
# for i in range(n + 1):
#     if i == 0:
#         c = 1
#     elif i == n:
#         c = 1
#     elif i % 2 == 0:
#         c = 2
#     else:
#         c = 4
#     x = delta*i + a
#     y = f(x)
#     sum += y*c
#     printf(y)
# printf(sum)
# printf(sum*delta/3)
# print("++++++++++++++++++++++")


# sum = 0
# for i in range(n + 1):
#     if i == 0:
#         c = 1
#     elif i == n:
#         c = 1
#     else:
#         c = 2
#     x = delta*i + a
#     y = f(x)
#     sum += y*c
#     printf(y)
# printf(sum)
# printf(sum*delta/2)

h = 0.2
a = 0
b = 1

x0 = 0
y0 = 1
x = x0
y = y0
for n in range(int((b-a)/h)):
    dy = (x*x*y) - (y*y*0.5)
    y += (h*dy)
    x += h
    print(n, x, y, dy)
