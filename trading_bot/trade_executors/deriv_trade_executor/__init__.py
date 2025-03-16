
from trading_bot.trade_executors.deriv_executor import DerivExecutor

executor = DerivExecutor()

def execute_deriv_trade(trade_type, amount, symbol):
    """Wrapper function for executing trades via DerivExecutor."""
    return executor.execute_trade(trade_type, amount, symbol)


def place_trade():
    return None