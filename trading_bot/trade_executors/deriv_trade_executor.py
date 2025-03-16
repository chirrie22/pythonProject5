import websocket
import json
import logging
from datetime import datetime, timezone
import threading
import time
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example of the DerivTradeExecutor (You should replace this with your actual executor)
class DerivTradeExecutor:
    def __init__(self, api_url="https://api.deriv.com/v1/market_data"):
        self.api_url = api_url

    @staticmethod
    def execute_trade(trade_type, amount, symbol):
        # Simulate trade execution (Replace with your actual API call)
        logger.info(f"Executing {trade_type} trade of {amount} on {symbol}")
        return {"status": "success", "trade_type": trade_type, "amount": amount, "symbol": symbol}


# WebSocket callback functions
def on_message(message):
    try:
        data = json.loads(message)
        if 'tick' in data:
            # Extract the necessary data from the tick
            timestamp = data['tick']['epoch']
            quote = data['tick']['quote']
            logger.info(f"Received tick data at {datetime.fromtimestamp(timestamp, timezone.utc)}: {quote}")

            # Example: Place a trade based on the received tick data (this is just for demo)
            trade_type = "buy" if random.random() > 0.5 else "sell"
            amount = 10  # Example trade amount
            symbol = "R_75"  # Symbol being traded
            executor = DerivTradeExecutor()  # Initialize trade executor
            result = executor.execute_trade(trade_type, amount, symbol)
            logger.info(f"Trade result: {result}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")

def on_error(error):
    logger.error(f"WebSocket error: {error}")

def on_close():
    logger.info("WebSocket closed")

def on_open(ws):
    # Send a subscription message for the 'R_75' ticks
    subscription_message = json.dumps({
        "ticks": "R_75",
        "subscribe": 1
    })
    ws.send(subscription_message)
    logger.info("Subscribed to R_75 ticks")

# Create and run the WebSocket connection in a separate thread
def run_websocket():
    websocket_url = "wss://ws.binaryws.com/websockets/v3?app_id=67310"
    ws = websocket.WebSocketApp(
        websocket_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    ws.run_forever()

# Thread to run the WebSocket connection
def start_websocket_thread():
    websocket_thread = threading.Thread(target=run_websocket)
    websocket_thread.daemon = True  # Allow thread to be killed when the main program ends
    websocket_thread.start()
    logger.info("WebSocket thread started")

# Function to keep the main program running
def keep_running():
    try:
        while True:
            time.sleep(1)  # Prevent main thread from exiting
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")

if __name__ == "__main__":
    start_websocket_thread()  # Start the WebSocket in a separate thread
    keep_running()  # Keep the main program running
