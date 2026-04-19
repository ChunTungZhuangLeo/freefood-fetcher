"""
Telegram Bot Integration for Night Shift Agent
Delivers morning briefings via Telegram.

Setup:
1. Message @BotFather on Telegram
2. Create a new bot with /newbot
3. Copy the API token
4. Add TELEGRAM_BOT_TOKEN to your .env
5. Start a chat with your bot and send /start
6. Get your chat ID by visiting: https://api.telegram.org/bot<TOKEN>/getUpdates
"""

import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class TelegramBot:
    """Telegram bot for delivering messages."""

    def __init__(self, token: str = None, chat_id: str = None):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, text: str, parse_mode: str = "Markdown") -> bool:
        """Send a message to the configured chat."""
        if not self.token or not self.chat_id:
            print("Telegram not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
            return False

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print("✅ Message sent via Telegram")
                return True
            else:
                print(f"Telegram error: {response.text}")
                return False
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")
            return False

    def send_morning_briefing(self, briefing: str) -> bool:
        """Send the morning briefing with nice formatting."""
        # Add header
        formatted = f"☀️ *MORNING BRIEFING*\n{'─' * 20}\n\n{briefing}"
        return self.send_message(formatted)

    def get_updates(self) -> list:
        """Get recent messages (useful for finding chat ID)."""
        url = f"{self.base_url}/getUpdates"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json().get("result", [])
        except Exception as e:
            print(f"Error getting updates: {e}")
        return []

    def get_chat_id(self) -> Optional[str]:
        """Helper to find your chat ID."""
        updates = self.get_updates()
        for update in updates:
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                print(f"Found chat ID: {chat_id}")
                return str(chat_id)
        print("No messages found. Send a message to your bot first.")
        return None


class WhatsAppBusiness:
    """
    WhatsApp Business API integration.
    Note: Requires WhatsApp Business API access and approved templates.
    """

    def __init__(self, phone_number_id: str = None, access_token: str = None):
        self.phone_number_id = phone_number_id or os.getenv("WHATSAPP_PHONE_ID")
        self.access_token = access_token or os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.base_url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}/messages"

    def send_message(self, to: str, text: str) -> bool:
        """Send a WhatsApp message."""
        if not self.phone_number_id or not self.access_token:
            print("WhatsApp not configured")
            return False

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": text}
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"WhatsApp error: {e}")
            return False


if __name__ == "__main__":
    # Test Telegram bot
    bot = TelegramBot()

    # Try to find chat ID if not set
    if not bot.chat_id:
        print("Looking for chat ID...")
        bot.get_chat_id()
    else:
        # Send test message
        test_message = """
☀️ *Test Morning Briefing*

📧 *Inbox Summary*
• 3 urgent emails
• 12 unread total

📅 *Today's Schedule*
• 9:00 AM - Team Standup
• 2:00 PM - Client Call

✅ *Top Priority*
Reply to boss's email about Q2 report

_Sent by Ara Night Shift Agent_
"""
        bot.send_message(test_message)
