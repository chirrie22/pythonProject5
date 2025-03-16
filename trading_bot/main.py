import logging
from trading_bot.trade_executors.deriv_executor import DerivExecutor


def initialize_logger():
    """Set up logging for the trading bot."""
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if this function is called multiple times
    if not logger.handlers:
        file_handler = logging.FileHandler("trade_log.txt")
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


# Initialize the logger at module level
logger = initialize_logger()


def start_bot():
    """Start the trading bot and execute a sample trade."""
    logger.info("Trading bot started successfully!")

    # Create an instance of DerivExecutor
    executor = DerivExecutor()

    # Sample trade execution (modify as needed)
    trade_type = "buy"
    amount = 100
    symbol = "EURUSD"

    logger.info(f"Attempting trade: {trade_type.upper()} {amount} on {symbol}")

    result = executor.execute_trade(trade_type, amount, symbol)
    logger.info(result)  # Log trade result

    return "Bot started"


if __name__ == '__main__':
    start_bot()
