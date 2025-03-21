import logging
import os

def setup_logger(log_file="trading_bot.log"):
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)  # Capture all levels of logs

    # Prevent adding multiple handlers
    if not logger.handlers:
        # Console Handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        # File Handler
        file_handler = logging.FileHandler(log_file, mode='a')
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Initialize logger
logger = setup_logger()

# Example usage
logger.info("Logger initialized successfully!")
logger.debug("This is a debug message for troubleshooting.")
