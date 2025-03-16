import pandas as pd

def simulate_trades(data):
    print("Simulating trades...")

    if data.empty:
        return pd.DataFrame()  # Return empty DataFrame if no data

    # Example strategy: Buy when price drops, sell when it rises
    trades = []
    for i in range(1, len(data)):
        if data["price"][i] > data["price"][i - 1]:  # Example condition
            trades.append({"date": data["date"][i], "action": "BUY", "price": data["price"][i]})
        else:
            trades.append({"date": data["date"][i], "action": "SELL", "price": data["price"][i]})

    return pd.DataFrame(trades)
