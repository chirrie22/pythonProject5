import pandas as pd
import os

# Get the correct file path
data_path = os.path.join(os.path.dirname(__file__), "data.csv")


def load_data():
    """Load data from CSV file."""
    if not os.path.exists(data_path):
        print(f"Error: File {data_path} not found.")
        return None
    return pd.read_csv(data_path)


def calculate_sma(data, window=2):
    """Calculate Simple Moving Average (SMA)."""
    data["SMA"] = data["price"].rolling(window=window).mean()
    return data


def simulate_trades(data, sl=0.02, tp=0.03):
    """Simulate trades using SMA strategy with Stop-Loss (SL) & Take-Profit (TP)."""
    balance = 1000  # Starting balance
    position = None
    trade_log = []

    data = calculate_sma(data)

    for i in range(len(data) - 1):
        current_price = data.loc[i, "price"]
        next_price = data.loc[i + 1, "price"]
        current_sma = data.loc[i, "SMA"]

        if pd.isna(current_sma):  # Skip if SMA is NaN
            continue

        # Buy Condition: Price above SMA
        if position is None and current_price > current_sma:
            position = current_price
            trade_log.append(f"BUY at {current_price}")

        # Check SL/TP conditions
        elif position is not None:
            sl_price = position * (1 - sl)  # Stop-Loss price
            tp_price = position * (1 + tp)  # Take-Profit price

            if current_price <= sl_price:
                loss = sl_price - position
                balance += loss
                trade_log.append(f"STOP-LOSS triggered at {sl_price}, Loss: {loss}")
                position = None
            elif current_price >= tp_price:
                profit = tp_price - position
                balance += profit
                trade_log.append(f"TAKE-PROFIT triggered at {tp_price}, Profit: {profit}")
                position = None
            elif current_price < current_sma:
                profit = current_price - position
                balance += profit
                trade_log.append(f"SELL at {current_price}, Profit: {profit}")
                position = None

    return balance, trade_log


def run_backtest():
    """Run the backtest process."""
    print(f"Looking for data at: {data_path}")
    print("Running backtest...")

    data = load_data()
    if data is None:
        print("No valid data available for trade simulation.")
        return

    print("Data loaded successfully!")
    print(data, "\n")

    final_balance, trades = simulate_trades(data)

    print("\nTrade Log:")
    for trade in trades:
        print(trade)

    print(f"\nFinal Balance: {final_balance}")


if __name__ == "__main__":
    run_backtest()
