import websocket
import json
import pandas as pd
import os

# Correct Deriv API WebSocket URL
APP_ID = "67310"  # Replace with your own Deriv app ID
DERIV_API_URL = f"wss://ws.derivws.com/websockets/v3?app_id={APP_ID}"

# Set data save path
data_dir = os.path.dirname(__file__)
data_path = os.path.join(data_dir, "deriv_v75_data.csv")


# Function to fetch historical data
def get_historical_data(symbol="R_75", count=100, granularity=60):
    try:
        ws = websocket.create_connection(DERIV_API_URL)
        print("✅ Connected to Deriv WebSocket")

        # Request historical data
        request = {
            "ticks_history": symbol,
            "count": count,
            "end": "latest",
            "granularity": granularity,
            "style": "candles"
        }

        ws.send(json.dumps(request))
        response = json.loads(ws.recv())

        # Close WebSocket properly
        ws.close()
        print("🔒 WebSocket closed successfully.")

        # Validate response
        if "candles" not in response:
            print("❌ No candle data received. Check API response.")
            print("Response:", response)
            return None

        # Convert response to DataFrame
        candles = response["candles"]
        df = pd.DataFrame(candles)

        if df.empty:
            print("❌ No data fetched.")
            return None

        df["epoch"] = pd.to_datetime(df["epoch"], unit="s")

        # Save to CSV
        df.to_csv(data_path, index=False)
        print(f"✅ Data saved successfully at: {data_path}")

        return df

    except websocket.WebSocketException as e:
        print(f"❌ WebSocket Error: {e}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")


# Run data fetch
if __name__ == "__main__":
    get_historical_data()

