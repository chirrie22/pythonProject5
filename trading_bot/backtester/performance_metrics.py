def calculate_metrics(trades):
    print("Calculating performance metrics...")

    if trades.empty:
        return {"profit": 0, "loss": 0, "win_rate": 0}

    profit = sum(trade["price"] for trade in trades if trade["action"] == "SELL")
    loss = sum(trade["price"] for trade in trades if trade["action"] == "BUY")
    win_rate = round((profit / (profit + loss)) * 100, 2) if (profit + loss) > 0 else 0

    return {"profit": profit, "loss": loss, "win_rate": win_rate}
