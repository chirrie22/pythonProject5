import sys
import os

# Ensure script runs correctly from subdirectories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from trading_bot.backtester.backtest import backtest, plot_results

# Example function call (ensure this exists in backtest.py)
backtest()
plot_results()
