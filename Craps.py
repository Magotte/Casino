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
    return above

def Dices():
    return sum([random.randint(1, 6), random.randint(1, 6)])

def RollTheDices(bets, distScale):
    sumDices = Dices()
    win = []
    for i in bets:
        # If the bet is equal the sum of the two dices: True, else False
        # if the sum of dices is 2 which is the minimum then the corresponding rescaling is in the first element
        # of the list distScale
        win.append(bool(i == sumDices) * distScale[sumDices - 2])
    # print(sumDices)
    # # How many won ?
    # swin = sum(win)
    # if swin != 0:
    #      print(swin)
    # else:
    #      print("Nobody won")
    return win


# Scaling function to obtain 90% for th players and 10% for the casino
def Scale():
    sums = []
    for i in range(1, 7):
        for j in range(1, 7):
            sums.append(i + j)
    dist = []
    for k in range(2, 13):
        dist.append((36 * 0.9) / sums.count(k))
    return dist
distScale = Scale()

class Craps(object):
    """Craps game"""
    def __init__(self, minimum):
        self.min = minimum
    def SimulateGame(self, amounts, bets):
        w = RollTheDices(bets, distScale)
        # Check that the amount betted is superior to the minimum
        # We zip the two lists to multiply the terms of same position together
        gains = [i * j * k for i, j, k in zip(w, amounts, AboveMinimum(amounts, self.min))]
        casinoGains = sum(amounts) - sum(gains)
        return [casinoGains, gains]

