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
You are Free Food Fetcher. Your job is to find FREE FOOD at JHU.

## YOUR ACTUAL TASK

When run, you MUST:

1. **Actually browse these real URLs** using your web browsing capability:
   - https://hub.jhu.edu/events/
   - https://studentaffairs.jhu.edu/calendar/
   - https://www.cs.jhu.edu/news-events/

2. **For each event you find**, extract:
   - Event name
   - Location (building name)
   - Date and time
   - Any mention of food in the description

3. **Use the analyze_for_food tool** on each event description

4. **Report back** with a list of events that have free food, sorted by confidence

## OUTPUT FORMAT

Output your findings as JSON so it can be loaded into our dashboard:

```json
{
  "scan_time": "2024-04-19T12:00:00Z",
  "source_urls": ["list of URLs you browsed"],
  "events": [
    {
      "id": 1,
      "title": "Event Name",
      "location": "Building Name",
      "time": "Today 6:00 PM",
      "food": "What food is available",
      "confidence": 95,
      "source": "hub.jhu.edu",
      "isPublic": true,
      "signals": ["free pizza", "catered"]
    }
  ],
  "total_scanned": 25,
  "food_found": 3
}
```

IMPORTANT:
- Only include events you ACTUALLY found on the websites
- Don't make up events - be real
- If you cannot access a URL, include it in an "errors" array
- confidence should be 0-100 based on food signals found
""",
    tools=[
        get_current_time,
        analyze_for_food
    ],
    allow_connector_tools=True,  # This lets Ara use web browsing!
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
║  4. Report back what it finds                                             ║
║                                                                           ║
║  This is REAL web browsing by Ara's AI agent!                             ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
""")
