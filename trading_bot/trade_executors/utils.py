import pandas as pd

def load_historical_data(filepath):
    """Load historical market data from a CSV file."""
    df = pd.read_csv(filepath)
    df["short_ma"] = df["price"].rolling(window=5).mean()
    df["long_ma"] = df["price"].rolling(window=20).mean()
    return df
