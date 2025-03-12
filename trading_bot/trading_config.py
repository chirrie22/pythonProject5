# trading_bot/trading_config.py
import os

# Get API credentials from the environment, with defaults
TRADING_API_KEY = os.getenv('TRADING_API_KEY', 'default_api_key')
TRADING_SECRET = os.getenv('TRADING_SECRET', 'default_secret')

def get_config():
    """
    Returns a configuration dictionary with trading settings.
    """
    config = {
        'api_key': TRADING_API_KEY,
        'secret': TRADING_SECRET,
        'max_trade': 1000,
        'min_trade': 10
    }
    return config

def validate_config(config):
    """
    Validates the configuration dictionary.
    Raises ValueError if required keys are missing or empty.
    """
    if not config.get('api_key'):
        raise ValueError("API key is missing")
    if not config.get('secret'):
        raise ValueError("Secret is missing")
    return True
