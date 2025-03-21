import sys
import os
import logging
from dotenv import load_dotenv
from trading_bot.trade_executors.deriv_executor import DerivExecutor

# Load environment variables from .env file
load_dotenv()

# Retrieve API token and trading details from environment variables
API_TOKEN = os.getenv("API_TOKEN")
SYMBOL = os.getenv("SYMBOL", "R_75")  # Default to "R_75" if not set
BUY_AMOUNT = float(os.getenv("BUY_AMOUNT", 1))  # Default to 1 if not set

# Ensure the root project directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def initialize_logger():
    """Set up logging for the trading bot."""
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler("trade_log.txt", mode='a')
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


# Initialize the logger
logger = initialize_logger()


def check_api_token():
    """Check if the API token is set."""
    if not API_TOKEN:
        logger.error("❌ API_TOKEN is missing in the .env file. Set it before running the bot.")
        raise ValueError("API_TOKEN is missing")


def execute_trade(executor, trade_type, amount, symbol):
    """Execute a trade and log the response."""
    logger.info(f"🚀 Attempting trade: {trade_type.upper()} {amount} on {symbol}")

    if not hasattr(executor, 'execute_trade'):
        logger.error("❌ ERROR: DerivExecutor has no method execute_trade()")
        return None

    try:
        result = executor.execute_trade(trade_type, amount, symbol)
        if result:
            logger.info(f"✅ Trade executed successfully: {result}")
            return result
        else:
            logger.error("❌ Trade execution failed.")
            return None
    except Exception as e:
        logger.error(f"❌ Exception during trade execution: {e}")
        return None


def start_bot():
    """Start the trading bot."""
    logger.info("⚡ Trading bot started!")

    # Debugging API variables
    logger.info(f"🔍 DEBUG: Loaded API_TOKEN={API_TOKEN[:5]}... (hidden for security)")
    logger.info(f"🔍 DEBUG: Loaded SYMBOL={SYMBOL}")
    logger.info(f"🔍 DEBUG: Loaded BUY_AMOUNT={BUY_AMOUNT}")

    try:
        check_api_token()
    except ValueError as e:
        return str(e)

    # Initialize executor
    executor = DerivExecutor(api_token=API_TOKEN)

    # Define trade details
    trade_type = "buy"  # Change as needed ("buy" or "sell")
    amount = BUY_AMOUNT
    symbol = SYMBOL

    # Execute trade
    result = execute_trade(executor, trade_type, amount, symbol)

    return "Bot started ✅" if result else "Bot stopped due to trade failure ❌"


if __name__ == '__main__':
    result = start_bot()
    logger.info(result)


