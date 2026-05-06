import os
import requests
from dotenv import load_dotenv


load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_discord_alert(message: str) -> None:
    """
    Sends a simple text alert to the configured Discord webhook.
    """
    if not DISCORD_WEBHOOK_URL:
        raise ValueError("Missing DISCORD_WEBHOOK_URL in .env")

    payload = {
        "content": message
    }

    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json=payload,
        timeout=15
    )

    response.raise_for_status()


if __name__ == "__main__":
    send_discord_alert("Mythea webhook test successful.")
    print("Discord test alert sent.")