import pandas as pd
import pandas_ta as ta
from datetime import datetime
from numpy import nan as npNaN  # Ensure compatibility with NumPy


class ScalpingVIX75Strategy:
    def __init__(self, data_fetcher, trade_executor):
        self.data_fetcher = data_fetcher
        self.trade_executor = trade_executor

    def calculate_indicators(self, data):
        """Calculate EMA, RSI, and Bollinger Bands indicators."""
        df = pd.DataFrame(data)

        # Ensure data has the required 'close' column
        if df.empty or 'close' not in df.columns:
            print("❌ Error: Market data missing or invalid.")
            return None

        df['ema9'] = ta.ema(df['close'], length=9)
        df['ema21'] = ta.ema(df['close'], length=21)
        df['rsi'] = ta.rsi(df['close'], length=14)

        # Bollinger Bands
        bb = ta.bbands(df['close'], length=20)
        if bb is not None and 'BBU_20_2.0' in bb.columns and 'BBL_20_2.0' in bb.columns:
            df['upper_band'] = bb['BBU_20_2.0']
            df['lower_band'] = bb['BBL_20_2.0']
        else:
            df['upper_band'] = npNaN
            df['lower_band'] = npNaN

        return df

    def check_buy_signal(self, df):
        """Check if buy conditions are met."""
        if len(df) < 1:
            return False  # Prevent index error

        last_row = df.iloc[-1]
        if last_row['ema9'] > last_row['ema21'] and last_row['rsi'] < 70 and last_row['close'] > last_row['lower_band']:
            print(f"[{datetime.now()}] ✅ BUY Signal detected at price {last_row['close']}")
            return True
        return False

    def check_sell_signal(self, df):
        """Check if sell conditions are met."""
        if len(df) < 1:
            return False  # Prevent index error

        last_row = df.iloc[-1]
        if last_row['ema9'] < last_row['ema21'] and last_row['rsi'] > 30 and last_row['close'] < last_row['upper_band']:
            print(f"[{datetime.now()}] ❌ SELL Signal detected at price {last_row['close']}")
            return True
        return False

    def execute_strategy(self):
        """Fetch market data and execute trades based on signals."""
        data = self.data_fetcher.fetch_data()
        df = self.calculate_indicators(data)

        if df is None or df.empty:
            print("⚠️ Skipping trade execution due to invalid or insufficient data.")
            return

        trade_size = 1000  # Default lot size
        stop_loss = 50  # Risk management
        take_profit = 100

        if self.check_buy_signal(df):
            print(f"[{datetime.now()}] 📈 Executing BUY trade at {df['close'].iloc[-1]}")
            self.trade_executor.place_trade('buy', trade_size, stop_loss=stop_loss, take_profit=take_profit)
        elif self.check_sell_signal(df):
            print(f"[{datetime.now()}] 📉 Executing SELL trade at {df['close'].iloc[-1]}")
            self.trade_executor.place_trade('sell', trade_size, stop_loss=stop_loss, take_profit=take_profit)
        else:
            print(f"[{datetime.now()}] ⚠️ No valid trade signal found.")
