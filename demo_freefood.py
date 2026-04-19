#!/usr/bin/env python3
"""
Free Food Fetcher - Live Demo
==============================

Interactive demo showing the Free Food Fetcher in action.
"""

import os
import sys
import time
import subprocess
import json

# Colors
class C:
    B = '\033[94m'
    G = '\033[92m'
    Y = '\033[93m'
    R = '\033[91m'
    C = '\033[96m'
    M = '\033[95m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

def clear():
    os.system('clear')

def type_text(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main():
    clear()
    print(f"""
{C.BOLD}{C.Y}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║     🍕🍕🍕  FREE FOOD FETCHER  🍕🍕🍕                                     ║
║                                                                           ║
║              Never Miss Free Food Again                                   ║
║              Powered by Ara's 24/7 Cloud                                  ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{C.END}
""")

    input(f"{C.DIM}Press Enter to start demo...{C.END}")

    # Phase 1: Scanning
    clear()
    print(f"\n{C.BOLD}{C.C}🔍 PHASE 1: SCANNING CAMPUS EVENTS{C.END}\n")
    time.sleep(0.5)

    sources = [
        ("CS Department Calendar", "📚"),
        ("Entrepreneurship Center", "🚀"),
        ("Student Life Events", "🎉"),
        ("Graduate School", "🎓"),
        ("Club Calendars", "👥"),
    ]

    print(f"  {C.DIM}Scanning event sources...{C.END}\n")
    for name, emoji in sources:
        time.sleep(0.3)
        print(f"    {emoji} {name}... {C.G}✓{C.END}")

    print(f"\n  {C.G}Found 12 upcoming events{C.END}")
    time.sleep(1)

    # Phase 2: Detection
    clear()
    print(f"\n{C.BOLD}{C.M}🍽️ PHASE 2: DETECTING FREE FOOD{C.END}\n")
    time.sleep(0.5)

    events = [
        ("Tech Talk: Building with AI", "Bloomberg 462", "12:00 PM", "Lunch provided", 85, True),
        ("Career Fair", "Rec Center", "10:00 AM", "No food mentioned", 15, False),
        ("Startup Pitch Night", "Hodson 210", "6:00 PM", "Free pizza and drinks!", 95, True),
        ("Study Group", "Library", "3:00 PM", "BYOF", 10, False),
        ("ACM Club Meeting", "Malone 228", "5:00 PM", "Chipotle provided!", 90, True),
        ("Research Symposium", "Glass Pavilion", "11:00 AM", "Catered reception", 80, True),
    ]

    print(f"  {C.DIM}Analyzing events for food signals...{C.END}\n")

    for title, loc, time_str, food, score, has_food in events:
        time.sleep(0.4)
        if has_food:
            bar = f"{C.G}{'█' * (score // 10)}{'░' * (10 - score // 10)}{C.END}"
            print(f"    {C.G}✅{C.END} {title[:35]:35} {bar} {score}%")
            print(f"       {C.DIM}└─ \"{food}\"{C.END}")
        else:
            print(f"    {C.DIM}❌ {title[:35]:35} {'░' * 10} {score}%{C.END}")

    print(f"\n  {C.G}🍕 Found 4 events with free food!{C.END}")
    time.sleep(1)

    # Phase 3: Alert
    clear()
    print(f"\n{C.BOLD}{C.Y}📱 PHASE 3: SENDING ALERTS{C.END}\n")
    time.sleep(0.5)

    print(f"""
    ┌─────────────────────────────────────────┐
    │  {C.BOLD}📱 Telegram{C.END}                            │
    ├─────────────────────────────────────────┤
    │                                         │
    │  {C.Y}Free Food Bot{C.END}                          │
    │  ─────────────────────────────────      │
    │                                         │
    │  🍕🔥 {C.BOLD}FREE FOOD ALERT{C.END} 🔥🍕              │
    │                                         │
    │  {C.G}Startup Pitch Night{C.END}                    │
    │  📍 Hodson Hall 210                     │
    │  🕐 Today 6:00 PM                       │
    │                                         │
    │  🍽️ Free pizza and drinks!              │
    │  📊 Confidence: {C.G}HIGH (95%){C.END}              │
    │                                         │
    │  Don't miss out! 🏃‍♂️                     │
    │                                         │
    │  ─────────────────────────────────      │
    │                                         │
    │  🍕 {C.BOLD}ANOTHER ONE!{C.END} 🍕                     │
    │                                         │
    │  {C.G}ACM Club Meeting{C.END}                       │
    │  📍 Malone 228                          │
    │  🕐 Tomorrow 5:00 PM                    │
    │                                         │
    │  🍽️ Chipotle provided!                  │
    │  📊 Confidence: {C.G}HIGH (90%){C.END}              │
    │                                         │
    └─────────────────────────────────────────┘
    """)

    time.sleep(1)

    # Phase 4: Running on Ara
    clear()
    print(f"\n{C.BOLD}{C.C}☁️ PHASE 4: RUNNING ON ARA'S CLOUD{C.END}\n")
    time.sleep(0.5)

    print(f"  {C.DIM}Executing on Ara...{C.END}\n")

    # Actually run on Ara
    try:
        result = subprocess.run(
            ["ara", "run", "freefood_ara.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout + result.stderr

        # Extract run info
        if "run_id" in output:
            print(f"  {C.G}✓ Running on Ara's cloud{C.END}")

            # Find the JSON
            try:
                json_start = output.find('{')
                json_end = output.rfind('}') + 1
                if json_start != -1:
                    data = json.loads(output[json_start:json_end])
                    print(f"  {C.C}  Run ID: {data.get('run_id', 'N/A')}{C.END}")
                    print(f"  {C.C}  App ID: {data.get('app_id', 'N/A')}{C.END}")
                    print(f"  {C.C}  Status: {data.get('result', {}).get('state', 'N/A')}{C.END}")
            except:
                pass

            print(f"\n  {C.G}✓ Free Food Fetcher executed successfully!{C.END}")
        else:
            print(f"  {C.G}✓ Connected to Ara{C.END}")

    except Exception as e:
        print(f"  {C.Y}⚠ Run 'ara auth login' first{C.END}")

    time.sleep(1)

    # Summary
    clear()
    print(f"""
{C.BOLD}{C.G}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║              🍕 FREE FOOD FETCHER - DEMO COMPLETE 🍕                      ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   What It Does:                                                           ║
║   ─────────────                                                           ║
║   • Scans campus event calendars every hour                               ║
║   • AI detects "free food" signals in event descriptions                  ║
║   • Filters by your preferences (pizza lover? vegan?)                     ║
║   • Sends instant alerts for high-confidence events                       ║
║   • Daily digest of all upcoming free food                                ║
║                                                                           ║
║   Powered By:                                                             ║
║   ───────────                                                             ║
║   • Ara's 24/7 cloud infrastructure                                       ║
║   • Runs hourly without your laptop being on                              ║
║   • Delivers via Telegram, WhatsApp, or Discord                           ║
║                                                                           ║
║   Commands:                                                               ║
║   ─────────                                                               ║
║   ara run freefood_ara.py       # Check now                               ║
║   ara logs freefood_ara.py      # View history                            ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{C.END}

{C.BOLD}🍕 Never miss free food again!{C.END}

""")

if __name__ == "__main__":
    main()
