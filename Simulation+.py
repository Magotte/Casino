import Roulette
import Craps
import random

#### Helping functions

def SubList(which, list, amounts):  # obtain elements for a given given table (list)
    t = []
    for i in range(len(list)):
        if (list[i] == which):
            t.append(amounts[i])
    return(t)

def SortID(id, list): # Re-order a list in function of ID numbers
    x, y = zip(*sorted(zip(id, list)))
    return(y)

def AssignTypes(prop1, prop2, A, B, C, size):
    type1 = [A] * int(size*prop1)
    type2 = [B] * int(size * prop2)
    type3 = [C] * (size - len(type1) - len(type2))
    return(type1 + type2 + type3)

def AssignWealth(types):
    wealth = []
    for i in range(len(types)):
        if (types[i] == "bachelor"):
            wealth.append(random.randint(200, 500))
        elif (types[i] == "returning"):
            wealth.append(random.randint(100, 300))
        else:
            wealth.append(random.randint(200, 300))
    return wealth

def r(n, seq):
    choices = []
    for i in range(n):
        choices.append(random.choice(seq))
    return(choices)


## This class is solely implemented to gather the parameters of the casino
# class Casino(object):
#     def __init__(self, param):
#         self.rounds = param[0] # Number of rounds
#         self.nbCraps = param[1] # Number of Craps tables
#         self.nbRoulette = param[2] # Number of Roulette tables
#         self.nbC = param[3] # Number of customers
#         self.propB = param[4] # Proportion of bachelor
#         self.propR = param[5] # Proportion of returning customers
#         self.giftB = param[6] # Gift given to bachelors if they are out of money (given once)
#         self.bar = param[7] # Number of barmen
#         self.wage = param[8] # Employees evening wage
#         self.cash = param[9] # Casino starting cash flow
#         self.minR = random.choice([50, 100, 200]) # Minimum bet for Roulette (the same each evening ?)
#         self.minC = random.choice([0, 25, 50])  # Minimum bet for Craps (the same each evening ?)
#         self.types = AssignTypes(self.propB, self.propR, "bachelor", "returning", "new", self.nbC) # types of each customers
#         self.wealth = AssignWealth(self.types) # Initial wealth of each customers
#         self.ID = [i for i in range(self.nbC)] # Customers identifier to keep track of them as they change tables
#         self.Gift = [False] * self.nbC # Keeps track of whether bachelors have been bailed out already
#         self.salaries = self.wage * (self.nbCraps + self.nbRoulette + self.bar)


class Casino(object):
    def __init__(self, param):
        self.rounds = param[0]  # Number of rounds
        self.nbCraps = param[1]  # Number of Craps tables
        self.nbRoulette = param[2]  # Number of Roulette tables
        self.bar = param[7]  # Number of barmen
        self.wage = param[8]  # Employees evening wage
        self.cash = param[9]  # Casino starting cash flow
        self.salaries = self.wage * (self.nbCraps + self.nbRoulette + self.bar)

class Customer(object):
    def __init__(self, param):
        self.rounds = param[0]  # Number of rounds
        self.nbCraps = param[1]  # Number of Craps tables
        self.nbRoulette = param[2]  # Number of Roulette tables
        self.nbC = param[3] # Number of customers
        self.propB = param[4] # Proportion of bachelor
        self.propR = param[5] # Proportion of returning customers
        self.giftB = param[6] # Gift given to bachelors if they are out of money (given once)
        self.minR = random.choice([50, 100, 200]) # Minimum bet for Roulette (the same each evening ?)
        self.minC = random.choice([0, 25, 50])  # Minimum bet for Craps (the same each evening ?)
        self.types = AssignTypes(self.propB, self.propR, "bachelor", "returning", "new", self.nbC) # types of each customers
        self.wealth = AssignWealth(self.types) # Initial wealth of each customers
        self.ID = [i for i in range(self.nbC)] # Customers identifier to keep track of them as they change tables
        self.Gift = [False] * self.nbC # Keeps track of whether bachelors have been bailed out already
    # Knowing a current wealth, returns an amount bet taking into account different minimums for Craps and Roulette
    def ChooseTables(self):
        self.tables = r(self.nbC, range(1, self.nbRoulette + self.nbCraps +1))
    # The amount they bet depend on their type but also their table (for the returning type)

    def AmountsBetted(self):
        bets = []
        for i in range(self.nbC):
            if self.types[i] == "bachelor":
                bets.append(random.randint(0, self.wealth[i]))
            elif self.types[i] == "returning":
                if self.tables[i] <= self.nbRoulette and self.wealth[i] >= self.minR:
                    bets.append(self.minR)
                elif self.tables[i] > self.nbRoulette and self.wealth[i] >= self.minC:
                    bets.append(self.minC)
                else:
                    bets.append(0)
            else:
                bets.append(random.randint(0, self.wealth[i]//3))
        self.amounts = bets

    def UpdateWealth(self, gains, drinkstips):
        self.wealth = [i - j + k for i, j, k in zip(gains, drinkstips, self.wealth)]
        for i in range(self.nbC):
            if self.wealth[i] == 0 and self.Gift[i] is False and self.types[i] == "bachelor":
                self.wealth[i] = self.giftB
                self.Gift[i] = True

l = [3, 10, 10, 5, 0.1, 0.5, 200, 4, 200, 50000]
c = Customer(l)
print(c.wealth)
c.UpdateWealth([10] * 5, [1] * 5)
print(c.wealth)

class Bar(object):
    def __init__(self, param, wealth):
        self.nbC = param[3]  # Number of customers
        self.bar = param[7]  # Number of barmen
        # In-between each rounds, customers would like to order 0, 1, or 2 times without considering their budget
        # If they have more than 60$ they by drinks else nothing
        self.orders = r(self.nbC, [0, 1, 2])
        # Each barmen can take orders (put a limit afterwards): Assigns customers to any of them randomly
        self.barmen = r(self.nbC, range(1, self.bar + 1))
        self.spend = [i * j * 20 * bool(k > (60 * j)) for i, j, k in zip(r(self.nbC, [1, 2]), self.orders, wealth)]
        self.tips = [i * bool(j > 0) for i, j in zip(r(self.nbC, range(21)), self.spend)]

# class Customer(Casino):
#     # Knowing a current wealth, returns an amount bet taking into account different minimums for Craps and Roulette
#     def ChooseTables(self):
#         self.tables = r(self.nbC, range(1, self.nbRoulette + self.nbCraps +1))
#     # The amount they bet depend on their type but also their table (for the returning type)
#
#     def AmountsBetted(self):
#         bets = []
#         for i in range(self.nbC):
#             if self.types[i] == "bachelor":
#                 bets.append(random.randint(0, self.wealth[i]))
#             elif self.types[i] == "returning":
#                 if self.tables[i] <= self.nbRoulette and self.wealth[i] >= self.minR:
#                     bets.append(self.minR)
#                 elif self.tables[i] > self.nbRoulette and self.wealth[i] >= self.minC:
#                     bets.append(self.minC)
#                 else:
#                     bets.append(0)
#             else:
#                 bets.append(random.randint(0, self.wealth[i]//3))
#         self.amounts = bets
#
#     # Update Customers wealth by overriding the wealth attribute (and the "gift tracker" attribute)
#     def UpdateWealth(self, gains, drinkstips):
#         self.wealth = [i - j + k for i, j, k in zip(gains, drinkstips, self.wealth)]
#         for i in range(self.nbC):
#             if self.wealth[i] == 0 and self.Gift[i] is False and self.types[i] == "bachelor":
#                 self.wealth[i] = self.giftB
#                 self.Gift[i] = True
#
# # Customers should have a probability to go to the bar (once or more) in-between each round where they get 1 or 2 drinks
# # Under class customer for the wealth update
#
#
# class Bar(Customer):
#     # In-between each rounds, customers would like to order 0, 1, or 2 times without considering their budget
#     # If they have more than 60$ they by drinks else nothing
#     def Orders(self):
#         self.orders = r(self.nbC, [0, 1, 2])
#     # Each barmen can take orders (put a limit afterwards): Assigns customers to any of them randomly
#         self.barmen = r(self.nbC, range(1, self.bar + 1))
#         self.spend = [i * j * 20 * bool(k > (60 * j)) for i, j, k in zip(r(self.nbC, [1, 2]), self.orders, self.wealth)]
#         self.tips = [i * bool(j > 0) for i, j in zip(r(self.nbC, range(21)), self.spend)]

# Rounds, Roulette, Craps, Customers, Bachelor, Returning, Gift, Barmen, Wage, Cash flow
l = [3, 10, 10, 100, 0.1, 0.5, 200, 4, 200, 50000]

# print(bar.spend)
# print(bar.wealth)


def SimulateEvening(param):
    # Set up the evening
    casino = Casino(param)
    customers = Customer(param)
    # Set up the first series of drinks orders
    bar = Bar(param, customers.wealth)
    # Customers can order drinks before playing
    eveningtable = [0] * (casino.nbRoulette + casino.nbCraps)
    barincome = 0
    customers.UpdateWealth([0] * customers.nbC, [i + j for i, j in zip(bar.spend, bar.tips)])
    for i in range(1, casino.rounds):
        # Set up the order at the bar and make customers by drinks before even starting a round
        # Generate tables
        customers.ChooseTables()
        # Generate amounts bet
        customers.AmountsBetted()
        # result stores the gains of the players: 0 or a positive number
        # MixedId stores the Id number of the players in "table order"
        # TableIncome stores the income of the tables for one round (negative or positive)
        result = []
        mixedid = []
        tableincome = []
    # return [min([i - j for i, j in zip(w, customers.wealth)]), customers.wealth, w]

        # Roulette tables
        for i in range(1, casino.nbRoulette + 1):
            r = Roulette.Roulette(customers.minR)
            mixedid += SubList(i, customers.tables, customers.ID)
            store = r.SimulateGame(SubList(i, customers.tables, customers.amounts))  # For a specific table
            tableincome.append(store[0])
            result = result + store[1]
        # Craps tables
        for i in range(casino.nbRoulette + 1, casino.nbRoulette + casino.nbCraps + 1):
            c = Craps.Craps(customers.minC)
            mixedid += SubList(i, customers.tables, customers.ID)
            store = c.SimulateGame(SubList(i, customers.tables, customers.amounts))
            tableincome.append(store[0] * (1 - bool(store[0] > 0) * 0.005))  # Table benefit minus croupier bonus
            result = result + store[1]
        # Recover the outcomes for every customers in same order as before splitting
        alloutcomes = [i - j for i, j in zip(SortID(mixedid, result), customers.amounts)]
        customers.UpdateWealth(alloutcomes, [0] * customers.nbC)
        # And update their budget for next round with their new drinks expenditures
        bar = Bar(param, customers.wealth)
        barincome += sum(bar.spend)
        customers.UpdateWealth([0] * customers.nbC, [i + j for i, j in zip(bar.spend, bar.tips)])
        eveningtable = [i + j for i, j in zip(eveningtable, tableincome)]  # Keeps track of revenues for all tables across rounds
    # Revenues for different games
    Evening = [sum(eveningtable[0:(casino.nbRoulette - 1)])]  # Roulette results
    Evening += [sum(eveningtable[casino.nbRoulette:len(eveningtable)])]  # Craps results
    cashflow = casino.cash + sum(Evening) + barincome - casino.salaries
    return [Evening, cashflow]
test = SimulateEvening(l)
print(test)
