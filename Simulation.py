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

share = sum(x) / len(x)
print(share)  # Very close to 0.9 each time

########################################################################################################################
########################################################################################################################

### Full Casino

# Rounds, Roulette, Craps, Customers, Bachelor, Returning, Gift, Barmen, Wage, Cash flow
# returns [tips, Evening, barincome, cashflow]


cashflow = [50000]
tips = []
roulette = []
craps = []
nbsim = 1000
for i in range(nbsim):
    parameters = [3, 10, 10, 100, 0.1, 0.5, 200, 4, 200, cashflow[i]]
    casino = Casino.SimulateEvening(parameters)
    Games = casino[1]
    cashflow.append(casino[3])
    if cashflow[i] < 0:
        print("Not Good")
        break
    roulette.append(Games[0])
    craps.append(Games[1])
    tips.append(sum(casino[0]) / parameters[7])  # Average tip for a barman in one evening


print(max(cashflow) / cashflow[0])  # The cash flow increases by  about 60 times its initial value after 1000 evening
print(sum(roulette), sum(craps))  # Income from roulette more than double (it was to be expected)
print(sum(tips) / nbsim)  # 464 in average for 1000 simulation
# It seems that giving a lot as starting budget still is ok for the casino: there is only 10 bachelors and they do bet
# more than the others (it even worked with 200K).


# Can't plot...
def AffineFit(y, x):
    # Linear fit
    if y[0] == 0:
        return sum(y) / sum(x)
    else:
        # Affine fit
        obs = len(y)
        # x'x
        x11 = sum(x)
        x12 = sum([i * j for i , j in zip(x, x)])
        x21 = sum(x)
        x22 = obs
        # xy
        y1 = sum([i * j for i , j in zip(y, x)])
        y2 = sum(y)
        # determinant
        det = x11 * x22 - x12 * x21
        beta0 = (x22 * y1 - x12 * y2) / det
        beta1 = (x11 * y2 - x21 * y1) / det
        return [beta0, beta1]

# print(AffineFit(cashflow, range(1, nbsim + 1)))  # Seems to work but bad fit... there is a lot of variation
                                                 # although there should be a linear trend
# print(AffineFit([i - j for i, j in zip(cashflow, [cashflow[0]] * len(cashflow))], range(1, nbsim + 1)))

# I wanted to fit the evolution of the cash flow (or other) and compare the different slopes estimates (beta1)
# with different parameters but it seems that there is too much variation due to all the randomness in an evening
# simulation to recover a proper interpretation
# A beta1 being close to 0 would have meant a flat evolution and so a level representing a limit at which
# if casino parameters are increased the casino can't sustain its expanses anymore

