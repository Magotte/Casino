import random
def r(n, seq):
    choices = []
    for i in range(n):
        choices.append(random.choice(seq))
    return(choices)

def AboveMinimum(l, m):
    above = []
    for i in l:
        above.append(bool(i >= m))
    return (above)

def Dices():
    return(sum([random.randint(1, 6), random.randint(1, 6)]))

def RollTheDices(bets, distScale):
    sumDices = Dices()
    win = []
    for i in bets:
        # If the bet is equal the sum of the two dices: True, else False
        win.append(bool(i == sumDices) * distScale[sumDices - 2])
    # print(sumDices)
    # # How many won ?
    # swin = sum(win)
    # if swin != 0:
    #      print(swin)
    # else:
    #      print("Nobody won")
    return (win)


x = [i for i in range(7) if i != 0]
y = []
for i in x:
    for j in x:
        y.append(i + j)
dist = []

for j in [i for i in range(13) if i > 1]:
    dist.append(y.count(j))

# Scale it to obtain 90% - 10%
distScale = [round((36 * 0.9) / i) for i in dist]
print(distScale)
class Craps(object):
    """Craps game"""
    def __init__(self, minimum):
        self.min = minimum
    def SimulateGame(self, amounts):
        bets = r(len(amounts), range(1, 12))
        w = RollTheDices(bets, distScale)
        # Check that the amount betted is superior to the minimum
        # We zip the two lists to multiply the terms of same position together
        gains = [i * j * k  for i, j, k in zip(w, amounts, AboveMinimum(amounts, self.min))]
        casinoGains = sum(amounts) - sum(gains)
        return ([casinoGains, gains])


tt = []
ctt = []
for i in range(10000):
    tt.append(Dices())
for j in [i for i in range(13) if i > 1]:
    ctt.append(tt.count(j))

print(ctt)

# print([random.randint(1, 6), random.randint(1, 6)])

