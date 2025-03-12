"""
Package initialization for trading_bot.

This file re‑exports modules (config, logger, main) so that they are accessible
at the package level (e.g. trading_bot.config). Do not run this file directly.
"""

from . import config
from . import logger
from . import main

__all__ = ['config', 'logger', 'main']
