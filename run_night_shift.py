#!/usr/bin/env python3
"""
Ara Night Shift - 24/7 Productivity Agent
==========================================

This is the main entry point for the Night Shift agent.
It can run as:
1. One-time execution (for testing)
2. Scheduled execution (runs at specified time daily)
3. Continuous daemon (runs in background)

Usage:
    python run_night_shift.py              # Run once (test mode)
    python run_night_shift.py --schedule   # Run daily at BRIEFING_TIME
    python run_night_shift.py --daemon     # Run as background service
"""

import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from agents.night_shift import NightShiftAgent
from integrations.gmail import GmailClient
from integrations.calendar import CalendarClient
from integrations.telegram_bot import TelegramBot


def run_analysis():
    """Run the night shift analysis and deliver briefing."""
    print(f"\n{'='*50}")
    print(f"🌙 ARA NIGHT SHIFT AGENT")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    # Initialize components
    agent = NightShiftAgent()
    gmail = GmailClient()
    calendar = CalendarClient()
    telegram = TelegramBot()

    # Fetch data
    print("📧 Fetching emails...")
    emails = gmail.get_recent_emails(max_results=20, hours_back=24)
    print(f"   Found {len(emails)} emails")

    print("📅 Fetching calendar...")
    events = calendar.get_todays_events()
    print(f"   Found {len(events)} events")

    print("📁 Scanning downloads...")
    downloads_path = os.path.expanduser("~/Downloads")
    try:
        files = os.listdir(downloads_path)[:50]  # Limit to 50 files
        print(f"   Found {len(files)} files")
    except Exception:
        files = []
        print("   Could not access Downloads folder")

    # Run analysis
    user_name = os.getenv("USER_NAME", "there")
    briefing = agent.run_nightly_analysis(
        emails=emails,
        events=events,
        files=files,
        user_name=user_name
    )

    # Display briefing
    print(f"\n{'='*50}")
    print("📋 MORNING BRIEFING")
    print(f"{'='*50}\n")
    print(briefing)
    print(f"\n{'='*50}\n")

    # Deliver via Telegram
    if telegram.token and telegram.chat_id:
        print("📱 Sending via Telegram...")
        success = telegram.send_morning_briefing(briefing)
        if success:
            print("✅ Briefing delivered!")
        else:
            print("❌ Failed to send via Telegram")
    else:
        print("ℹ️  Telegram not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")

    return briefing


def run_scheduled():
    """Run agent on a daily schedule."""
    from apscheduler.schedulers.blocking import BlockingScheduler

    briefing_time = os.getenv("BRIEFING_TIME", "07:00")
    hour, minute = map(int, briefing_time.split(":"))

    scheduler = BlockingScheduler()
    scheduler.add_job(
        run_analysis,
        'cron',
        hour=hour,
        minute=minute,
        id='morning_briefing'
    )

    print(f"🕐 Night Shift Agent scheduled for {briefing_time} daily")
    print("Press Ctrl+C to stop")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n👋 Night Shift Agent stopped")


def run_daemon():
    """Run as a background daemon with periodic checks."""
    import time
    from apscheduler.schedulers.background import BackgroundScheduler

    briefing_time = os.getenv("BRIEFING_TIME", "07:00")
    hour, minute = map(int, briefing_time.split(":"))

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_analysis,
        'cron',
        hour=hour,
        minute=minute,
        id='morning_briefing'
    )
    scheduler.start()

    print(f"🌙 Night Shift Agent running in background")
    print(f"📋 Morning briefing scheduled for {briefing_time}")
    print("Press Ctrl+C to stop")

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("\n👋 Night Shift Agent stopped")


def main():
    parser = argparse.ArgumentParser(
        description="Ara Night Shift - 24/7 Productivity Agent"
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Run on daily schedule (uses BRIEFING_TIME env var)"
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run as background daemon"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run once in test mode (default)"
    )

    args = parser.parse_args()

    if args.schedule:
        run_scheduled()
    elif args.daemon:
        run_daemon()
    else:
        run_analysis()


if __name__ == "__main__":
    main()
