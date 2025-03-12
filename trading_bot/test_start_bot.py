import unittest
import logging
import sys
import os
from io import StringIO

# Adjust sys.path so Python can locate the trading_bot package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import trading_bot.main as main


class TestStartBot(unittest.TestCase):
    def test_start_bot_returns_expected(self):
        result = main.start_bot()
        self.assertEqual(result, "Bot started")

    def test_start_bot_logs(self):
        # Capture log output
        stream = StringIO()
        test_handler = logging.StreamHandler(stream)
        test_handler.setFormatter(logging.Formatter('%(message)s'))
        logger = logging.getLogger("trading_bot")
        logger.addHandler(test_handler)

        main.start_bot()

        logger.removeHandler(test_handler)
        log_output = stream.getvalue()

        self.assertIn("Trading bot started successfully!", log_output)
        self.assertIn("Trade executed: BUY 100 on EURUSD", log_output)

    def test_logger_initialization_branch(self):
        # Clear the logger's handlers to simulate a fresh state
        logger = logging.getLogger("trading_bot")
        logger.handlers = []

        # Re-initialize the logger so the branch in initialize_logger() is executed
        new_logger = main.initialize_logger()
        # Check that a handler was added
        self.assertTrue(new_logger.handlers)
        # Optionally, you can check that the formatter is as expected:
        handler = new_logger.handlers[0]
        self.assertEqual(handler.formatter._fmt, '%(asctime)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    unittest.main()
