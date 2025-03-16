# plot_result_utils.py

import matplotlib.pyplot as plt

def plot_results(trade_history):
    """Plots the balance over time."""
    plt.plot(trade_history)
    plt.xlabel("Time")
    plt.ylabel("Balance")
    plt.title("Trading Performance Over Time")
    plt.show()
