# trading_bot/test_trading_config_improved.py
import os
import unittest
from trading_bot.trading_config import get_config, validate_config


class TestTradingConfig(unittest.TestCase):
    def test_get_config_defaults(self):
        # Ensure that get_config returns a dictionary with the expected keys and default values
        config = get_config()
        self.assertIn('api_key', config)
        self.assertIn('secret', config)
        self.assertIn('max_trade', config)
        self.assertIn('min_trade', config)

        # Check that the default values are in place when no environment variables are set.
        self.assertEqual(config['api_key'], 'default_api_key')
        self.assertEqual(config['secret'], 'default_secret')
        self.assertEqual(config['max_trade'], 1000)
        self.assertEqual(config['min_trade'], 10)

    def test_validate_config_success(self):
        # Provide a valid configuration and expect validation to pass.
        config = {
            'api_key': 'test_key',
            'secret': 'test_secret',
            'max_trade': 1000,
            'min_trade': 10
        }
        self.assertTrue(validate_config(config))

    def test_validate_config_missing_api_key(self):
        # Test that a missing API key results in a ValueError.
        config = {
            'api_key': '',
            'secret': 'test_secret'
        }
        with self.assertRaises(ValueError) as context:
            validate_config(config)
        self.assertEqual(str(context.exception), "API key is missing")

    def test_validate_config_missing_secret(self):
        # Test that a missing secret results in a ValueError.
        config = {
            'api_key': 'test_key',
            'secret': None
        }
        with self.assertRaises(ValueError) as context:
            validate_config(config)
        self.assertEqual(str(context.exception), "Secret is missing")


if __name__ == '__main__':
    unittest.main()
