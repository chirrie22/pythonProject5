class DerivStrategy:
    pass

import sys
sys.path.append("C:/Users/chiri/PycharmProjects/pythonProject5")  # Adjust this to your project path

from trading_bot.strategies.deriv_strategy import DerivStrategy

def test_strategy_edge_case():
    strategy = DerivStrategy()
    market_data = {"price": 100, "volatility": 0.1}  # Simulate edge market data
    decision = strategy.apply_strategy(market_data)
    assert decision in ["buy", "sell", "hold"]  # Ensure valid decision is returned
