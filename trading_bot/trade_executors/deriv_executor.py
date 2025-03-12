import logging

class DerivExecutor:
    VALID_ASSETS = {"EURUSD", "USDJPY", "GBPUSD"}  # Define allowed assets

    def execute_trade(self, trade_type, amount, asset):
        trade_type = trade_type.upper()

        # Validate trade type
        if trade_type not in ["BUY", "SELL"]:
            raise ValueError(f"Invalid trade type: {trade_type}. Must be 'BUY' or 'SELL'.")

        # Validate amount
        if not isinstance(amount, (int, float)):
            raise TypeError("Trade amount must be a number.")
        if amount <= 0:
            raise ValueError("Trade amount must be positive.")

        # ✅ Validate asset
        if asset not in self.VALID_ASSETS:
            raise ValueError(f"Invalid asset: {asset}. Allowed: {', '.join(self.VALID_ASSETS)}.")

        # Simulate execution
        trade_message = f"Trade executed: {trade_type} {amount} on {asset}"
        logging.info(trade_message)

        return trade_message  # Ensure it returns a string, not True
