class DerivStrategy:
    def __init__(self, volatility_threshold=2, trend_threshold=0.5, price_threshold=100):
        self.volatility_threshold = volatility_threshold
        self.trend_threshold = trend_threshold
        self.price_threshold = price_threshold
        self.entry_price = None
        self.trade_type = None

    def apply_strategy(self, market_data):
        """Applies strategy based on price, volatility, and trend direction."""
        price = market_data.get("price", 0)
        volatility = market_data.get("volatility", float('inf'))
        trend = market_data.get("trend", 0)

        if price > self.price_threshold and volatility < self.volatility_threshold and trend > self.trend_threshold:
            self.entry_price = price
            self.trade_type = "buy"
            return "buy"
        elif price < self.price_threshold and volatility < self.volatility_threshold and trend < -self.trend_threshold:
            self.entry_price = price
            self.trade_type = "sell"
            return "sell"
        return "hold"

    def check_tp_sl(self, current_price, account_balance):
        """
        Checks if Take Profit (2× account balance) or Stop Loss (0.5× account balance) is hit.
        :param current_price: Current market price.
        :param account_balance: User's current account balance.
        :return: 'close_take_profit', 'close_stop_loss', or None.
        """
        if self.entry_price is None or self.trade_type is None:
            return None  # No active trade

        tp_amount = account_balance * 2
        sl_amount = account_balance * 0.5

        if self.trade_type == "buy":
            tp_price = self.entry_price + tp_amount
            sl_price = self.entry_price - sl_amount
        else:  # "sell"
            tp_price = self.entry_price - tp_amount
            sl_price = self.entry_price + sl_amount

        if (self.trade_type == "buy" and current_price >= tp_price) or (self.trade_type == "sell" and current_price <= tp_price):
            return "close_take_profit"
        elif (self.trade_type == "buy" and current_price <= sl_price) or (self.trade_type == "sell" and current_price >= sl_price):
            return "close_stop_loss"

        return None  # Continue holding trade

    def risk_management(self, capital, risk_percent):
        """Calculates position size based on risk percentage."""
        risk_percent = max(min(risk_percent, 100), 0.1)
        return round((capital * risk_percent) / 100, 2)
