import unittest
import trading_bot

class TestImport(unittest.TestCase):
    def test_module_imports(self):
        self.assertTrue(hasattr(trading_bot, 'config'))
        self.assertTrue(hasattr(trading_bot, 'logger'))
        self.assertTrue(hasattr(trading_bot, 'main'))  # Ensure main is imported

if __name__ == '__main__':
    unittest.main()
