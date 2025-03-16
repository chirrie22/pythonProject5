def simple_moving_average_strategy(row):
    """Basic strategy using moving averages."""
    if row["short_ma"] > row["long_ma"]:
        return "BUY"
    elif row["short_ma"] < row["long_ma"]:
        return "SELL"
    return "HOLD"
