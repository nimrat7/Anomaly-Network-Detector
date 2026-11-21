
import json
import urllib.request
import urllib.parse
import urllib.error

from telegram_config import BOT_TOKEN, CHAT_ID


def send_telegram_alert(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    data = urllib.parse.urlencode(payload).encode()

    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            result = json.loads(response.read().decode())

        if result.get("ok"):
            print("Telegram notification sent successfully!")
            return True

        print("Telegram API rejected the message.")
        return False

    except urllib.error.HTTPError as error:
        print("Telegram HTTP error:", error.code)
        return False

    except Exception as error:
        print("Telegram connection failed:", type(error).__name__)
        return False


if __name__ == "__main__":

    test_message = """
NETWORK ANOMALY DETECTOR

Your Telegram notification system is working!

Status: Connected
System: Kali Linux
Detection Engine: Isolation Forest

Your security monitoring project is progressing successfully.
"""

    send_telegram_alert(test_message)
