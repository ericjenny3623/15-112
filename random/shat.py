# import copy


# def ct1(s):
#     t = s
#     u = copy.copy(s)
#     s += 'b'
#     return s, t, u


# for value in ct1('a'):
#     print(value)
# for value in ct1(['a']):
#     print(value)


a = [1, 2, 3, 6, 4, 5]
for x in a:
    if x % 3 == 0:
        a.remove(x)
print(a)
