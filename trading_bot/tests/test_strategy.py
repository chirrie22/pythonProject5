import unittest
from trading_bot.strategies.deriv_strategy import DerivStrategy

class TestDerivStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = DerivStrategy()

    def test_apply_strategy_buy(self):
        market_data = {"price": 105, "volatility": 1.5, "trend": 0.8}
        self.assertEqual(self.strategy.apply_strategy(market_data), "buy")

    def test_apply_strategy_sell(self):
        market_data = {"price": 95, "volatility": 1.5, "trend": -0.8}
        self.assertEqual(self.strategy.apply_strategy(market_data), "sell")

    def test_apply_strategy_hold(self):
        market_data = {"price": 100, "volatility": 3.0, "trend": 0.5}
        self.assertEqual(self.strategy.apply_strategy(market_data), "hold")

if __name__ == "__main__":
    unittest.main()
