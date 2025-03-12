import unittest
from trading_bot.trade_executors.deriv_executor import DerivExecutor

class TestExecuteDerivTrade(unittest.TestCase):
    def setUp(self):
        self.executor = DerivExecutor()

    def test_valid_trade(self):
        """Test a valid trade execution"""
        result = self.executor.execute_trade("BUY", 100, "EURUSD")
        self.assertEqual(result, "Trade executed: BUY 100 on EURUSD")

    def test_invalid_trade_type(self):
        """Expect ValueError for invalid trade type"""
        with self.assertRaises(ValueError) as context:
            self.executor.execute_trade("INVALID", 100, "EURUSD")

        self.assertIn("Invalid trade type:", str(context.exception))
        self.assertIn("Must be 'BUY' or 'SELL'", str(context.exception))

    def test_invalid_asset(self):
        """Expect ValueError for invalid asset"""
        with self.assertRaises(ValueError) as context:
            self.executor.execute_trade("BUY", 100, "INVALID_ASSET")

        self.assertIn("Invalid asset: INVALID_ASSET", str(context.exception))
        self.assertIn("Allowed:", str(context.exception))
        self.assertIn("USDJPY", str(context.exception))
        self.assertIn("EURUSD", str(context.exception))
        self.assertIn("GBPUSD", str(context.exception))

    def test_non_numeric_amount(self):
        """Expect TypeError for non-numeric trade amount"""
        with self.assertRaises(TypeError) as context:
            self.executor.execute_trade("BUY", "one hundred", "EURUSD")

        self.assertIn("Trade amount must be a number", str(context.exception))

    def test_negative_amount(self):
        """Expect ValueError for negative trade amount"""
        with self.assertRaises(ValueError) as context:
            self.executor.execute_trade("BUY", -100, "EURUSD")

        self.assertIn("Trade amount must be positive", str(context.exception))

if __name__ == "__main__":
    unittest.main()
