import asyncio
import json
import websockets
from trading_bot.config import API_TOKEN, DERIV_API_URL
from trading_bot.trade_executors.deriv_trade_executor import place_trade


async def connect_to_deriv():
    """ Connects to Deriv WebSocket API and listens for price updates. """
    while True:  # Reconnect loop
        try:
            async with websockets.connect(DERIV_API_URL) as ws:
                # Authenticate using API token
                auth_request = {"authorize": API_TOKEN}
                await ws.send(json.dumps(auth_request))

                # Wait for authentication response
                auth_response = await ws.recv()
                auth_data = json.loads(auth_response)

                if "error" in auth_data:
                    print(f"Authorization failed: {auth_data['error']['message']}")
                    return

                print("✅ Successfully authenticated with Deriv API")

                # Subscribe to market price updates
                subscription_request = {
                    "ticks": "R_75",  # Example: Change this to the asset you want
                    "subscribe": 1
                }
                await ws.send(json.dumps(subscription_request))

                # Listen for market updates
                while True:
                    try:
                        response = await ws.recv()
                        data = json.loads(response)

                        if "error" in data:
                            print(f"Error: {data['error']['message']}")
                            break

                        # Extract price
                        if "tick" in data:
                            tick = data["tick"]
                            price = tick["quote"]
                            print(f"📈 Market Update: {tick['symbol']} - Price: {price}")

                            # Example trading logic (Modify based on your strategy)
                            if price > 500000:  # Example condition
                                print("🔵 Buy Signal Detected!")
                                await place_trade(ws, price)  # Corrected
                            elif price < 400000:  # Example condition
                                print("🔴 Sell Signal Detected!")
                                await place_trade(ws, price)  # Corrected

                    except websockets.exceptions.ConnectionClosed as e:
                        print(f"Connection closed: {e}")
                        break

        except Exception as e:
            print(f"An error occurred: {e}")
            # Reconnect after a delay in case of failure
            print("Reconnecting in 5 seconds...")
            await asyncio.sleep(5)


# Run the WebSocket connection
if __name__ == "__main__":
    asyncio.run(connect_to_deriv())
