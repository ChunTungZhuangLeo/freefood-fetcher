"""
Ara Night Shift Agent
A 24/7 productivity agent that works while you sleep.

This agent:
1. Scans your inbox and prioritizes emails
2. Checks your calendar for conflicts
3. Organizes your Downloads folder
4. Generates a morning briefing
5. Delivers via WhatsApp/Telegram
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class NightShiftAgent:
    """24/7 Agent that prepares your morning while you sleep."""

    def __init__(self):
        self.system_prompt = """You are a personal productivity agent that runs 24/7.
        Your job is to analyze emails, calendars, and tasks to prepare a morning briefing.
        Be concise, actionable, and prioritize ruthlessly.
        Format output for easy scanning on mobile (WhatsApp/Telegram)."""

    def analyze_emails(self, emails: List[Dict]) -> Dict:
        """Analyze and prioritize emails."""
        if not emails:
            return {"summary": "No new emails", "urgent": [], "drafts": []}

        email_text = "\n\n".join([
            f"From: {e.get('from', 'Unknown')}\n"
            f"Subject: {e.get('subject', 'No subject')}\n"
            f"Preview: {e.get('snippet', '')[:200]}"
            for e in emails[:20]  # Limit to 20 most recent
        ])

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=self.system_prompt,
            messages=[{
                "role": "user",
                "content": f"""Analyze these emails and provide:
1. URGENT (needs response today): List with one-line summaries
2. IMPORTANT (respond this week): List with one-line summaries
3. FYI (no action needed): Brief count
4. DRAFT RESPONSES: For urgent emails, draft 1-2 sentence replies

Emails:
{email_text}

Format as JSON with keys: urgent, important, fyi_count, drafts"""
            }]
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"raw_analysis": response.content[0].text}

    def check_calendar(self, events: List[Dict]) -> Dict:
        """Check calendar for conflicts and prep."""
        if not events:
            return {"summary": "No events scheduled", "conflicts": [], "prep_needed": []}

        events_text = "\n".join([
            f"- {e.get('title', 'Untitled')} at {e.get('time', 'TBD')} ({e.get('duration', '?')})"
            for e in events
        ])

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=self.system_prompt,
            messages=[{
                "role": "user",
                "content": f"""Analyze today's calendar:
{events_text}

Identify:
1. CONFLICTS: Overlapping meetings
2. PREP NEEDED: Meetings that need preparation
3. TRAVEL TIME: Any gaps too short between locations
4. FOCUS TIME: Available blocks for deep work

Format as JSON with keys: conflicts, prep_needed, travel_issues, focus_blocks"""
            }]
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"raw_analysis": response.content[0].text}

    def organize_downloads(self, files: List[str]) -> Dict:
        """Suggest organization for Downloads folder."""
        if not files:
            return {"summary": "Downloads folder is empty", "actions": []}

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=self.system_prompt,
            messages=[{
                "role": "user",
                "content": f"""These files are in the Downloads folder:
{chr(10).join(files[:50])}

Suggest organization:
1. DELETE: Old/duplicate files
2. ARCHIVE: Files older than 30 days
3. SORT: Group by type/project

Format as JSON with keys: delete, archive, sort_by_category"""
            }]
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"raw_analysis": response.content[0].text}

    def generate_briefing(
        self,
        email_analysis: Dict,
        calendar_analysis: Dict,
        file_analysis: Dict,
        user_name: str = "there"
    ) -> str:
        """Generate the morning briefing message."""

        context = f"""
EMAIL ANALYSIS:
{json.dumps(email_analysis, indent=2)}

CALENDAR ANALYSIS:
{json.dumps(calendar_analysis, indent=2)}

FILE ANALYSIS:
{json.dumps(file_analysis, indent=2)}
"""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system="""You are generating a morning briefing for WhatsApp/Telegram.
            Use emojis sparingly but effectively.
            Be concise - this will be read on a phone.
            Prioritize actionable items at the top.
            Use line breaks for readability.""",
            messages=[{
                "role": "user",
                "content": f"""Generate a morning briefing for {user_name}.

Today is {datetime.now().strftime('%A, %B %d, %Y')}.

{context}

Structure:
1. One-line greeting with weather/date
2. TOP PRIORITY (1-3 items max)
3. TODAY'S SCHEDULE (quick overview)
4. INBOX SUMMARY (counts + urgent items)
5. SUGGESTED ACTIONS (what to do first)

Keep it under 500 words. Mobile-friendly format."""
            }]
        )

        return response.content[0].text

    def run_nightly_analysis(
        self,
        emails: List[Dict] = None,
        events: List[Dict] = None,
        files: List[str] = None,
        user_name: str = "there"
    ) -> str:
        """Run the full nightly analysis and generate briefing."""

        print("🌙 Night Shift Agent starting...")

        # Analyze emails
        print("📧 Analyzing emails...")
        email_analysis = self.analyze_emails(emails or [])

        # Check calendar
        print("📅 Checking calendar...")
        calendar_analysis = self.check_calendar(events or [])

        # Organize downloads
        print("📁 Organizing files...")
        file_analysis = self.organize_downloads(files or [])

        # Generate briefing
        print("📝 Generating morning briefing...")
        briefing = self.generate_briefing(
            email_analysis,
            calendar_analysis,
            file_analysis,
            user_name
        )

        print("✅ Night Shift complete!")
        return briefing


# Telegram Bot Integration (optional)
class TelegramDelivery:
    """Deliver briefing via Telegram."""

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    def send_message(self, text: str) -> bool:
        """Send message via Telegram."""
        import requests

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Telegram error: {e}")
            return False


# Example usage and testing
if __name__ == "__main__":
    # Sample data for testing
    sample_emails = [
        {
            "from": "boss@company.com",
            "subject": "URGENT: Q2 Report Due Tomorrow",
            "snippet": "Please ensure the Q2 report is finalized by end of day tomorrow. The board meeting is on Friday."
        },
        {
            "from": "team@startup.io",
            "subject": "Hackathon Reminder - Sunday 12pm",
            "snippet": "Don't forget the Ara x JHU hackathon starts at noon. Food will be provided."
        },
        {
            "from": "newsletter@techcrunch.com",
            "subject": "TechCrunch Daily",
            "snippet": "Today's top stories: AI agents reshape productivity..."
        }
    ]

    sample_events = [
        {"title": "Team Standup", "time": "9:00 AM", "duration": "30 min"},
        {"title": "Client Call", "time": "10:00 AM", "duration": "1 hour"},
        {"title": "Lunch with Alex", "time": "12:30 PM", "duration": "1 hour"},
        {"title": "Focus Time", "time": "2:00 PM", "duration": "2 hours"},
    ]

    sample_files = [
        "report_v1_final_FINAL.pdf",
        "screenshot_2024_01_15.png",
        "meeting_notes.docx",
        "random_download.zip",
        "invoice_march.pdf"
    ]

    # Run the agent
    agent = NightShiftAgent()
    briefing = agent.run_nightly_analysis(
        emails=sample_emails,
        events=sample_events,
        files=sample_files,
        user_name="Chuntung"
    )

    print("\n" + "="*50)
    print("MORNING BRIEFING")
    print("="*50)
    print(briefing)
