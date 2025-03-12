import requests
import pandas as pd
import time

# Define the API key from Alpha Vantage
ALPHA_VANTAGE_API_KEY = "5C6C0D6YFIHXZK2I"  # Replace with your API key

# Function to fetch stock data from Alpha Vantage
def fetch_data_alpha_vantage(symbol, interval="5min", api_key=ALPHA_VANTAGE_API_KEY):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "apikey": api_key
    }

    try:
        # Send the request to the Alpha Vantage API
        response = requests.get(url, params=params)

        # Print the raw response and status code for debugging
        print(f"Response status code: {response.status_code}")
        print(f"Raw response from Alpha Vantage:\n{response.text}\n")

        if response.status_code == 200:
            # Check if the data contains the expected time series
            data = response.json()
            if "Time Series (1min)" in data:
                # Extract time series data and convert it into a pandas DataFrame
                df = pd.DataFrame(data["Time Series (1min)"]).T
                df = df.rename(columns={
                    '1. open': 'Open',
                    '2. high': 'High',
                    '3. low': 'Low',
                    '4. close': 'Close',
                    '5. volume': 'Volume'
                })
                df.index = pd.to_datetime(df.index)
                df = df.sort_index()
                return df
            elif "Note" in data:
                print(f"Error: {data['Note']}")  # This could be an API call limit error message
            else:
                print(f"Error: No time series data returned")
        else:
            print(f"Error: Request failed with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Handle connection issues
        print(f"Request failed with exception: {e}")

    return None

# Main function
def main():
    ticker = "AAPL"  # Replace with your symbol of choice
    print("Starting script...")

    # Fetch data from Alpha Vantage
    data = fetch_data_alpha_vantage(ticker, interval="15min")  # You can adjust the interval

    if data is None:
        print("Error: No data fetched. Exiting script.")
        return  # Stop execution if no data

    print("Data successfully retrieved. Training model now...")
    # Call your model training code here

    print("Script completed.")

# Run the script
if __name__ == "__main__":
    main()