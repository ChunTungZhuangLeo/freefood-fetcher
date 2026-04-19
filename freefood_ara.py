#!/usr/bin/env python3
"""
Free Food Fetcher - Never Miss Free Food Again
===============================================

An AI agent that monitors events and alerts you when there's free food.
Runs 24/7 on Ara's cloud infrastructure.

Deploy:
    ara deploy freefood_ara.py --cron "0 * * * *"  # Every hour

Run now:
    ara run freefood_ara.py
"""

import ara_sdk as ara
from datetime import datetime, timezone
from typing import List, Dict, Optional
import json


# =============================================================================
# TOOLS - Functions the AI can call
# =============================================================================

@ara.tool(id="get_current_time")
def get_current_time() -> dict:
    """Get the current time and day of week."""
    now = datetime.now(timezone.utc)
    return {
        "utc_time": now.isoformat(),
        "day_of_week": now.strftime("%A"),
        "hour": now.hour,
        "is_lunch_time": 11 <= now.hour <= 14,
        "is_dinner_time": 17 <= now.hour <= 20
    }


@ara.tool(id="scan_campus_events")
def scan_campus_events(campus: str = "JHU") -> dict:
    """
    Scan campus event calendars for upcoming events.

    Args:
        campus: Campus to scan (e.g., "JHU", "Cornell", "Stanford")

    Returns:
        List of upcoming events
    """
    # In production, this would scrape real event sources
    # Demo data for hackathon
    events = [
        {
            "id": "evt_001",
            "title": "Tech Talk: Building with AI",
            "location": "Bloomberg Center 462",
            "time": "Today 12:00 PM",
            "description": "Join us for a talk on AI development. Lunch will be provided.",
            "source": "CS Department Calendar"
        },
        {
            "id": "evt_002",
            "title": "Startup Pitch Night",
            "location": "Hodson Hall 210",
            "time": "Today 6:00 PM",
            "description": "Watch student startups pitch. Free pizza and drinks!",
            "source": "Entrepreneurship Center"
        },
        {
            "id": "evt_003",
            "title": "Study Break",
            "location": "Brody Learning Commons",
            "time": "Today 9:00 PM",
            "description": "Take a break from studying. Snacks provided.",
            "source": "Student Life"
        },
        {
            "id": "evt_004",
            "title": "Research Symposium",
            "location": "Glass Pavilion",
            "time": "Tomorrow 11:00 AM",
            "description": "Annual research presentations with catered reception.",
            "source": "Graduate School"
        },
        {
            "id": "evt_005",
            "title": "Club Meeting: ACM",
            "location": "Malone 228",
            "time": "Tomorrow 5:00 PM",
            "description": "Weekly meeting to discuss upcoming hackathons. Chipotle provided!",
            "source": "Student Clubs"
        }
    ]

    return {
        "campus": campus,
        "events_found": len(events),
        "events": events,
        "scan_time": datetime.now(timezone.utc).isoformat()
    }


@ara.tool(id="detect_free_food")
def detect_free_food(event_description: str, event_title: str) -> dict:
    """
    Analyze an event to detect if free food is available.

    Args:
        event_description: The event description text
        event_title: The event title

    Returns:
        Food detection results
    """
    text = (event_description + " " + event_title).lower()

    # Food keywords
    food_signals = [
        "free food", "free pizza", "free lunch", "free dinner",
        "lunch provided", "dinner provided", "food provided",
        "catered", "refreshments", "snacks", "pizza", "chipotle",
        "tacos", "sandwiches", "breakfast", "brunch", "buffet",
        "will be served", "complimentary", "on us"
    ]

    detected_signals = [s for s in food_signals if s in text]
    has_food = len(detected_signals) > 0

    # Confidence scoring
    if len(detected_signals) >= 3:
        confidence = "high"
        food_score = 95
    elif len(detected_signals) >= 2:
        confidence = "high"
        food_score = 85
    elif len(detected_signals) == 1:
        confidence = "medium"
        food_score = 70
    else:
        confidence = "low"
        food_score = 20

    return {
        "has_free_food": has_food,
        "confidence": confidence,
        "food_score": food_score,
        "signals_detected": detected_signals,
        "signal_count": len(detected_signals)
    }


@ara.tool(id="get_user_preferences")
def get_user_preferences() -> dict:
    """
    Get user's food and event preferences.

    Returns:
        User preferences for filtering events
    """
    # In production, this would load from user settings
    return {
        "preferred_food": ["pizza", "chipotle", "tacos", "sandwiches"],
        "dietary_restrictions": [],
        "max_distance_minutes": 15,
        "interested_topics": ["tech", "AI", "startups", "research"],
        "notify_hours_before": 2,
        "min_food_score": 60
    }


@ara.tool(id="filter_events_by_preference")
def filter_events_by_preference(
    events: List[Dict],
    preferences: Dict
) -> dict:
    """
    Filter events based on user preferences.

    Args:
        events: List of events with food detection
        preferences: User preferences

    Returns:
        Filtered and ranked events
    """
    min_score = preferences.get("min_food_score", 60)

    qualified_events = []
    for event in events:
        if event.get("food_score", 0) >= min_score:
            qualified_events.append(event)

    # Sort by food score
    qualified_events.sort(key=lambda x: x.get("food_score", 0), reverse=True)

    return {
        "total_events": len(events),
        "qualified_events": len(qualified_events),
        "events": qualified_events,
        "filter_applied": f"food_score >= {min_score}"
    }


@ara.tool(id="send_food_alert")
def send_food_alert(
    event_title: str,
    event_location: str,
    event_time: str,
    food_type: str,
    food_score: int
) -> dict:
    """
    Send a free food alert to the user.

    Args:
        event_title: Name of the event
        event_location: Where the event is
        event_time: When the event starts
        food_type: Type of food detected
        food_score: Confidence score (0-100)

    Returns:
        Confirmation of alert sent
    """
    # Build alert message
    if food_score >= 90:
        emoji = "🍕🔥"
        urgency = "HIGH CONFIDENCE"
    elif food_score >= 70:
        emoji = "🍕"
        urgency = "LIKELY"
    else:
        emoji = "🍴"
        urgency = "POSSIBLE"

    message = f"""
{emoji} FREE FOOD ALERT {emoji}

📍 {event_title}
📍 {event_location}
🕐 {event_time}

🍽️ Food: {food_type}
📊 Confidence: {urgency} ({food_score}%)

Don't miss out! 🏃‍♂️
    """

    return {
        "status": "sent",
        "channel": "telegram",
        "message": message.strip(),
        "event_title": event_title,
        "food_score": food_score,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@ara.tool(id="send_daily_digest")
def send_daily_digest(events: List[Dict]) -> dict:
    """
    Send a daily digest of upcoming free food events.

    Args:
        events: List of events with free food

    Returns:
        Confirmation of digest sent
    """
    if not events:
        message = """
☀️ Daily Food Report

No free food events found today 😢

I'll keep scanning and alert you when something comes up!
        """
    else:
        event_lines = []
        for i, evt in enumerate(events[:5], 1):
            event_lines.append(
                f"{i}. {evt.get('title', 'Event')}\n"
                f"   📍 {evt.get('location', 'TBA')} @ {evt.get('time', 'TBA')}\n"
                f"   🍽️ Score: {evt.get('food_score', '?')}%"
            )

        message = f"""
☀️ Daily Food Report

🍕 Found {len(events)} free food event(s) today!

{chr(10).join(event_lines)}

Reply /details [number] for more info.
        """

    return {
        "status": "sent",
        "channel": "telegram",
        "message": message.strip(),
        "events_count": len(events),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@ara.tool(id="subscribe_to_source")
def subscribe_to_source(source_url: str, source_name: str) -> dict:
    """
    Subscribe to a new event source for monitoring.

    Args:
        source_url: URL of the event calendar/feed
        source_name: Friendly name for the source

    Returns:
        Subscription confirmation
    """
    return {
        "status": "subscribed",
        "source_name": source_name,
        "source_url": source_url,
        "check_frequency": "hourly",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# =============================================================================
# AUTOMATION - The Free Food Fetcher agent
# =============================================================================

freefood = ara.Automation(
    id="freefood",
    system_instructions="""
You are Free Food Fetcher, an AI agent that helps users never miss free food events.

## Your Mission
Find free food on campus and alert users before events start.

## Your Workflow

1. **Check Time**: Use get_current_time to know if it's meal time
2. **Scan Events**: Use scan_campus_events to find upcoming events
3. **Detect Food**: For each event, use detect_free_food to check for food signals
4. **Get Preferences**: Use get_user_preferences to know what user wants
5. **Filter**: Use filter_events_by_preference to find matching events
6. **Alert**: Use send_food_alert for high-priority events
7. **Digest**: Use send_daily_digest for daily summary

## Alert Priority

- food_score >= 90: Send immediately with 🔥
- food_score >= 70: Include in digest, alert if < 2 hours away
- food_score >= 50: Include in digest only

## Food Detection Tips

Look for signals like:
- "lunch provided", "dinner provided"
- "free pizza", "free food"
- "catered", "refreshments"
- Specific food names (Chipotle, sandwiches, etc.)

## Personality

Be fun and enthusiastic about free food! Use food emojis 🍕🌮🥪
Users love when you're excited about good finds.

Always prioritize events happening soon over future events.
""",
    tools=[
        get_current_time,
        scan_campus_events,
        detect_free_food,
        get_user_preferences,
        filter_events_by_preference,
        send_food_alert,
        send_daily_digest,
        subscribe_to_source
    ],
    allow_connector_tools=True,
)


# =============================================================================
# CLI - For local testing
# =============================================================================

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║     🍕 FREE FOOD FETCHER 🍕                                               ║
║                                                                           ║
║     Never Miss Free Food Again                                            ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   Commands:                                                               ║
║     ara deploy freefood_ara.py                    # Deploy to Ara         ║
║     ara deploy freefood_ara.py --cron "0 * * * *" # Check every hour      ║
║     ara run freefood_ara.py                       # Run now               ║
║     ara logs freefood_ara.py                      # View logs             ║
║                                                                           ║
║   Tools Available:                                                        ║
║     • scan_campus_events     - Find events on campus                      ║
║     • detect_free_food       - Check if event has food                    ║
║     • get_user_preferences   - Load user food preferences                 ║
║     • filter_events          - Match events to preferences                ║
║     • send_food_alert        - Send notification                          ║
║     • send_daily_digest      - Daily summary                              ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
""")

    # Demo the tools
    print("\n🔍 Testing tools locally...\n")

    print("1. Scanning campus events...")
    events = scan_campus_events("JHU")
    print(f"   Found {events['events_found']} events\n")

    print("2. Detecting free food in events...")
    for evt in events["events"][:3]:
        result = detect_free_food(evt["description"], evt["title"])
        emoji = "✅" if result["has_free_food"] else "❌"
        print(f"   {emoji} {evt['title'][:40]}")
        if result["has_free_food"]:
            print(f"      └─ Score: {result['food_score']}% | Signals: {result['signals_detected']}")

    print("\n3. Sample alert:")
    alert = send_food_alert(
        "Tech Talk: Building with AI",
        "Bloomberg 462",
        "Today 12:00 PM",
        "Lunch provided",
        85
    )
    print(alert["message"])

    print("\n✅ Ready to deploy! Run: ara deploy freefood_ara.py")
