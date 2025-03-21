import logging
import pandas as pd
import time
from trading_bot.strategies.deriv_strategy import DerivStrategy
from trading_bot.data_fetchers.live_data_fetcher import LiveDataFetcher

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Backtester:
    def __init__(self, initial_balance=1000, symbol="R_75"):
        self.strategy = DerivStrategy()
        self.fetcher = LiveDataFetcher(symbol)
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.trade_log = []
        self.position = None

    def run(self):
        """Runs the backtester using live data."""
        self.fetcher.start_stream()  # Start fetching live data

        while True:
            if not self.fetcher.live_data:
                time.sleep(1)  # Wait if no data yet
                continue

            market_data = self.fetcher.live_data.pop(0)  # Get latest tick
            signal = self.strategy.calculate_signal(market_data)

            if signal == "BUY" and not self.position:
                self.position = market_data['price']
                self.trade_log.append(("BUY", market_data['timestamp'], market_data['price']))
                logging.info(f"BUY at {market_data['price']} on {market_data['timestamp']}")

            elif signal == "SELL" and self.position:
                profit = market_data['price'] - self.position
                self.balance += profit
                self.trade_log.append(("SELL", market_data['timestamp'], market_data['price'], profit))
                logging.info(f"SELL at {market_data['price']} on {market_data['timestamp']} | Profit: {profit}")
                self.position = None

        self.evaluate()

    def evaluate(self):
        """Evaluates the trading performance."""
        total_profit = self.balance - self.initial_balance
        win_rate = sum(1 for trade in self.trade_log if trade[0] == "SELL" and trade[3] > 0) / max(1, len(self.trade_log) // 2)
        logging.info(f"Final Balance: {self.balance}")
        logging.info(f"Total Profit: {total_profit}")
        logging.info(f"Win Rate: {win_rate * 100:.2f}%")

if __name__ == "__main__":
    backtester = Backtester(symbol="R_75")
    backtester.run()
