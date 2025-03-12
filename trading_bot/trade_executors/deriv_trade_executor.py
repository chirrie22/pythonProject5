# trading_bot/trade_executors/deriv_trade_executor.py

from trading_bot.trade_executors.deriv_executor import DerivExecutor

def execute_deriv_trade(trade_type, amount, symbol):
    executor = DerivExecutor()
    return executor.execute_trade(trade_type, amount, symbol)
