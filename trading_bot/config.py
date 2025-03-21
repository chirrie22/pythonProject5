# trading_bot/config.py

# 🔗 API Configuration
DERIV_API_URL = "wss://ws.binaryws.com/websockets/v3?app_id=67310"  # WebSocket URL
API_TOKEN = "your_api_token_here"  # 🔑 Replace with your real API token
BASE_URL = "https://api.deriv.com"  # REST API Base URL

# 📈 Market and Symbol Settings
MARKET_TYPE = "deriv"  # Market type (options: deriv, forex, crypto)
SYMBOL = "R_75"  # Market symbol (modify as needed)

# 💰 Trading Settings
BUY_AMOUNT = 1  # Amount per trade (adjust as required)
SELL_AMOUNT = 1  # Amount per sell trade (optional)
MAX_TRADES_PER_MINUTE = 10  # Maximum trades allowed per minute

# 📉 Risk Management Settings
STOP_LOSS_PERCENTAGE = 0.05  # Stop loss percentage (5%)
TAKE_PROFIT_PERCENTAGE = 0.10  # Take profit percentage (10%)
RISK_PER_TRADE = 0.02  # Risk per trade (2% of capital)

# ⏰ Time Settings
TRADE_TIMEOUT = 60  # Timeout for a trade (in seconds)

# 🛠️ Additional Configurations
LOGGING_LEVEL = "INFO"  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
