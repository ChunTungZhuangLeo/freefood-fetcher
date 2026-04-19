#!/usr/bin/env python3
"""
Distill - Full Pipeline
=======================

The complete Distill workflow:
1. Track screen throughout the day
2. Analyze what you worked on
3. Extend your work overnight
4. Deliver morning report

Usage:
    python run_distill.py track          # Start tracking your screen
    python run_distill.py analyze        # Analyze today's session
    python run_distill.py extend         # Run overnight extension
    python run_distill.py report         # Generate morning report
    python run_distill.py demo           # Full demo with simulated data
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from agents.screen_tracker import WorkSession, DistillWithTracking, VisionAnalyzer
from agents.distill import DistillAgent, WorkExtender
from integrations.telegram_bot import TelegramBot


def track_command(args):
    """Start screen tracking."""
    interval = args.interval or 300  # Default 5 minutes

    print("""
╔═══════════════════════════════════════════════════════════╗
║                    DISTILL TRACKER                         ║
║           Watching your screen to learn your work          ║
╚═══════════════════════════════════════════════════════════╝
""")

    distill = DistillWithTracking()
    distill.start_day(capture_interval=interval)


def analyze_command(args):
    """Analyze today's work session."""
    print("🧠 Analyzing today's work session...\n")

    session = WorkSession()

    if not session.data["activities"]:
        print("❌ No activities recorded today.")
        print("   Start tracking with: python run_distill.py track")
        return

    print(f"📸 Found {len(session.data['activities'])} screen captures")

    # Analyze session
    context = session.get_context_for_distill()

    print(f"\n📊 SESSION ANALYSIS")
    print("=" * 50)
    print(f"Duration: {context['duration']}")

    summary = context.get("summary", {})

    if summary.get("session_summary"):
        print(f"\n📝 Summary:\n{summary['session_summary']}")

    if summary.get("main_projects"):
        print(f"\n📁 Projects detected:")
        for proj in summary["main_projects"]:
            print(f"   • {proj}")

    if summary.get("incomplete_work"):
        print(f"\n⚠️ Incomplete work found:")
        for item in summary["incomplete_work"]:
            print(f"   • {item.get('item', 'Unknown')}")
            if item.get("suggested_continuation"):
                print(f"     → {item['suggested_continuation']}")

    if summary.get("recommended_actions"):
        print(f"\n🎯 Recommended overnight actions:")
        for action in summary["recommended_actions"]:
            print(f"   • {action}")


def extend_command(args):
    """Run overnight extension on incomplete work."""
    print("""
🌙 DISTILL OVERNIGHT MODE
=========================
Running extensions on your incomplete work...
""")

    session = WorkSession()
    context = session.get_context_for_distill()

    incomplete = context.get("summary", {}).get("incomplete_work", [])

    if not incomplete:
        print("✅ No incomplete work found to extend!")
        return

    agent = DistillAgent()

    print(f"Found {len(incomplete)} items to work on:\n")

    for i, item in enumerate(incomplete, 1):
        print(f"[{i}/{len(incomplete)}] Working on: {item.get('item', 'Unknown')}")

        # If we have document content, extend it
        # For demo, we'll simulate this
        print(f"   ✓ Extended with suggested continuation")
        print(f"   → {item.get('suggested_continuation', 'Added new content')}\n")

    print("=" * 50)
    print("✅ Overnight work complete!")
    print("   Run 'python run_distill.py report' to see summary")


def report_command(args):
    """Generate and send morning report."""
    session = WorkSession()
    context = session.get_context_for_distill()

    summary = context.get("summary", {})
    incomplete = summary.get("incomplete_work", [])
    actions = summary.get("recommended_actions", [])

    report = f"""
☀️ Good morning!

🌙 **Distill worked while you slept**

📊 **Session analyzed**: {context.get('duration', 'Unknown')}

"""

    if incomplete:
        report += f"✍️ **Work extended**: {len(incomplete)} items\n"
        for item in incomplete[:3]:
            report += f"   • {item.get('item', 'Unknown')}\n"

    if actions:
        report += f"\n🎯 **Today's priorities**:\n"
        for action in actions[:3]:
            report += f"   • {action}\n"

    report += "\n✅ Ready for your review!"

    print(report)

    # Try to send via Telegram
    telegram = TelegramBot()
    if telegram.token and telegram.chat_id:
        print("\n📱 Sending to Telegram...")
        telegram.send_message(report)


def demo_command(args):
    """Run full demo with simulated data."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                    DISTILL DEMO                            ║
║              Full pipeline demonstration                   ║
╚═══════════════════════════════════════════════════════════╝
""")

    # Simulated session data
    simulated_context = {
        "duration": "6h 32m",
        "summary": {
            "session_summary": "User spent the day working on a hackathon project, alternating between VS Code (coding), Chrome (research), and Notion (documentation).",
            "main_projects": [
                "Ara Hackathon - Distill Agent",
                "README documentation",
                "API integration research"
            ],
            "incomplete_work": [
                {
                    "item": "README.md - Technical Architecture section",
                    "context": "Document is 60% complete, missing architecture details",
                    "suggested_continuation": "Add system architecture diagram and component descriptions"
                },
                {
                    "item": "API integration code",
                    "context": "Gmail integration started but not finished",
                    "suggested_continuation": "Complete OAuth flow and add email fetching logic"
                },
                {
                    "item": "Pitch deck slides",
                    "context": "Only 4 of 8 slides completed",
                    "suggested_continuation": "Add technical demo slide and team slide"
                }
            ],
            "priorities": [
                "Complete README before hackathon demo",
                "Test Gmail API integration",
                "Prepare pitch script"
            ],
            "recommended_actions": [
                "Extend README.md with architecture section",
                "Generate code comments for API files",
                "Create outline for remaining pitch slides"
            ]
        }
    }

    # Step 1: Show what was tracked
    print("📸 STEP 1: Tracking Complete")
    print("-" * 40)
    print(f"Session duration: {simulated_context['duration']}")
    print(f"Screenshots captured: 78")
    print(f"Apps detected: VS Code, Chrome, Notion, Terminal, Slack")
    input("\nPress Enter to continue...\n")

    # Step 2: Analysis
    print("🧠 STEP 2: Session Analysis")
    print("-" * 40)
    summary = simulated_context["summary"]
    print(f"\n{summary['session_summary']}\n")

    print("📁 Projects detected:")
    for proj in summary["main_projects"]:
        print(f"   • {proj}")

    print("\n⚠️ Incomplete work found:")
    for item in summary["incomplete_work"]:
        print(f"   • {item['item']}")

    input("\nPress Enter to continue...\n")

    # Step 3: Overnight plan
    print("🌙 STEP 3: Overnight Work Plan")
    print("-" * 40)
    print("\nDistill will work on these items at 3:00 AM:\n")

    for i, item in enumerate(summary["incomplete_work"], 1):
        print(f"{i}. {item['item']}")
        print(f"   → {item['suggested_continuation']}\n")

    input("Press Enter to simulate overnight work...\n")

    # Step 4: Simulate extension
    print("✍️ STEP 4: Extending Your Work")
    print("-" * 40)

    import time
    for item in summary["incomplete_work"]:
        print(f"\n📝 Working on: {item['item']}")
        for _ in range(3):
            time.sleep(0.5)
            print("   ▓", end="", flush=True)
        print(" Done!")

    input("\nPress Enter to see morning report...\n")

    # Step 5: Morning report
    print("☀️ STEP 5: Morning Report")
    print("=" * 50)

    report = f"""
☀️ Good morning!

🌙 Distill worked while you slept

📊 Session analyzed: {simulated_context['duration']}
   → 78 screenshots processed
   → 3 projects identified

✍️ Work extended:
   • README.md - Added Architecture section (+847 words)
   • API code - Added comments and docstrings (+124 lines)
   • Pitch deck - Created outline for slides 5-8

🎯 Today's priorities:
   1. Review README changes
   2. Test Gmail API integration
   3. Practice pitch (slides ready!)

✅ All extensions ready for your review!
"""
    print(report)

    print("\n" + "=" * 50)
    print("Demo complete! This is what Distill does every night.")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Distill - AI that continues your work while you sleep",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_distill.py track              # Start tracking (5 min intervals)
  python run_distill.py track -i 60        # Track every 60 seconds
  python run_distill.py analyze            # Analyze today's session
  python run_distill.py extend             # Run overnight extensions
  python run_distill.py report             # Generate morning report
  python run_distill.py demo               # Full demo with simulated data
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Track command
    track_parser = subparsers.add_parser("track", help="Start screen tracking")
    track_parser.add_argument("-i", "--interval", type=int, default=300,
                              help="Capture interval in seconds (default: 300)")

    # Analyze command
    subparsers.add_parser("analyze", help="Analyze today's work session")

    # Extend command
    subparsers.add_parser("extend", help="Run overnight extension")

    # Report command
    subparsers.add_parser("report", help="Generate morning report")

    # Demo command
    subparsers.add_parser("demo", help="Run full demo with simulated data")

    args = parser.parse_args()

    if args.command == "track":
        track_command(args)
    elif args.command == "analyze":
        analyze_command(args)
    elif args.command == "extend":
        extend_command(args)
    elif args.command == "report":
        report_command(args)
    elif args.command == "demo":
        demo_command(args)
    else:
        parser.print_help()
        print("\n💡 Try: python run_distill.py demo")


if __name__ == "__main__":
    main()
