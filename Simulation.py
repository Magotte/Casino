import Roulette
import Craps
import random
import Casino

def r(n, seq):
    choices = []
    for i in range(n):
        choices.append(random.choice(seq))
    return(choices)

xx = [i for i in range(2, 13)]
casino = []
customers = []
for i in range(1000):
    craps = Craps.Craps(0)
    c = craps.SimulateGame(r(100, range(101)), r(100, xx))
    casino.append(c[0]) # Amount gained by the casino
    customers.append(sum(c[1])) # Sum of gains of the customers

share = [j / (i + j) for i, j in zip(casino, customers)]
print(sum(share)/len(share))

########################################################################################################################
########################################################################################################################

### Full Casino

# Rounds, Roulette, Craps, Customers, Bachelor, Returning, Gift, Barmen, Wage, Cash flow
# [tips, Evening, barincome, cashflow]
parameters = [3, 10, 10, 100, 0.1, 0.5, 200, 4, 200, 50000]

cashflow = []
tips = []
roulette = []
craps = []

for i in range(1000):
    print(i)
    casino = Casino.SimulateEvening(parameters)
    Games = casino[1]
    cashflow.append(casino[3])
    roulette.append(Games[0])
    craps.append(Games[1])
    tips.append(sum(casino[0]) / parameters[7])  # Average tip for a barman in one evening
