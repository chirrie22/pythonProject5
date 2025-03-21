import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    """Send a message to the Telegram bot with error handling."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}

    try:
        response = requests.post(url, data=data)
        response_data = response.json()

        if response_data.get("ok"):
            print("📩 Telegram message sent successfully!")
        else:
            print(f"❌ Telegram API Error: {response_data}")

        return response_data
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return {"ok": False, "error": str(e)}

def execute_trade(signal, asset="Volatility 75", amount=10):
    """Simulate trade execution and send alerts to Telegram."""
    if signal in ["BUY", "SELL"]:
        print(f"Placing {signal} order for {asset}...")

        # Send initial trade signal
        message = f"📢 Trade Alert!\n📊 Asset: {asset}\n📈 Signal: {signal}\n💰 Amount: ${amount}\n⏳ Order Executing..."
        send_telegram_message(message)

        # Simulate trade processing time
        time.sleep(2)

        # Simulated trade outcome (random profit/loss)
        profit = round(amount * 0.95, 2)  # Example: 95% profit rate
        outcome_message = f"💹 Trade Result:\n📊 Asset: {asset}\n📈 Signal: {signal}\n💰 Amount: ${amount}\n💵 Profit: ${profit}\n✅ Trade Completed!"
        send_telegram_message(outcome_message)

    else:
        print("No trade executed.")
        send_telegram_message("⚠️ No trade executed. Market conditions not met.")

# Example: Running automated trades
if __name__ == "__main__":
    trades = [("BUY", "Volatility 75"), ("SELL", "Volatility 100"), ("BUY", "EUR/USD")]

    for signal, asset in trades:
        execute_trade(signal, asset, amount=1000)
        time.sleep(10)  # Wait before next trade (adjust timing as needed)
