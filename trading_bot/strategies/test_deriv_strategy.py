import unittest
from trading_bot.strategies.deriv_strategy import DerivStrategy


class TestDerivStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = DerivStrategy()

    def test_calculate_signal(self):
        buy_signal = self.strategy.calculate_signal({"price": 110, "volatility": 1.5, "trend": 0.8})
        sell_signal = self.strategy.calculate_signal({"price": 90, "volatility": 1.5, "trend": -0.8})
        hold_signal = self.strategy.calculate_signal({"price": 100, "volatility": 3, "trend": 0})

        self.assertEqual(buy_signal, "BUY")
        self.assertEqual(sell_signal, "SELL")
        self.assertEqual(hold_signal, "HOLD")

    def test_risk_management(self):
        trade_size = self.strategy.risk_management(1000, 5)  # 5% risk on $1000
        self.assertEqual(trade_size, 50)


if __name__ == "__main__":
    unittest.main()
