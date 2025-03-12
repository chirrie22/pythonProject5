import unittest
import logging
from trading_bot.trade_executors.deriv_executor import DerivExecutor

class TestDerivTradeExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = DerivExecutor()

    def test_valid_trade(self):
        """Test valid trade execution."""
        result = self.executor.execute_trade("BUY", 100, "EURUSD")
        self.assertEqual(result, "Trade executed: BUY 100 on EURUSD")

    def test_invalid_trade_type(self):
        """Test handling of invalid trade types."""
        with self.assertRaises(ValueError) as context:
            self.executor.execute_trade("HOLD", 100, "EURUSD")  # Invalid type

        self.assertIn("Invalid trade type: HOLD", str(context.exception))

    def test_invalid_amount_type(self):
        """Test handling of non-numeric trade amounts."""
        with self.assertRaises(TypeError) as context:
            self.executor.execute_trade("BUY", "one hundred", "EURUSD")  # Not a number

        self.assertIn("Trade amount must be a number.", str(context.exception))

    def test_negative_amount(self):
        """Test handling of negative trade amounts."""
        with self.assertRaises(ValueError) as context:
            self.executor.execute_trade("SELL", -50, "EURUSD")  # Negative amount

        self.assertIn("Trade amount must be positive.", str(context.exception))

    def test_invalid_asset(self):
        """Test handling of invalid trading assets."""
        with self.assertRaises(ValueError) as context:
            self.executor.execute_trade("BUY", 100, "BTCUSD")  # Not in allowed assets

        exception_message = str(context.exception)
        self.assertIn("Invalid asset: BTCUSD", exception_message)
        self.assertIn("Allowed:", exception_message)
        self.assertIn("EURUSD", exception_message)
        self.assertIn("USDJPY", exception_message)
        self.assertIn("GBPUSD", exception_message)

    def test_trade_logging(self):
        """Test if trade execution is logged correctly."""
        with self.assertLogs(level=logging.INFO) as log_capture:
            self.executor.execute_trade("SELL", 200, "GBPUSD")

        log_message = log_capture.output[0]  # Get first logged message
        self.assertIn("Trade executed: SELL 200 on GBPUSD", log_message)


if __name__ == "__main__":
    unittest.main()
