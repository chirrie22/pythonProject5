import unittest
from unittest.mock import MagicMock, patch

class TestWebSocket(unittest.TestCase):
    @patch("websocket.WebSocketApp")  # Make sure this path matches how WebSocket is imported
    def test_websocket_mock(self, mock_ws):
        # Mock WebSocket behavior
        mock_ws.return_value.run_forever = MagicMock()
        mock_ws.return_value.send = MagicMock()
        mock_ws.return_value.close = MagicMock()

        # Simulate calling the WebSocket connection
        ws = mock_ws()
        ws.run_forever()

        # Assertions to ensure it was called
        ws.run_forever.assert_called_once()

if __name__ == "__main__":
    unittest.main()
