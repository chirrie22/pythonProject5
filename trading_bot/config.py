# trading_bot/config.py

# API configuration
DERIV_API_URL = "wss://ws.binaryws.com/websockets/v3?app_id=67310"  # WebSocket URL
API_TOKEN = "zOHx5Nu50zDoY0z"  # Replace with your real API token
BASE_URL = "https://api.deriv.com"  # Base URL for API requests

# Market and Symbol settings
MARKET_TYPE = "deriv"  # Set your market type here (e.g., deriv, forex, crypto)
SYMBOL = "R_75"  # Market Symbol (can be changed depending on your trading strategy)

# Trading settings
BUY_AMOUNT = 1  # Trade amount (can be adjusted as needed)

# Add any other parameters that you might need in the future
# For example, max number of trades per minute, risk management settings, etc.
MAX_TRADES_PER_MINUTE = 10
STOP_LOSS_PERCENTAGE = 0.05  # Example stop loss percentage

