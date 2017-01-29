import random

def r(n, seq):
    choices = []
    for i in range(n):
        choices.append(random.choice(seq))
    return(choices)


# Returns True if the element inside a list is superior to min
# Takes a list and an integer as argument
def AboveMinimum(l, m):
    above = []
    for i in l:
        above.append(bool(i >= m))
    return (above)

def SpinTheWheel(bets):
    # Number at which the wheel stops
    stop = random.randint(0, 36)
    # Win = True, Lost = False
    win = []
    for i in bets:
        # If the bet is equal stop: True, else False
        win.append(bool(i == stop))
    print("It stopped at %s" %(stop))
    # How many won ?
    if sum(win) > 1:
        print("%s players won" %(sum(win)))
    elif sum(win) == 1:
        print("One player won")
    else:
        print("Nobody won")
    return (win)
class Roulette(object):
    """Roulette game"""
    def __init__(self, minimum):
        self.min = minimum

    def SimulateGame(self, amounts, bets):
        w = SpinTheWheel(bets)
        # Check that the amount betted is superior to the minimum
        # We zip the two lists to multiply the terms of same position together
        gains = [i * j * k * 30 for i, j, k in zip(w, amounts, AboveMinimum(amounts, self.min))]
        casinoGains = sum(amounts) - sum(gains)
        return [casinoGains, gains]

rou = Roulette(0)
rou.SimulateGame(r(100, range(101)), r(100, range(36)))