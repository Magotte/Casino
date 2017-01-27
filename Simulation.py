import Roulette
import Craps
import random
# from collections import Counter
# import numpy as np
# from matplotlib import pyplot as plt

# bs = [1, 2, 3, 3, 5, 6, 7, 8, 32, 24]
# gs = [20, 30, 40, 50, 100, 10, 30, 150, 300, 26]
#
# t = Roulette.Roulette(25)
# print(t.SimulateGame(bs, gs))
#
# cr = [2, 3, 5, 8, 9, 10, 11, 12]
# crb = [18, 25, 90, 100, 100, 8, 9, 30]

# t2 = Craps.Craps(20)
# print(t2.SimulateGame(cr, crb))

# throws = [Craps.Dices()*1000]
# labels, values = zip(*Counter(thousandsthrows).items())
# indexes = np.arange(len(labels))
# width = 1
# plt.bar(indexes, values, width)
# plt.xticks(indexes + width * 0.5, labels)
# plt.show()

# Possible outcomes
x = [i for i in range(7) if i != 0]
y = []
for i in x:
    for j in x:
        y.append(i + j)

dist = []

for j in [i for i in range(13) if i > 1]:
    dist.append(y.count(j))

# Scale it to obtain 90% - 10%
distScale = [(36 * 0.9) / i for i in dist]
print(dist)
print(distScale)

def r(n,seq):
    choices = []
    for i in range(n):
        choices.append(random.choice(seq))
    return(choices)


xx = [i for i in range(2, 13)]
casino = []
customers = []
for i in range(1000):
    craps = Craps.Craps(0, distScale)
    c = craps.SimulateGame(r(100, xx), r(100, range(101)))
    casino.append(c[0]) # Amount gained by the casino
    customers.append(sum(c[1])) # Sum of gains of the customers

print(casino)
print(customers)

share = [j / (i + j) for i, j in zip(casino, customers)]
# print(sum(customers)/(sum(casino) + sum(customers)))
print(sum(share)/len(share))
# t = r(10, xx)
# print(t)


# c = Craps.Craps(0, distScale)
# print(c.SimulateGame(r(20, xx), r(20, range(101))))
