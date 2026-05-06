import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import requests
from dotenv import load_dotenv


load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


@dataclass
class AttackEvent:
    """Represents a Mythea combat event that should trigger a Discord alert."""

    attacker_name: str
    attacker_province: str
    defender_name: str
    defender_province: str
    attack_type: str = "Unknown"
    land_gained: Optional[int] = None
    notes: Optional[str] = None


def send_discord_alert(message: str) -> None:
    """Sends a simple text alert to the configured Discord webhook."""
    if not DISCORD_WEBHOOK_URL:
        raise ValueError("Missing DISCORD_WEBHOOK_URL in environment variables")

    payload = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=15)
    response.raise_for_status()


def send_attack_notification(event: AttackEvent) -> None:
    """Sends a structured embed message to Discord for a Mythea attack event."""
    if not DISCORD_WEBHOOK_URL:
        raise ValueError("Missing DISCORD_WEBHOOK_URL in environment variables")

    fields = [
        {
            "name": "Attacker",
            "value": f"{event.attacker_name} ({event.attacker_province})",
            "inline": True,
        },
        {
            "name": "Defender",
            "value": f"{event.defender_name} ({event.defender_province})",
            "inline": True,
        },
        {"name": "Attack Type", "value": event.attack_type, "inline": True},
    ]

    if event.land_gained is not None:
        fields.append({"name": "Land Gained", "value": str(event.land_gained), "inline": True})

    if event.notes:
        fields.append({"name": "Notes", "value": event.notes, "inline": False})

    embed = {
        "title": "⚔️ Mythea Attack Alert",
        "description": "Your province was attacked.",
        "color": 15158332,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fields": fields,
    }

    payload = {
        "username": "Mythea Guard",
        "embeds": [embed],
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=15)
    response.raise_for_status()


def build_attack_event_from_env() -> AttackEvent:
    """Builds an AttackEvent from environment variables for simple integrations/tests."""
    return AttackEvent(
        attacker_name=os.getenv("MYTHEA_ATTACKER_NAME", "Unknown Attacker"),
        attacker_province=os.getenv("MYTHEA_ATTACKER_PROVINCE", "Unknown Province"),
        defender_name=os.getenv("MYTHEA_DEFENDER_NAME", "You"),
        defender_province=os.getenv("MYTHEA_DEFENDER_PROVINCE", "Your Province"),
        attack_type=os.getenv("MYTHEA_ATTACK_TYPE", "Unknown"),
        land_gained=(
            int(os.getenv("MYTHEA_LAND_GAINED"))
            if os.getenv("MYTHEA_LAND_GAINED", "").isdigit()
            else None
        ),
        notes=os.getenv("MYTHEA_ATTACK_NOTES"),
    )


if __name__ == "__main__":
    test_event = build_attack_event_from_env()
    send_attack_notification(test_event)
    print("Discord attack alert sent.")
