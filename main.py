import matplotlib.pyplot as plt
import scienceplots

import numpy as np

from roulette import roulette


def get_mean_money(roul):
    return roul.mean_money()


def get_mean_money_loss(roul):
    return roul.mean_money_loss()


def get_mean_N_rounds(roul):
    return roul.mean_N_rounds()


def get_percent_wins(roul):
    return roul.percent_wins()


def plot_roulette(objectives, rouls, strategies, data:str, y_label:str, title:str, filename:str, location='lower right', save=False):

    functions = {"get_mean_money": get_mean_money,
                 "get_mean_money_loss": get_mean_money_loss,
                 "get_mean_N_rounds": get_mean_N_rounds,
                 "get_percent_wins": get_percent_wins}

    symbols = {"get_mean_money": "€",
                 "get_mean_money_loss": "€",
                 "get_mean_N_rounds": "",
                 "get_percent_wins": "%"}
    # Create an array for the x-axis positions
    x_positions = np.arange(len(objectives)) * len(objectives)/2

    # Set the width of the bars
    bar_width = 0.7

    y_values = []
    for i in rouls:
        y_values.append(functions[data](i))

    # Create the bar chart
    for i, strategy in enumerate(strategies):
        plt.bar(x_positions - len(strategies) * bar_width/2 + i*bar_width  + bar_width/2, y_values[i*len(objectives):(i+1)*len(objectives)], bar_width, label=strategy)
    #plt.bar(x_positions + bar_width/2, y_values[len(objectives):], bar_width, label=strategy[1])
    # Annotate the values on top of the bars
    for i, x in enumerate(x_positions):
        for j, strategy in enumerate(strategies):
            x_pos = x - len(strategies) * bar_width/2 + j*bar_width + bar_width/2
            y = y_values[j*len(objectives):(j+1)*len(objectives)][i]
            plt.text(x_pos, y + 1, str(round(y*100)/100) + symbols[data], ha='center', va='bottom')

    # Set the labels and title
    plt.xlabel('Objectives')
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(x_positions, objectives)
    plt.legend(loc=location)

    # Display the chart
    if save:
        plt.savefig(filename, dpi=600)
    plt.show()


initial_money = 100
strategy = ['Martingale', 'James Bond', 'Kerebel']
objectives = [1.05, 1.1, 1.25, 1.5, 2]
N = int(1e6)

rouls = []

for s in strategy:
    for o in objectives:
        rouls.append(roulette(s, initial_money, o , N))
        rouls[-1].run()


plot_roulette(objectives, rouls, strategy, data="get_mean_money", y_label='Average money (€)', title='Average money at the end of the simulations for different objectives', filename='plot_money.png', save=True)

plot_roulette(objectives, rouls, strategy, data="get_mean_money_loss", y_label='Average money (€)', title='Average money after a loss for different objectives', location='upper left', filename='plot_money_loss.png', save=True)

plot_roulette(objectives, rouls, strategy, data="get_mean_N_rounds", y_label='Number of rounds', title='Average number of rounds for different objectives', location='upper left', filename='plot_N_rounds.png', save=True)

plot_roulette(objectives, rouls, strategy, data="get_percent_wins", y_label='Percentage of wins (%)', title='Percentage of wins for different objectives', filename='plot_percent.png', save=True)
