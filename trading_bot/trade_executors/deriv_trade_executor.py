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


# Deriv Trade Executor
class DerivTradeExecutor:
    def __init__(self, api_url="https://api.deriv.com/v1/trade"):
        self.api_url = api_url  # Update to the correct trading API

    @staticmethod
    def execute_trade(trade_type, amount, symbol):
        trade_type = trade_type.upper()  # Convert to "BUY" or "SELL"

        # Simulate trade execution (Replace with actual API request if needed)
        logger.info(f"Executing {trade_type} trade of {amount} on {symbol}")
        return {"status": "success", "trade_type": trade_type, "amount": amount, "symbol": symbol}


# WebSocket callback functions
def on_message(ws, message):
    try:
        data = json.loads(message)
        if 'tick' in data:
            # Extract tick data
            timestamp = data['tick']['epoch']
            quote = data['tick']['quote']
            logger.info(f"Received tick data at {datetime.fromtimestamp(timestamp, timezone.utc)}: {quote}")

            # Random trade decision (For demo purposes)
            trade_type = "buy" if random.random() > 0.5 else "sell"
            amount = 10
            symbol = "R_75"

            executor = DerivTradeExecutor()
            result = executor.execute_trade(trade_type, amount, symbol)
            logger.info(f"Trade result: {result}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")


def on_error(ws, error):
    logger.error(f"WebSocket error: {error}")


def on_close(ws, close_status_code, close_msg):
    logger.info(f"WebSocket closed: {close_status_code} - {close_msg}")


def on_open(ws):
    subscription_message = json.dumps({
        "ticks": "R_75",
        "subscribe": 1
    })

    ws.send(subscription_message)
    logger.info("Subscribed to R_75 ticks")


# WebSocket connection function
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


# Start WebSocket in a separate thread
def start_websocket_thread():
    websocket_thread = threading.Thread(target=run_websocket)
    websocket_thread.daemon = True  # Thread stops when main program ends
    websocket_thread.start()
    logger.info("WebSocket thread started")


# Keep the program running
def keep_running():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")


if __name__ == "__main__":
    start_websocket_thread()
    keep_running()
