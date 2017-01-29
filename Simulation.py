import Roulette
import Craps
import random
import Casino

def r(n, seq):
    choices = []
    for i in range(n):
        choices.append(random.choice(seq))
    return(choices)


# Monte carlo (its actually similar to just running 100 000 simulations)
casino = []
customers = []
x = []
for i in range(100):
    for j in range(1000):  # 1000 rounds
        craps = Craps.Craps(0)
        c = craps.SimulateGame(r(100, range(101)), r(100, range(2, 13)))
        casino.append(c[0])  # Amount gained by the casino
        customers.append(sum(c[1]))  # Sum of gains of the customers
    x.append(sum(customers) / (sum(customers) + sum(casino)))
    print(i)

share = [sum(x) / len(x)]
print(share)  # Very close to 0.9 each time

########################################################################################################################
########################################################################################################################

### Full Casino

# Rounds, Roulette, Craps, Customers, Bachelor, Returning, Gift, Barmen, Wage, Cash flow
# [tips, Evening, barincome, cashflow]
# parameters = [3, 10, 10, 100, 0.1, 0.5, 200, 4, 200, 50000]
#
# cashflow = []
# tips = []
# roulette = []
# craps = []
#
# for i in range(1000):
#     print(i)
#     casino = Casino.SimulateEvening(parameters)
#     Games = casino[1]
#     cashflow.append(casino[3])
#     roulette.append(Games[0])
#     craps.append(Games[1])
#     tips.append(sum(casino[0]) / parameters[7])  # Average tip for a barman in one evening
