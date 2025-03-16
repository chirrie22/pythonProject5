# Initialize the trading_bot package
from .config import API_TOKEN, DERIV_API_URL
from .trade_executors.deriv_trade_executor import execute_deriv_trade
