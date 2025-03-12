class DerivStrategy:
    def __init__(self, volatility_threshold=2, trend_threshold=0.5):
        self.volatility_threshold = volatility_threshold
        self.trend_threshold = trend_threshold

    def apply_strategy(self, market_data):
        """Applies strategy based on price, volatility, and trend direction."""
        price = market_data.get("price", 0)
        volatility = market_data.get("volatility", 0)
        trend = market_data.get("trend", 0)

        if price > 100 and volatility < self.volatility_threshold and trend > self.trend_threshold:
            return "buy"
        elif price < 100 and volatility < self.volatility_threshold and trend < -self.trend_threshold:
            return "sell"
        return "hold"

    def calculate_signal(self, market_data):
        """Alternative signal calculation based on price and trend."""
        price = market_data['price']
        trend = market_data.get('trend', 0)

        if price > 100:
            return "BUY"
        elif price < 100 and trend < 0:  # Adjusted condition
            return "SELL"
        return "HOLD"

    def risk_management(self, capital, risk_percent):
        """Calculates position size based on risk percentage."""
        return (capital * risk_percent) / 100
