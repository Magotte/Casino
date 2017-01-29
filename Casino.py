import random
import math


################ Helping functions

########################################################################################################################
########################################################################################################################

### Roulette and Craps

# Draws a random vector with replacement
def r(n, seq):
    choices = []
    for i in range(n):
        choices.append(random.choice(seq))
    return choices


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
        win.append(bool(i == sumDices) * distScale[sumDices - 2])
    return win


def SpinTheWheel(bets):
    stop = random.randint(0, 36)
    win = []
    for i in bets:
        win.append(bool(i == stop))
    return win


def Scale():
    sums = []
    for i in range(1, 7):
        for j in range(1, 7):
            sums.append(i + j)
    dist = []
    for k in range(2, 13):
        dist.append(round((36 * 0.9) / sums.count(k)))
    return dist
distScale = Scale()

########################################################################################################################
########################################################################################################################

### Functions for classes attributes

# For every ocurrence of number "which" in "list", returns the elements in "amounts" that are at the same indexes
# Amounts bet and tables are predetermined before a game: This function helps in dispatching amounts bet to the
# corresponding table and keeping track of the customers (by ID) to be able to reupdate their state after a game
def SubList(which, list, amounts):
    t = []
    for i in range(len(list)):
        if (list[i] == which):
            t.append(amounts[i])
    return t


# Sorts a list in increasing numbers: Helps in recovering players states after they hava been dispatched to
# different tables and played
def SortID(id, list):
    x, y = zip(*sorted(zip(id, list)))
    return y


# Assigns a type for each customers taking into account the proportions of each types (a share of prop1 for type A)
def AssignTypes(prop1, prop2, A, B, C, size):
    type1 = [A] * int(size*prop1)
    type2 = [B] * int(size * prop2)
    type3 = [C] * (size - len(type1) - len(type2))
    return type1 + type2 + type3


# Knowing the type of each customers bachelor,returning or new (one-timers) we give them a starting budget (wealth)
# according to the advised parameters.
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


# I decided to put a limit on how many orders barmen can handle (20 each). Indeed, if there is no limit the casino
# is better of having only one barman handling all orders as it would then pay only one wage
# The funtion randomly picks customers (called the unlucky customers) who will not be served
# "orders" is a list of number of orders for each customers (takes 0, 1 or 2)
# The ones ordering twice can be picked twice
# "nb" is the number of barmen and capacity is fixed to 20
# For simplicity, barmen can complete each others: what matters is their total capacity but of course at the end some
# will get more tips than others
def PickCustomers(orders, nb, capacity):
    # Which customers orders ?
    which = SubList(1, orders, [i for i in range(len(orders))]) + SubList(2, orders, [i for i in range(len(orders))])
    # Randomly choose them. This draws random vectors without replacement (pip didn't work at that time so I couldn't
    # install numpy) and is computationally demanding but works properly.
    unlucky = [random.choice(which)]
    while  len(unlucky) != (sum(orders) - nb * capacity):
        x = random.choice(which)
        if unlucky.count(x) == 0 or (orders[x] == 2 and unlucky.count(x) == 1):
            unlucky.append(x)
    picked = [0] * len(orders)
    for i in unlucky:
        picked[i] += 1
    return picked
    # Returns a vector of 0, 1 or 2 giving customers that are not served once or twice (of course, only the customers
    # who wanted to order twice can be "unlucky" twice)
    # It can happen that a customer who wanted to order twice is not served at all and someone who only wanted to order
    # once is actually served. There is no priority for bigger consumers.

########################################################################################################################
########################################################################################################################

### Classes

# This class solely gathers parameters that don't vary in one evening
# Helps to keep the code clear: if we have "casino.  " we know it is a fixed parameter
# Having only attributes actually reduces assignment in the main code and its clarity
class Casino(object):
    def __init__(self, param):
        self.rounds = param[0]  # Number of rounds
        self.nbCraps = param[1]  # Number of Craps tables
        self.nbRoulette = param[2]  # Number of Roulette tables
        self.bar = param[7]  # Number of barmen
        self.wage = param[8]  # Employees evening wage
        self.cash = param[9]  # Casino starting cash flow
        self.salaries = self.wage * (self.nbCraps + self.nbRoulette + self.bar)  # Labor expenses


# Customer state can vary inside a same evening (her wealth, the amounts she bets, the tables she goes)
class Customer(object):
    def __init__(self, param):
        self.rounds = param[0]  # Number of rounds
        self.nbCraps = param[1]  # Number of Craps tables
        self.nbRoulette = param[2]  # Number of Roulette tables
        self.nbC = param[3]  # Number of customers
        self.propB = param[4]  # Proportion of bachelor
        self.propR = param[5]  # Proportion of returning customers
        self.giftB = param[6]  # Gift given to bachelors if they are out of money (given once)
        self.minR = random.choice([50, 100, 200]) # Minimum bet for Roulette (the same each evening ?)
        self.minC = random.choice([0, 25, 50])  # Minimum bet for Craps (the same each evening ?)
        self.types = AssignTypes(self.propB, self.propR, "bachelor", "returning", "new", self.nbC)
        self.wealth = AssignWealth(self.types)  # Initial wealth of each customers
        self.ID = [i for i in range(self.nbC)]  # Customers identifier to keep track of them as they change tables
        self.Gift = [False] * self.nbC  # Keeps track of whether bachelors have been bailed out already

    # Randomly choose tables: the first ones are the Roulette tables (from 1 to nbRoulette or 1 to 10 in the set-up)
    # and the others the Craps tables
    def ChooseTables(self):

        self.tables = r(self.nbC, range(1, self.nbRoulette + self.nbCraps + 1))

    # The amount they bet depend on their type but also their table (for the returning type)
    # As for the barmen. I decided to add a restriction on the number of players at one table
    # If there is more than 10 players at a table, some customers get shy and don't play
    # 1 out of three do not play in average (it does not depend on type).
    def AmountsBetted(self):
        bets = []
        plays = []
        for i in range(self.nbC):
            if self.tables.count(self.tables[i]) < 10:  # if less than 10 tables, customers plays
                plays.append(True)
            else:
                plays.append(random.choice([False, True, True]))  # if not, plays with probability 2/3
        for i in range(self.nbC):
            if self.types[i] == "bachelor":  # if bachelor: can bet all her wealth (and if table not crowded or not shy)
                bets.append(random.randint(0, self.wealth[i]) * plays[i])
            elif self.types[i] == "returning":  # if returning:, plays the minimum or nothing if her wealth is small
                if self.tables[i] <= self.nbRoulette and self.wealth[i] >= self.minR:
                    bets.append(self.minR * plays[i])
                elif self.tables[i] > self.nbRoulette and self.wealth[i] >= self.minC:
                    bets.append(self.minC * plays[i])
                else:
                    bets.append(0)
            else:  # if new: plays from 0 to one third of her budget
                bets.append(random.randint(0, self.wealth[i]//3) * plays[i])
        self.amounts = bets

    # Updates wealth after a game
    def AfterRound(self, gains):
        for i in range(self.nbC):
            self.wealth[i] += gains[i]
            # I decided that the gift is given to bachelors if their wealth is inferior to 20:
            # "If you lost so much that you can't afford a drink, we will bail you out"
            # It makes the probability of giving a new starting budget higher and makes this aspect of the Casino
            # more interesting to study
            # self.Gift helps in checking whether some customers have already been granted a new starting budget
            if self.types[i] == "bachelor" and self.wealth[i] < 20 and self.Gift[i] is False:
                self.wealth[i] += self.giftB
                self.Gift[i] = True

    # Updates wealth after hitting the bar
    def AfterBar(self, drinks, tips):
        self.wealth = [i - j - k for i, j, k in zip(self.wealth, drinks, tips)]


class Bar(object):
    def __init__(self, param):
        self.nbC = param[3]  # Number of customers
        self.bar = param[7]  # Number of barmen
        # Each barmen can take orders: Assigns customers to any of them randomly
        self.barmen = r(self.nbC, range(1, self.bar + 1))

    # Generates expenditures in drinks, tips and the corresponding bonus (tips) for barmen
    # Customers left budget have to be checked (the 60$ limit for one order)
    # To make it even more important for the casino to have an appropriate number of tables, I decided that customers
    # who didn't bet are not happy and do not want to drink
    def Orders(self, wealth, amounts):
        spend = []
        tips = []
        # In-between each rounds, customers would like to order 0, 1, or 2 times without considering their budget
        # If they have more than 60$ they by drinks else nothing
        orders = r(self.nbC, [0, 1, 2])
        barmantips = [0] * self.bar
        if sum(orders) > self.bar * 20:  # Taking into account the bar capacity
            # Decrease the number of orders of the unlucky
            orders = [i - j for i, j in zip(orders, PickCustomers(orders, self.bar, 20))]
        for i in range(self.nbC):
            # If she doesn't want to drink or doesn't have the money or is not happy...
            if orders[i] == 0 or wealth[i] < 60 or amounts[i] == 0:
                spend.append(0)  # ... she does not spend money at the bar
                tips.append(0)   # and so does not tip
            else:  # if she has the money, she wants to drink and she played beforehand...
                spend.append(random.choice([1, 2]) * 20)  # ... she randomly picks between 1 and 2 drinks for 20$ each
                tips.append(random.choice(range(21)))  # and tips between 1 and 20
            if orders[i] == 2 and wealth[i] - spend[i] - tips[i] >= 60:  # if she wants to order a second time
                spend[i] += random.choice([1, 2]) * 20  # Same thing
                tips[i] += random.choice(range(21))     # Same thing
            barmantips[self.barmen[i] - 1] += tips[i]  # Store the total tips of the salve for each barmen
        self.drinks = spend
        self.tips = tips
        self.barmantips = barmantips

class Roulette(object):
    """Roulette game"""
    def __init__(self, minimum):
        self.min = minimum

    def SimulateGame(self, amounts):
        bets = r(len(amounts), range(37))
        w = SpinTheWheel(bets)
        # Check that the amount betted is superior to the minimum
        # We zip the two lists to multiply the terms of same position together
        gains = [i * j * k * 30 for i, j, k in zip(w, amounts, AboveMinimum(amounts, self.min))]
        casinoGains = sum(amounts) - sum(gains)
        return [casinoGains, gains]

class Craps(object):
    """Craps game"""
    def __init__(self, minimum):
        self.min = minimum

    def SimulateGame(self, amounts):
        bets = r(len(amounts), range(2, 13))
        w = RollTheDices(bets, distScale)
        # Check that the amount bet is superior to the minimum
        # We zip the two lists to multiply the terms of same positions together
        gains = [i * j * k for i, j, k in zip(w, amounts, AboveMinimum(amounts, self.min))]
        casinoGains = sum(amounts) - sum(gains)
        return [casinoGains, gains]

########################################################################################################################
########################################################################################################################

### Main code

def SimulateEvening(param):
    # Set up the evening
    casino = Casino(param)
    customers = Customer(param)
    # Set up the first series of drinks orders
    bar = Bar(param)
    # Customers can order drinks before playing and they all want to drink (virtual bet amounts different from 0)
    bar.Orders(customers.wealth, [1] * bar.nbC)
    # Update customers wealth
    customers.AfterBar(bar.drinks, bar.tips)
    # Store the bar income (only comes from drinks as a 100% profit)
    barincome = sum(bar.drinks)
    # "eveningtable" stores the income for each tables for the evening
    eveningtable = [0] * (casino.nbRoulette + casino.nbCraps)
    # Store barmen tips for the first salve
    tips = bar.barmantips
    # Each round: Customers play and go to the bar
    for i in range(1, casino.rounds):
        customers.ChooseTables()  # Dispatch to tables
        customers.AmountsBetted()  # Generate amounts bet
        # result stores the gains of players: 0 or a positive number (their bet times the coefficient: 30 for Roulette)
        result = []
        mixedid = []  # mixedid stores the Id number of the players in "table order" (so mixed)
        tableincome = []  # tableincome stores the income of the tables for one round (negative or positive)

        # Roulette tables
        for j in range(1, casino.nbRoulette + 1):  # 1 to 10 Roulette
            r = Roulette(customers.minR)  # Generate the object Roulette
            mixedid += SubList(j, customers.tables, customers.ID)  # Keep track of the customers at this table (table "i")
            # Outcome for this specific table: casino gain, customers gains: [casino, [player1, player2, ...]]
            store = r.SimulateGame(SubList(j, customers.tables, customers.amounts))
            # Table income minus the croupiers bonus (0.5%). I keep everything in integer.
            tableincome.append(math.ceil(store[0] * (1 - bool(store[0] > 0) * 0.005)))
            result += store[1]  # append the customers gains (they are mixed)

        # Craps tables (similar to Roulette)
        for k in range(casino.nbRoulette + 1, casino.nbRoulette + casino.nbCraps + 1):  # 11 to 20 Craps
            c = Craps(customers.minC)
            mixedid += SubList(k, customers.tables, customers.ID)
            store = c.SimulateGame(SubList(k, customers.tables, customers.amounts))
            tableincome.append(math.ceil(store[0] * (1 - bool(store[0] > 0) * 0.005)))
            result += store[1]

        # Recover the outcomes for every customers in same order as before dispatching
        alloutcomes = [i - j for i, j in zip(SortID(mixedid, result), customers.amounts)]
        customers.AfterRound(alloutcomes)  # Update wealth after the round
        bar.Orders(customers.wealth, alloutcomes)  # Generate new orders, expenditures, tips...
        tips = [i + j for i, j in zip(tips, bar.barmantips)]   # Add tips to the previous tips for each barmen
        barincome += sum(bar.drinks)  # Same thing for the casino bar income
        customers.AfterBar(bar.drinks, bar.tips)  # Update customers wealth after hitting the bar
        # Add the round income to the total current income
        eveningtable = [i + j for i, j in zip(eveningtable, tableincome)]
    # Revenues for different games
    Evening = [sum(eveningtable[0:(casino.nbRoulette - 1)])]  # Roulette revenues
    Evening += [sum(eveningtable[casino.nbRoulette:len(eveningtable)])]  # Craps revenues
    cashflow = casino.cash + sum(Evening) + barincome - casino.salaries - sum(customers.Gift) * 200  # New cash flow
    return [tips, Evening, barincome, cashflow]
    # Returns lists and vectors: [list, list, int, int]


# # Rounds, Roulette, Craps, Customers, Bachelor, Returning, Gift, Barmen, Wage, Cash flow
# l = [3, 10, 10, 100, 0.1, 0.5, 200, 4, 200, 50000]
# test = SimulateEvening(l)
# print(test)

