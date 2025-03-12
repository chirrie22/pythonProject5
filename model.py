import requests
import pandas as pd
import time
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
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
        response = requests.get(url, params=params)

        # Print raw response for debugging
        print(f"Raw response from Alpha Vantage: {response.text}\n")

        if response.status_code == 200:
            data = response.json()
            if f"Time Series ({interval})" in data:  # Ensure the correct key
                df = pd.DataFrame(data[f"Time Series ({interval})"]).T
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
            else:
                print(f"Error: {data.get('Note', 'No time series data returned')}")
        else:
            print(f"Error: Request failed with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed with exception: {e}")

    return None

# Prepare data for training
def prepare_data(data):
    data['Date'] = data.index
    data['Date'] = data['Date'].map(pd.Timestamp.toordinal)  # Convert dates to numbers
    return data[['Date', 'Close']]

# Train model and predict next closing price
def train_and_predict(data):
    if data is None or len(data) < 2:
        print("Not enough data to train the model. Skipping this round.")
        return

    data = prepare_data(data)

    # Splitting the data
    X = data[['Date']]
    y = data['Close']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Model Evaluation:\nRMSE: {rmse}\nMAE: {mae}\nMSE: {mse}\nR-Squared: {r2}")

    # Predict next day's closing price
    next_day = pd.DataFrame({'Date': [X.iloc[-1, 0] + 1]})  # Predict for the next day
    predicted_price = model.predict(next_day)
    print(f"Predicted Closing Price: {predicted_price}")

# Main function
def main():
    ticker = "AAPL"  # Replace with your symbol of choice
    print("Starting script...")

    # Fetch data from Alpha Vantage
    data = fetch_data_alpha_vantage(ticker, interval="5min")  # You can adjust the interval

    if data is None:
        print("Error: No data fetched. Exiting script.")
        return  # Stop execution if no data

    print("Data successfully retrieved. Training model now...")
    train_and_predict(data)
    print("Script completed.")

# Run the script
if __name__ == "__main__":
    main()