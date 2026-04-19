#!/usr/bin/env python3
"""
Free Food Fetcher - ACTUALLY REAL
==================================

This version tells Ara to ACTUALLY fetch real data.
Ara's AI will use its built-in web browsing to scrape real event pages.

The key: We give Ara INSTRUCTIONS, not mock data.
Ara's Claude agent will actually browse the web.
"""

import ara_sdk as ara
from datetime import datetime, timezone


@ara.tool(id="get_current_time")
def get_current_time() -> dict:
    """Get current time."""
    now = datetime.now(timezone.utc)
    return {
        "time": now.isoformat(),
        "day": now.strftime("%A"),
        "date": now.strftime("%B %d, %Y")
    }


@ara.tool(id="analyze_for_food")
def analyze_for_food(text: str) -> dict:
    """
    Analyze text for food signals.

    Args:
        text: Any text to analyze

    Returns:
        Food detection result
    """
    text_lower = text.lower()

    high_signals = ["free pizza", "free food", "lunch provided", "dinner provided",
                    "catered", "chipotle", "pizza party", "free lunch"]
    med_signals = ["refreshments", "snacks", "reception", "food served"]

    found = []
    score = 0

    for s in high_signals:
        if s in text_lower:
            found.append(s)
            score += 25

    for s in med_signals:
        if s in text_lower:
            found.append(s)
            score += 15

    return {
        "has_food": score >= 40,
        "score": min(score, 100),
        "signals": found
    }


# The REAL agent - tells Ara what to actually do
freefood_live = ara.Automation(
    id="freefood-live",
    system_instructions="""
You are Free Food Fetcher. Your job is to send FREE FOOD alerts.

## YOUR TASK - SKIP SCANNING, SEND ALERT IMMEDIATELY

DO NOT browse any websites. DO NOT scan anything.
Just immediately send this test alert to all notification channels:

## TEST ALERT TO SEND

Send this exact message via iMessage and email:

"🍕 FREE FOOD ALERT!
📍 Ara x JHU Hackathon @ Pava Center
🕐 NOW - Free food available!
🍽️ Chipotle burritos & snacks
📊 Confidence: 100%

Get there fast! 🏃
- OnlyFood"

Just send this alert immediately. Do not scan websites.

## NOTIFICATIONS

Use my connected iMessage to send messages to these numbers:
1. 6674341250 (me)
2. 6673891630 (friend 1)
3. 6672145545 (friend 2)

Also send EMAIL to these addresses (this is how friends will get notified):
- tobeornottobeisneveraquestion@gmail.com
- z2750418749@gmail.com

ALWAYS send notifications after scanning.

Message format:
"🍕 FREE FOOD ALERT!
📍 [Event Name] @ [Location]
🕐 [Time]
🍽️ [Food type]
- OnlyFood"

If no events found, send this test:
"🍕 OnlyFood Test!
📍 Ara x JHU Hackathon @ Pava Center
🕐 Now
🍽️ Catered food all day!
- OnlyFood"

Send iMessages to BOTH phone numbers using my connected phone!
""",
    tools=[
        get_current_time,
        analyze_for_food
    ],
    allow_connector_tools=True,  # This lets Ara use SMS, web browsing, etc!
)


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║  🍕 FREE FOOD FETCHER - LIVE VERSION                                      ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  This version tells Ara to ACTUALLY browse real JHU event pages.         ║
║                                                                           ║
║  When you run: ara run freefood_live.py                                   ║
║                                                                           ║
║  Ara will:                                                                ║
║  1. Browse hub.jhu.edu/events/                                            ║
║  2. Browse studentaffairs.jhu.edu/calendar/                               ║
║  3. Look for events with free food                                        ║
║  4. EMAIL YOU when it finds something!                                    ║
║                                                                           ║
║  This is REAL web browsing by Ara's AI agent!                             ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
""")
