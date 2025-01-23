import websocket
import json

APP_ID = "67311"  # Replace with your App ID
API_TOKEN = "rnDUBYw5v4gz4Ge"  # Replace with your valid API token
URL = f"wss://ws.binaryws.com/websockets/v3?app_id={APP_ID}"


def on_message(ws, message):
    """Handles incoming messages from the WebSocket."""
    data = json.loads(message)
    print("Received:", json.dumps(data, indent=4))

    if "error" in data:
        print("Error:", data["error"]["message"])
    elif "authorize" in data:
        print("Authorization successful!")
        # After successful authorization, request the balance
        balance_request = {
            "balance": 1,
            "subscribe": 1  # Subscribe to real-time updates
        }
        ws.send(json.dumps(balance_request))
        print("Balance request sent.")
    elif "balance" in data:
        print(f"Account Balance: {data['balance']['balance']} {data['balance']['currency']}")


def on_error(ws, error):
    """Handles WebSocket errors."""
    print("Error occurred:", error)


def on_close(ws, close_status_code, close_msg):
    """Handles WebSocket closure."""
    print("WebSocket connection closed.")


def on_open(ws):
    """Handles WebSocket connection opening."""
    print("WebSocket connected.")

    # Authorize with your API Token
    auth_request = {
        "authorize": API_TOKEN
    }
    ws.send(json.dumps(auth_request))
    print("Authorization request sent.")


# Create a WebSocket connection
ws = websocket.WebSocketApp(
    URL,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
    on_open=on_open
)

# Run the WebSocket connection
ws.run_forever()