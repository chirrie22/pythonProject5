import numpy as np


def add_features(tick_data, historical_prices=None):
    """
    Add extra trading features to the tick data.

    :param tick_data: Dictionary containing real-time tick data.
    :param historical_prices: List of past price values.
    :return: Updated tick_data with additional features.
    """
    if historical_prices is None:
        historical_prices = []

    # Ensure historical data exists
    if len(historical_prices) > 0:
        tick_data["SMA"] = np.mean(historical_prices[-5:])  # Simple Moving Average (Last 5)
        tick_data["Volatility"] = np.std(historical_prices[-5:])  # Price volatility

    return tick_data
