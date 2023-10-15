import numpy as np
from numpy.random import randint


class roulette(object):

    def __init__(self, method:str, initial_money:int, objective:float, N:int):
        """
        initiate the object,

        Arguments :

        method, str: The method of betting that should be used, either martingale or all-in:
        - The Martingale method is based on the idea of doubling your bet each round, this methods guaranties a win of your initial bet, given that you have infinite money.
        - The all-in method is less sofisticated, the point is to bet all the money necessary to get to your objective gain. e.g. if you have 100€ and want to get to 125€, you will bet 25€, if you win you stop, if you lose, you bet 50€ (75€ + 50€ = 125€) or in general, if you have an objective N and money m, you bet N-m.
        initial_money, int: The amount of money to start the simulations and play on the roulette.
        objective, float: The objective after which we stop playing as a proportion of the initial money, e.g. if the objective is 1.5 and the initial money is 100, the simulation stops either when we reach an amount of money > 150 or we can't play anymore.
        N, int: is the number of simulation to do.
        """

        self.method = method
        self.initial_money = initial_money
        self.objective = objective
        self.N = N
        
        self.money_end = []
        self.money_lost = []
        self.N_rounds = []
        self.money_earned = 0

        self.reds = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.blacks = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]


    def run(self):

        if self.method.lower() == "martingale":
            self.martingale()
        elif "allin" in self.method.lower() or "all-in" in self.method.lower() or "kerebel" in self.method.lower():
            self.kerebel()
        elif "red even" in self.method.lower() and "martingale" in self.method.lower():
            self.red_even_martingale()
        elif "alembert" in self.method.lower():
            self.dalembert()
        elif "bond" in self.method.lower() or "007" in self.method.lower():
            self.bond()
        else:
            raise ValueError(f"The method : {self.method}, has not been implemented, only the martingale, the all-in or the red-even strategies have been implemented")


    def roll(self, betting_on, bets):
        for i in bets:
            self.money -= i
            
        result = randint(0, 36+1)
        win = False
        
        for bet_on, bet in zip(betting_on, bets):
            if result == bet_on:
                self.money += 36*bet
                win = True
            if result > 0 and "even" == bet_on and result%2 == 0:
                self.money += 2*bet
                win = True
            if result > 0 and "odd" == bet_on and result%2 == 2:
                self.money += 2*bet
                win = True
            if result in self.reds and "red" == bet_on:
                self.money += 2*bet
                win = True
            if result in self.blacks and "black" == bet_on:
                self.money += 2*bet
                win = True
            if result > 18 and "high" == bet_on:
                self.money += 2*bet
            if (result >0 and result<19) and "low" == bet_on:
                self.money += 2*bet
        return win

    def martingale(self, increment:int=2):

        for i in range(self.N):
            self.money = self.initial_money
            self.bet = 1
            self.n_round = 0
            self.done = False

            while not self.done:
                self.n_round += 1

                win = self.roll(["red"], [self.bet])
                if win:
                    self.bet = 1
                else:
                    self.bet *= increment

                if self.bet > self.money:
                    self.money_end.append(self.money)
                    self.money_lost.append(self.money)
                    self.N_rounds.append(self.n_round)
                    self.done = True

                if self.money >= self.objective*self.initial_money:
                    self.money_end.append(self.money)
                    self.N_rounds.append(self.n_round)
                    self.done = True

    def kerebel(self, hard=False):

        for i in range(self.N):
            self.money = self.initial_money
            self.bet = self.objective*self.initial_money - self.money
            self.n_round = 0
            self.done = False

            while not self.done:
                self.n_round += 1

                self.roll(["red"], [self.bet])

                self.bet = self.objective*self.initial_money - self.money

                if (hard and self.money == 0) or (not hard and self.bet > self.money):
                    self.money_end.append(self.money)
                    self.money_lost.append(self.money)
                    self.N_rounds.append(self.n_round)
                    self.done = True

                if self.money >= self.objective*self.initial_money:
                    self.money_end.append(self.money)
                    self.N_rounds.append(self.n_round)
                    self.done = True

    def red_even_martingale(self):

        for i in range(self.N):
            self.money = self.initial_money
            self.bet = 1
            self.n_round = 0
            self.done = False

            while not self.done:
                self.n_round += 1

                win = self.roll(["red", "even"], [self.bet, self.bet])

                if win:
                    self.bet = 1
                else:
                    self.bet *= 2
            
                if self.bet > self.money:
                    self.money_end.append(self.money)
                    self.money_lost.append(self.money)
                    self.N_rounds.append(self.n_round)
                    self.done = True

                if self.money >= self.objective*self.initial_money:
                    self.money_end.append(self.money)
                    self.N_rounds.append(self.n_round)
                    self.done = True

    def dalembert(self, increment:int=2):

        for i in range(self.N):
            self.money = self.initial_money
            self.bet = 1
            self.n_round = 0
            self.done = False

            while not self.done:
                self.n_round += 1

                win = self.roll(["red"], [self.bet])
                if win:
                    self.bet = 1
                else:
                    self.bet += increment

                if self.bet > self.money:
                    self.money_end.append(self.money)
                    self.money_lost.append(self.money)
                    self.N_rounds.append(self.n_round)
                    self.done = True

                if self.money >= self.objective*self.initial_money:
                    self.money_end.append(self.money)
                    self.N_rounds.append(self.n_round)
                    self.done = True

    def bond(self):

        for i in range(self.N):
            self.money = self.initial_money
            self.bet = int(10*self.money/200*100)/100  # We only keep 2 digits after the .
            line_bet = int(5/6*self.bet*100)/100
            self.n_round = 0
            self.done = False

            while not self.done:
                self.n_round += 1

                win = self.roll([0, 13, 14, 15, 16, 17, 18, "high"], [self.bet, line_bet, line_bet, line_bet, line_bet, line_bet, line_bet, 14*self.bet])
            
                if 20*self.bet > self.money:
                    self.money_end.append(self.money)
                    self.money_lost.append(self.money)
                    self.N_rounds.append(self.n_round)
                    self.done = True
                    
                if self.money >= self.objective*self.initial_money:
                    self.money_end.append(self.money)
                    self.N_rounds.append(self.n_round)
                    self.done = True

    def mean_money(self):
        return np.mean(self.money_end)

    def mean_money_loss(self):
        return np.mean(self.money_lost)

    def mean_N_rounds(self):
        return np.mean(self.N_rounds)

    def percent_wins(self):
        return (self.N - len(self.money_lost)) / self.N * 100
