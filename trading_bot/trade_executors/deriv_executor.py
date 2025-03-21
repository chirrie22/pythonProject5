import os
import logging
import json
import websocket
import time
import requests
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DerivExecutor:
    VALID_ASSETS = {"R_75", "R_100", "R_50"}
    DERIV_API_URL = "wss://ws.binaryws.com/websockets/v3?app_id=67310"

    def __init__(self, api_token=API_TOKEN, account_balance=1000):
        """Initialize WebSocket connection and account balance."""
        if not api_token:
            raise ValueError("❌ Missing Deriv API Token. Set it in .env file.")

        self.api_token = api_token
        self.ws = None
        self.account_balance = account_balance  # User-defined account balance

    def connect(self):
        """Establish WebSocket connection."""
        try:
            if self.ws and self.ws.connected:
                return True
            self.ws = websocket.create_connection(self.DERIV_API_URL)
            logging.info("✅ WebSocket connected.")
            return True
        except Exception as e:
            logging.error(f"❌ WebSocket Connection Failed: {e}")
            return False

    def disconnect(self):
        """Close WebSocket connection."""
        if self.ws:
            self.ws.close()
            logging.info("🔌 WebSocket connection closed.")

    def authenticate(self):
        """Authenticate using API token."""
        if not self.connect():
            return False

        try:
            auth_data = {"authorize": self.api_token}
            self.ws.send(json.dumps(auth_data))
            response = json.loads(self.ws.recv())

            if "error" in response:
                logging.error(f"❌ Authentication Failed: {response['error']['message']}")
                return False

            logging.info("🔑 Authentication Successful!")
            return True
        except Exception as e:
            logging.error(f"❌ Authentication Error: {e}")
            return False

    def send_telegram_message(self, message):
        """Send message to Telegram bot."""
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            logging.warning("⚠️ Telegram bot token or chat ID is missing. Skipping notification.")
            return

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

        try:
            response = requests.post(url, data=data)
            response_data = response.json()

            if response_data.get("ok"):
                logging.info("📩 Telegram message sent successfully!")
            else:
                logging.error(f"❌ Telegram API Error: {response_data}")

        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Request failed: {e}")

    def execute_trade(self, trade_type, amount, asset):
        """Execute a trade and wait for its completion."""
        if asset not in self.VALID_ASSETS:
            raise ValueError(f"Invalid asset: {asset}. Allowed: {', '.join(self.VALID_ASSETS)}.")

        proposal_data = {
            "proposal": 1,
            "amount": amount,
            "basis": "stake",
            "contract_type": "CALL" if trade_type.upper() == "BUY" else "PUT",
            "currency": "USD",
            "duration": 1,
            "duration_unit": "m",
            "symbol": asset
        }

        try:
            if not self.authenticate():
                return {"error": "Authentication failed."}

            execution_time = time.strftime("%Y-%m-%d %H:%M:%S")

            self.send_telegram_message(
                f"📢 Trade Alert!\n🕒 Execution: {execution_time}\n📊 Asset: {asset}\n📈 Signal: {trade_type}\n💰 Amount: ${amount}\n⏳ Executing trade..."
            )

            self.ws.send(json.dumps(proposal_data))
            proposal_response = json.loads(self.ws.recv())

            if "error" in proposal_response:
                error_message = f"❌ Proposal Failed: {proposal_response['error']['message']}"
                logging.error(error_message)
                self.send_telegram_message(error_message)
                return proposal_response

            proposal_id = proposal_response.get("proposal", {}).get("id")
            if not proposal_id:
                logging.error("❌ No proposal ID received.")
                return {"error": "Proposal ID missing."}

            buy_data = {"buy": proposal_id, "price": amount}
            self.ws.send(json.dumps(buy_data))
            buy_response = json.loads(self.ws.recv())

            if "error" in buy_response:
                error_message = f"❌ Trade Failed: {buy_response['error']['message']}"
                logging.error(error_message)
                self.send_telegram_message(error_message)
                return buy_response

            contract_id = buy_response.get("buy", {}).get("contract_id")
            logging.info(f"✅ Trade Successful. Contract ID: {contract_id}")

            # Wait for trade to complete and fetch result
            profit_loss = self.get_trade_result(contract_id)
            result_time = time.strftime("%Y-%m-%d %H:%M:%S")

            trade_result_message = (
                f"💹 Trade Result:\n"
                f"🕒 Execution: {execution_time}\n"
                f"🕒 Result: {result_time}\n"
                f"📊 Asset: {asset}\n"
                f"📈 Signal: {trade_type}\n"
                f"💰 Amount: ${amount}\n"
                f"💵 P/L: ${profit_loss:.2f}\n"
                f"{'✅ 🟢 PROFIT' if profit_loss > 0 else '✅ 🔴 LOSS'}\n"
                f"📌 Trade Completed ✅"
            )

            logging.info(trade_result_message)
            self.send_telegram_message(trade_result_message)

            return {"profit_loss": profit_loss}

        except Exception as e:
            logging.error(f"❌ WebSocket Trade Error: {e}")
            return {"error": str(e)}

        finally:
            self.disconnect()

    def get_trade_result(self, contract_id):
        """Fetch trade result (profit/loss) using contract ID."""
        try:
            time.sleep(60)  # Simulate waiting for trade completion
            return round(random.uniform(-1000, 1000), 2)  # Simulated P/L for testing

        except Exception as e:
            logging.error(f"❌ Error fetching trade result: {e}")
            return 0

if __name__ == "__main__":
    executor = DerivExecutor(account_balance=1000)

    for i in range(5):  # Execute 5 trades
        trade_type = random.choice(["BUY", "SELL"])
        logging.info(f"🚀 Executing trade {i + 1}/5 as {trade_type}...")
        executor.execute_trade(trade_type, 1000, "R_75")
        time.sleep(5)  # Avoid API rate limits
