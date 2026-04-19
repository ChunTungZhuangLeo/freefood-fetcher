#!/usr/bin/env python3
"""
Free Food Fetcher - REAL Ara Integration
=========================================

This version actually uses Ara's built-in tools to:
1. Fetch real event data from JHU event calendars
2. Use web scraping to find food signals
3. Send real notifications

Deploy:
    ara deploy freefood_real.py --cron "0 * * * *"
"""

import ara_sdk as ara
from datetime import datetime, timezone
from typing import List, Dict
import json


# =============================================================================
# TOOLS - Real data fetching
# =============================================================================

@ara.tool(id="fetch_jhu_events")
def fetch_jhu_events() -> dict:
    """
    Fetch events from JHU's actual event calendar.
    Uses Ara's web fetching capability.

    In production, this would scrape:
    - https://hub.jhu.edu/events/
    - https://studentaffairs.jhu.edu/events/
    - Various department calendars

    Returns:
        List of events from JHU sources
    """
    # This tells Ara to fetch real data
    return {
        "action": "fetch_web",
        "sources": [
            "https://hub.jhu.edu/events/",
            "https://studentaffairs.jhu.edu/events/",
            "https://cs.jhu.edu/events/"
        ],
        "instruction": "Find all events happening today and tomorrow. For each event, extract: title, location, time, and any mention of food, refreshments, lunch, pizza, catering, or snacks."
    }


@ara.tool(id="fetch_instagram_events")
def fetch_instagram_events(accounts: List[str]) -> dict:
    """
    Check Instagram accounts for event announcements.

    Args:
        accounts: List of Instagram handles to check

    Returns:
        Recent posts mentioning events or food
    """
    return {
        "action": "fetch_social",
        "platform": "instagram",
        "accounts": accounts,
        "instruction": "Find recent posts mentioning events, free food, pizza, study breaks, or club meetings. Extract event details."
    }


@ara.tool(id="check_outlook_calendar")
def check_outlook_calendar() -> dict:
    """
    Check user's Outlook calendar for events with food.
    Requires Ara calendar connector to be enabled.

    Returns:
        Calendar events that might have food
    """
    return {
        "action": "check_calendar",
        "provider": "outlook",
        "filters": ["meeting", "seminar", "workshop", "reception"],
        "instruction": "Find events in my calendar that mention food, lunch, refreshments, or catering in the description or location."
    }


@ara.tool(id="check_email_invites")
def check_email_invites() -> dict:
    """
    Scan email for event invitations mentioning food.
    Requires Ara email connector.

    Returns:
        Email invites that mention food
    """
    return {
        "action": "scan_email",
        "folders": ["inbox", "events"],
        "keywords": ["free food", "pizza", "lunch provided", "catered", "refreshments"],
        "instruction": "Find recent event invitations or announcements that mention free food."
    }


@ara.tool(id="analyze_food_signals")
def analyze_food_signals(text: str) -> dict:
    """
    AI analysis of text to detect food signals.

    Args:
        text: Event description or email content

    Returns:
        Food detection with confidence score
    """
    # Food-related keywords
    high_confidence = ["free pizza", "free food", "lunch provided", "dinner provided",
                       "catered", "chipotle", "pizza party"]
    medium_confidence = ["refreshments", "snacks", "reception", "light bites",
                        "food will be served", "complimentary"]
    low_confidence = ["networking", "social hour", "happy hour"]

    text_lower = text.lower()

    score = 0
    signals = []

    for keyword in high_confidence:
        if keyword in text_lower:
            score += 30
            signals.append(keyword)

    for keyword in medium_confidence:
        if keyword in text_lower:
            score += 15
            signals.append(keyword)

    for keyword in low_confidence:
        if keyword in text_lower:
            score += 5
            signals.append(keyword)

    score = min(score, 100)

    return {
        "has_food": score >= 50,
        "confidence": score,
        "signals": signals,
        "recommendation": "GO!" if score >= 70 else "Maybe" if score >= 40 else "Skip"
    }


@ara.tool(id="send_telegram_alert")
def send_telegram_alert(event_name: str, location: str, time: str, food_type: str, score: int) -> dict:
    """
    Send alert via Telegram using Ara's messaging.

    Args:
        event_name: Name of the event
        location: Where it is
        time: When it starts
        food_type: What food is available
        score: Confidence score

    Returns:
        Confirmation of sent message
    """
    emoji = "🍕🔥" if score >= 80 else "🍕" if score >= 60 else "🍴"

    message = f"""
{emoji} FREE FOOD ALERT {emoji}

📍 {event_name}
📍 {location}
🕐 {time}

🍽️ {food_type}
📊 Confidence: {score}%

Don't miss out! 🏃
    """

    return {
        "action": "send_message",
        "channel": "telegram",
        "message": message.strip()
    }


@ara.tool(id="add_to_calendar")
def add_to_calendar(event_name: str, location: str, time: str, notes: str) -> dict:
    """
    Add food event to user's calendar with reminder.

    Args:
        event_name: Name of event
        location: Where it is
        time: When it starts
        notes: Food details

    Returns:
        Confirmation of calendar entry
    """
    return {
        "action": "create_calendar_event",
        "title": f"🍕 {event_name}",
        "location": location,
        "time": time,
        "reminder": "30 minutes before",
        "notes": f"FREE FOOD: {notes}"
    }


# =============================================================================
# AUTOMATION
# =============================================================================

freefood_real = ara.Automation(
    id="freefood-real",
    system_instructions="""
You are Free Food Fetcher, running on Ara's cloud 24/7.

## Your Data Sources

You have access to REAL data through these tools:
1. **fetch_jhu_events** - Scrape JHU event calendars
2. **fetch_instagram_events** - Check @jhuhopkins, @hopkinsstudents, etc.
3. **check_outlook_calendar** - User's calendar events
4. **check_email_invites** - Event invitations in email

## Your Workflow

Every hour:
1. Fetch events from all sources
2. Analyze each for food signals using analyze_food_signals
3. For high confidence (70%+): Send immediate Telegram alert
4. For medium confidence (40-69%): Add to daily digest
5. Ask if user wants to add to calendar

## Alert Priority

- Score 80+: 🍕🔥 Send IMMEDIATELY
- Score 60-79: 🍕 Include in hourly check
- Score 40-59: 🍴 Daily digest only
- Score <40: Skip

## Personality

Be enthusiastic about free food! Students love saving money.
Use emojis. Be fun but informative.
""",
    tools=[
        fetch_jhu_events,
        fetch_instagram_events,
        check_outlook_calendar,
        check_email_invites,
        analyze_food_signals,
        send_telegram_alert,
        add_to_calendar
    ],
    allow_connector_tools=True,  # Enable Ara's built-in web/email/calendar tools
)


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║     🍕 FREE FOOD FETCHER - REAL INTEGRATION 🍕                           ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   Data Sources:                                                           ║
║   ─────────────                                                           ║
║   📅 JHU Event Calendars (hub.jhu.edu, studentaffairs)                   ║
║   📸 Instagram (@jhuhopkins, @hopkinsstudents)                           ║
║   📧 Your Outlook/Gmail (event invitations)                              ║
║   📆 Your Calendar (meetings with food)                                  ║
║                                                                           ║
║   Ara Capabilities Used:                                                  ║
║   ──────────────────────                                                  ║
║   • Web fetching (scrape event pages)                                     ║
║   • Email connector (scan invites)                                        ║
║   • Calendar connector (check events)                                     ║
║   • Telegram messaging (send alerts)                                      ║
║   • 24/7 cloud execution (hourly checks)                                  ║
║                                                                           ║
║   Deploy:                                                                 ║
║   ───────                                                                 ║
║   ara deploy freefood_real.py --cron "0 * * * *"                         ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
""")
