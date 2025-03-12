import websocket
import json
import logging

# Configure logging (force=True ensures output is always displayed)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    force=True
)
logger = logging.getLogger("trading_bot.deriv_data_fetcher")

# Deriv WebSocket API URL
DERIV_WS_URL = "wss://ws.binaryws.com/websockets/v3?app_id=67310"


def on_message(ws, message):
    """Handles incoming messages from the WebSocket."""
    data = json.loads(message)
    logger.info(f"Fetched Market Data: {json.dumps(data, indent=2)}")
    print("Market Data Received:", data)  # Debugging print


def on_error(ws, error):
    """Handles WebSocket errors."""
    logger.error(f"WebSocket Error: {error}")
    print("Error:", error)  # Debugging print


def on_close(ws, close_status_code, close_msg):
    """Handles WebSocket closing events."""
    logger.info("Connection to Deriv WebSocket API closed.")
    print("WebSocket closed!")  # Debugging print


def on_open(ws):
    """Sends a subscription request when the connection opens."""
    logger.debug("Connecting to Deriv WebSocket API...")
    print("Connected to WebSocket!")  # Debugging print

    # Example: Subscribe to market data for a specific symbol (e.g., Volatility 75 Index)
    request = {
        "ticks": "R_75",  # Change symbol as needed
        "subscribe": 1
    }
    ws.send(json.dumps(request))
    logger.info("Market data subscription request sent.")
    print("Subscription request sent.")  # Debugging print


def fetch_deriv_market_data():
    """Connects to the Deriv WebSocket API and fetches real-time market data."""
    print("Starting WebSocket connection...")  # Debugging print
    ws = websocket.WebSocketApp(
        DERIV_WS_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    fetch_deriv_market_data()
