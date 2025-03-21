import pytest
from telegram_bot import send_telegram_message


def test_send_telegram_message():
    """Tests if the Telegram message sending function works."""
    response = send_telegram_message("Testing Telegram bot!")

    # Print the response for debugging
    print("Test response:", response)

    # Assert the response is successful
    assert response.get("ok", False) == True, f"Telegram API Error: {response}"
