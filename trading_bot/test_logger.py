import unittest
from unittest.mock import patch
import logging
from trading_bot.logger import logging as bot_logger

class TestLogger(unittest.TestCase):
    @patch("trading_bot.logger.logging.info")
    def test_logger_info(self, mock_log_info):
        bot_logger.info("Logging test")
        mock_log_info.assert_called_with("Logging test")

if __name__ == "__main__":
    unittest.main()
