import websocket
import json
import logging
from datetime import datetime

# Configuration
APP_ID = "67311"  # Replace with your App ID
API_TOKEN = "rnDUBYw5v4gz4Ge"  # Replace with your API token
URL = f"wss://ws.binaryws.com/websockets/v3?app_id={APP_ID}"
MARKET_SYMBOL = "R_75"  # Volatility 75 Index
TRADE_THRESHOLD = 2000  # Example price threshold to trigger a trade
TRADE_AMOUNT = 10  # Amount to stake
TRADE_DURATION = 5  # Duration of trade in ticks
TRADE_CURRENCY = "USD"  # Currency for trade

# Logging Configuration
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Global Variables
authorized = False


def log_event(message):
    """Logs events to the console and log file."""
    print(message)
    logging.info(message)


def save_to_file(filename, data):
    """Saves data to a file."""
    with open(filename, "a") as file:
        file.write(data + "\n")


def place_trade(ws, symbol, amount, contract_type, duration, duration_unit, currency):
    """Sends a trade request."""
    trade_request = {
        "buy": 1,
        "parameters": {
            "amount": amount,
            "basis": "stake",
            "contract_type": contract_type,
            "currency": currency,
            "duration": duration,
            "duration_unit": duration_unit,
            "symbol": symbol,
        },
    }
    ws.send(json.dumps(trade_request))
    log_event("Trade request sent: " + json.dumps(trade_request))


def on_message(ws, message):
    """Handles incoming messages."""
    global authorized
    data = json.loads(message)
    log_event("Received: " + json.dumps(data, indent=4))

    if "error" in data:
        log_event(f"Error: {data['error']['message']}")
    elif "authorize" in data:
        authorized = True
        log_event("Authorization successful!")

        # Request account balance
        balance_request = {"balance": 1, "subscribe": 1}
        ws.send(json.dumps(balance_request))
        log_event("Balance request sent.")

        # Subscribe to market ticks
        tick_request = {"ticks": MARKET_SYMBOL, "subscribe": 1}
        ws.send(json.dumps(tick_request))
        log_event(f"Tick subscription request sent for {MARKET_SYMBOL}.")
    elif "balance" in data:
        balance = data["balance"]["balance"]
        currency = data["balance"]["currency"]
        log_event(f"Account Balance: {balance} {currency}")
        save_to_file("balance_log.txt", f"{datetime.now()} - Balance: {balance} {currency}")
    elif "tick" in data:
        tick_data = data["tick"]
        latest_tick = tick_data["quote"]
        log_event(f"Latest Tick for {MARKET_SYMBOL}: {latest_tick}")

        # Example condition: place a trade if the price exceeds a threshold
        if latest_tick > TRADE_THRESHOLD:
            log_event(f"Price threshold reached: {latest_tick}. Placing trade.")
            place_trade(ws, MARKET_SYMBOL, TRADE_AMOUNT, "CALL", TRADE_DURATION, "t", TRADE_CURRENCY)


def on_error(ws, error):
    """Handles WebSocket errors."""
    log_event(f"WebSocket Error: {error}")


def on_close(ws, close_status_code, close_msg):
    """Handles WebSocket closure."""
    log_event("WebSocket connection closed.")


def on_open(ws):
    """Handles WebSocket connection opening."""
    log_event("WebSocket connected.")

    # Authorize the connection
    auth_request = {"authorize": API_TOKEN}
    ws.send(json.dumps(auth_request))
    log_event("Authorization request sent.")


# Create a WebSocket connection
ws = websocket.WebSocketApp(
    URL,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
    on_open=on_open,
)

# Run the WebSocket connection
try:
    ws.run_forever()
except KeyboardInterrupt:
    log_event("Bot stopped manually.")
