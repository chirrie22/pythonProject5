import unittest
from unittest.mock import patch
import trading_bot.main

class TestMain(unittest.TestCase):
    @patch("trading_bot.main.logger", autospec=True)
    def test_start_bot_execution(self, mock_logger):
        """Test start_bot() execution and logs."""
        result = trading_bot.main.start_bot()
        self.assertEqual(result, "Bot started")

        mock_logger.info.assert_any_call("Trading bot started successfully!")
        mock_logger.info.assert_any_call("Attempting trade: BUY 100 on EURUSD")
        mock_logger.info.assert_any_call("Trade executed: BUY 100 on EURUSD")

    @patch("trading_bot.main.DerivExecutor")
    def test_trade_execution(self, mock_executor):
        """Test that DerivExecutor executes a trade correctly."""
        instance = mock_executor.return_value
        instance.execute_trade.return_value = "Trade executed: BUY 100 on EURUSD"

        trading_bot.main.start_bot()

        mock_executor.assert_called_once()
        instance.execute_trade.assert_called_once_with('buy', 100, 'EURUSD')

if __name__ == "__main__":
    unittest.main()
