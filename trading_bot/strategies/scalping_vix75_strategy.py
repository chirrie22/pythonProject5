import talib
import requests
from datetime import datetime

class ScalpingVIX75Strategy:
    def __init__(self, data_fetcher, trade_executor):
        self.data_fetcher = data_fetcher
        self.trade_executor = trade_executor

    def calculate_indicators(self, data):
        close_prices = [d['close'] for d in data]
        # Calculate EMAs
        ema9 = talib.EMA(close_prices, timeperiod=9)
        ema21 = talib.EMA(close_prices, timeperiod=21)
        # Calculate RSI
        rsi = talib.RSI(close_prices, timeperiod=14)
        # Calculate Bollinger Bands
        upper, middle, lower = talib.BBANDS(close_prices, timeperiod=20)
        return ema9, ema21, rsi, upper, lower

    def check_buy_signal(self, ema9, ema21, rsi, lower_band, close_prices=None):
        if ema9[-1] > ema21[-1] and rsi[-1] < 70 and close_prices[-1] > lower_band[-1]:
            return True
        return False

    def check_sell_signal(self, ema9, ema21, rsi, upper_band):
        if ema9[-1] < ema21[-1] and rsi[-1] > 30 and close_prices[-1] < upper_band[-1]:
            return True
        return False

    def execute_strategy(self):
        data = self.data_fetcher.fetch_data()
        ema9, ema21, rsi, upper_band, lower_band = self.calculate_indicators(data)

        if self.check_buy_signal(ema9, ema21, rsi, lower_band):
            self.trade_executor.place_trade('buy', 10)  # Example amount
        elif self.check_sell_signal(ema9, ema21, rsi, upper_band):
            self.trade_executor.place_trade('sell', 10)  # Example amount

