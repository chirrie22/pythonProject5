import websocket
import json
import time

class LiveDataFetcher:
    def __init__(self, symbol="R_75"):
        self.symbol = symbol
        self.ws = None
        self.live_data = []

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            if "tick" in data:
                tick_info = {
                    "timestamp": data['tick']['epoch'],
                    "price": data['tick']['quote']
                }
                self.live_data.append(tick_info)
                print(f"Live Data: {tick_info}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def on_error(self, ws, error):
        print(f"WebSocket Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket connection closed. Reconnecting in 5 seconds...")
        time.sleep(5)
        self.start_stream()  # Reconnect

    def on_open(self, ws):
        request = json.dumps({
            "ticks": self.symbol,
            "subscribe": 1
        })
        ws.send(request)

    def start_stream(self):
        """Starts the WebSocket connection and fetches live data."""
        self.ws = websocket.WebSocketApp(
            "wss://ws.binaryws.com/websockets/v3?app_id=67310",
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.on_open = self.on_open
        self.ws.run_forever()

# Usage example (for testing)
if __name__ == "__main__":
    fetcher = LiveDataFetcher("R_75")
    fetcher.start_stream()
