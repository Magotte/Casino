import random
#
#
x = [3, 4, 5]
y = [1, 3, 2]
#
#
# print(x[1])
#
def OrderID(id, list): # Re-order a list in function of ID numbers
    z, t = zip(*sorted(zip(id, list)))
    return(t)

# print(OrderID(y,x))
# la = [i + j for i, j in zip(OrderID(y, x), x)]
# print(la)

def r(n, seq):
    choices = []
    for i in range(n):
        choices.append(random.choice(seq))
    return choices
# p = zip(y,x)
# print(*sorted(p))
# print(sorted(list(p)))


# print(AssignTypes(0.1, 0.5, "bachelor", "returning", "new", 20))
#
# def r(n, seq):
#     choices = []
#     for i in range(1,n):
#         choices.append(random.choice(seq))
#     return(choices)
#
#
# print(r(100, range(1, 20)))

# def SubList(which, list, amounts):  # obtain elements for a given given table (list)
#     t = []
#     for i in range(len(list)):
#         if (list[i] == which):
#             t.append(amounts[i])
#     return(t)
#
# l = [1, 2, 3, 4, 5, 6, 7, 9, 12, 2, 3, 2]
# a = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
# print(SubList(14, l, a))

# ll = [2]*3
# print(ll)

nbC = 5
orders = r(nbC, [0, 1, 2])
wealth = [200, 50, 90, 61, 50]
drinks = r(nbC, [1, 2])
spend = [i * j * 20 * bool(k > (60 * j)) for i, j, k in zip(drinks, orders, wealth)]
print(spend)
print(drinks)
print(orders)