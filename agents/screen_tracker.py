"""
Distill Screen Tracker
======================

Tracks your screen throughout the day to understand what you're working on.
Uses periodic screenshots + Claude Vision to build context.

Components:
1. ScreenCapture - Takes periodic screenshots
2. ActivityTracker - Tracks active apps/windows
3. ContextBuilder - Builds understanding of your work
4. WorkSession - Stores the day's activity
"""

import os
import subprocess
import json
import base64
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class ScreenCapture:
    """Captures screenshots periodically."""

    def __init__(self, capture_dir: str = "captures"):
        self.capture_dir = Path(capture_dir)
        self.capture_dir.mkdir(exist_ok=True)

    def capture(self) -> Optional[str]:
        """Take a screenshot and return the filepath."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = self.capture_dir / f"screen_{timestamp}.png"

        try:
            # macOS screenshot command
            subprocess.run(
                ["screencapture", "-x", "-C", str(filepath)],
                check=True,
                capture_output=True
            )
            return str(filepath)
        except subprocess.CalledProcessError as e:
            print(f"Screenshot failed: {e}")
            return None
        except FileNotFoundError:
            # Not on macOS, try alternative
            print("screencapture not found. Using placeholder.")
            return None

    def get_active_window(self) -> Dict:
        """Get info about the currently active window (macOS)."""
        try:
            # AppleScript to get active app and window
            script = '''
            tell application "System Events"
                set frontApp to name of first application process whose frontmost is true
                set frontWindow to ""
                try
                    tell process frontApp
                        set frontWindow to name of front window
                    end tell
                end try
            end tell
            return frontApp & "|" & frontWindow
            '''
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True
            )
            parts = result.stdout.strip().split("|")
            return {
                "app": parts[0] if parts else "Unknown",
                "window": parts[1] if len(parts) > 1 else "",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "app": "Unknown",
                "window": "",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

    def encode_image(self, filepath: str) -> str:
        """Encode image to base64 for API."""
        with open(filepath, "rb") as f:
            return base64.standard_b64encode(f.read()).decode("utf-8")


class ActivityTracker:
    """Tracks user activity throughout the day."""

    def __init__(self):
        self.activities: List[Dict] = []
        self.screen_capture = ScreenCapture()

    def record_activity(self) -> Dict:
        """Record current activity (screenshot + active window)."""
        window_info = self.screen_capture.get_active_window()
        screenshot_path = self.screen_capture.capture()

        activity = {
            "timestamp": datetime.now().isoformat(),
            "app": window_info.get("app", "Unknown"),
            "window_title": window_info.get("window", ""),
            "screenshot": screenshot_path
        }

        self.activities.append(activity)
        return activity

    def get_activity_summary(self) -> Dict:
        """Summarize the day's activities."""
        if not self.activities:
            return {"summary": "No activities recorded"}

        # Count time per app
        app_time = {}
        for activity in self.activities:
            app = activity.get("app", "Unknown")
            app_time[app] = app_time.get(app, 0) + 1

        # Sort by usage
        sorted_apps = sorted(app_time.items(), key=lambda x: x[1], reverse=True)

        return {
            "total_captures": len(self.activities),
            "time_range": {
                "start": self.activities[0]["timestamp"],
                "end": self.activities[-1]["timestamp"]
            },
            "app_usage": dict(sorted_apps[:10]),
            "activities": self.activities
        }


class VisionAnalyzer:
    """Analyzes screenshots using Claude Vision."""

    def analyze_screenshot(self, image_path: str) -> Dict:
        """Analyze a screenshot to understand what user is working on."""
        try:
            with open(image_path, "rb") as f:
                image_data = base64.standard_b64encode(f.read()).decode("utf-8")

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_data
                            }
                        },
                        {
                            "type": "text",
                            "text": """Analyze this screenshot and extract:
1. What application is being used?
2. What task is the user working on?
3. What content is visible (document title, code, email subject, etc.)?
4. What is the user likely trying to accomplish?
5. Is there any incomplete work visible?

Be specific and concise. Format as JSON:
{
    "application": "app name",
    "task": "what they're doing",
    "content_summary": "brief description of visible content",
    "user_intent": "what they're trying to accomplish",
    "incomplete_work": "any unfinished items visible",
    "key_details": ["specific details that might be useful"]
}"""
                        }
                    ]
                }]
            )

            try:
                return json.loads(response.content[0].text)
            except json.JSONDecodeError:
                return {"raw_analysis": response.content[0].text}

        except Exception as e:
            return {"error": str(e)}

    def analyze_work_session(self, screenshots: List[str]) -> Dict:
        """Analyze multiple screenshots to build session context."""
        analyses = []

        for path in screenshots[-10:]:  # Analyze last 10 screenshots
            if path and os.path.exists(path):
                analysis = self.analyze_screenshot(path)
                analyses.append(analysis)

        # Synthesize into session summary
        if not analyses:
            return {"summary": "No screenshots to analyze"}

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": f"""Based on these screenshot analyses from a work session, create a comprehensive summary:

ANALYSES:
{json.dumps(analyses, indent=2)}

Provide:
1. Overall summary of what the user was working on
2. Main projects/tasks identified
3. Any incomplete work that could be continued
4. The user's apparent priorities
5. Suggested next steps

Format as JSON:
{{
    "session_summary": "overall description",
    "main_projects": ["list of projects"],
    "incomplete_work": [
        {{
            "item": "description",
            "context": "relevant context",
            "suggested_continuation": "how to continue this"
        }}
    ],
    "priorities": ["apparent priorities"],
    "recommended_actions": ["what distill should do overnight"]
}}"""
            }]
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"raw_synthesis": response.content[0].text}


class WorkSession:
    """Manages a full work day session."""

    def __init__(self, session_dir: str = "sessions"):
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)

        self.session_id = datetime.now().strftime("%Y%m%d")
        self.session_file = self.session_dir / f"session_{self.session_id}.json"

        self.tracker = ActivityTracker()
        self.analyzer = VisionAnalyzer()

        # Load existing session or create new
        self.data = self._load_session()

    def _load_session(self) -> Dict:
        """Load existing session or create new."""
        if self.session_file.exists():
            with open(self.session_file) as f:
                return json.load(f)
        return {
            "session_id": self.session_id,
            "started": datetime.now().isoformat(),
            "activities": [],
            "analyses": [],
            "summary": None
        }

    def _save_session(self):
        """Save session to disk."""
        with open(self.session_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def capture_now(self) -> Dict:
        """Capture current screen and activity."""
        activity = self.tracker.record_activity()
        self.data["activities"].append(activity)
        self._save_session()

        print(f"📸 Captured: {activity['app']} - {activity['window_title'][:50]}")
        return activity

    def start_tracking(self, interval_seconds: int = 300):
        """Start continuous tracking (every N seconds)."""
        print(f"🔍 Starting screen tracking (every {interval_seconds}s)")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                self.capture_now()
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n⏹️ Tracking stopped")
            self.end_session()

    def analyze_session(self) -> Dict:
        """Analyze the full session with vision."""
        print("🧠 Analyzing session...")

        screenshots = [a.get("screenshot") for a in self.data["activities"] if a.get("screenshot")]

        if not screenshots:
            return {"error": "No screenshots to analyze"}

        analysis = self.analyzer.analyze_work_session(screenshots)
        self.data["summary"] = analysis
        self._save_session()

        return analysis

    def end_session(self) -> Dict:
        """End session and generate final summary."""
        self.data["ended"] = datetime.now().isoformat()

        # Generate analysis
        summary = self.analyze_session()

        print("\n" + "=" * 50)
        print("📊 SESSION SUMMARY")
        print("=" * 50)
        print(json.dumps(summary, indent=2))

        return summary

    def get_context_for_distill(self) -> Dict:
        """Get session context formatted for Distill agent."""
        if not self.data.get("summary"):
            self.analyze_session()

        return {
            "session_id": self.session_id,
            "duration": self._calculate_duration(),
            "summary": self.data.get("summary", {}),
            "recent_activities": self.data["activities"][-20:],
            "incomplete_work": self.data.get("summary", {}).get("incomplete_work", [])
        }

    def _calculate_duration(self) -> str:
        """Calculate session duration."""
        if not self.data["activities"]:
            return "0 minutes"

        start = datetime.fromisoformat(self.data["activities"][0]["timestamp"])
        end = datetime.fromisoformat(self.data["activities"][-1]["timestamp"])
        duration = end - start

        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60

        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes} minutes"


class DistillWithTracking:
    """Full Distill agent with screen tracking integration."""

    def __init__(self):
        self.session = WorkSession()
        self.analyzer = VisionAnalyzer()

    def start_day(self, capture_interval: int = 300):
        """Start tracking for the day."""
        print("🌅 Starting Distill day tracking")
        print(f"📸 Will capture screen every {capture_interval // 60} minutes")
        self.session.start_tracking(capture_interval)

    def end_day_and_extend(self) -> Dict:
        """End tracking and run overnight extension."""
        print("\n🌙 Ending day, preparing for overnight work...")

        # Get session context
        context = self.session.get_context_for_distill()

        print(f"\n📊 Session duration: {context['duration']}")
        print(f"📸 Screenshots captured: {len(self.session.data['activities'])}")

        # Show incomplete work found
        incomplete = context.get("incomplete_work", [])
        if incomplete:
            print(f"\n🔍 Found {len(incomplete)} incomplete items:")
            for item in incomplete:
                print(f"   • {item.get('item', 'Unknown')}")

        return context

    def generate_overnight_plan(self, context: Dict) -> str:
        """Generate plan for what Distill will do overnight."""
        incomplete = context.get("summary", {}).get("incomplete_work", [])
        actions = context.get("summary", {}).get("recommended_actions", [])

        plan = f"""
🌙 DISTILL OVERNIGHT PLAN
{'=' * 40}

Based on your work session ({context.get('duration', 'unknown duration')}),
here's what I'll work on tonight:

📋 INCOMPLETE WORK DETECTED:
"""
        for i, item in enumerate(incomplete[:5], 1):
            plan += f"\n{i}. {item.get('item', 'Unknown task')}"
            if item.get('suggested_continuation'):
                plan += f"\n   → {item.get('suggested_continuation')}"

        plan += f"""

🎯 PLANNED ACTIONS:
"""
        for i, action in enumerate(actions[:5], 1):
            plan += f"\n{i}. {action}"

        plan += f"""

⏰ I'll work on this at 3:00 AM and have results ready by 7:00 AM.

{'=' * 40}
"""
        return plan


# Demo / Test mode
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Distill Screen Tracker")
    parser.add_argument("--capture", action="store_true", help="Capture single screenshot")
    parser.add_argument("--track", type=int, default=0, help="Start tracking (interval in seconds)")
    parser.add_argument("--analyze", action="store_true", help="Analyze current session")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")

    args = parser.parse_args()

    if args.capture:
        session = WorkSession()
        activity = session.capture_now()
        print(f"Captured: {activity}")

    elif args.track > 0:
        distill = DistillWithTracking()
        distill.start_day(capture_interval=args.track)

    elif args.analyze:
        session = WorkSession()
        summary = session.analyze_session()
        print(json.dumps(summary, indent=2))

    elif args.demo:
        print("""
🌙 DISTILL SCREEN TRACKER - DEMO MODE
=====================================

This demonstrates how Distill tracks your work throughout the day.

COMMANDS:
  python screen_tracker.py --capture     # Take one screenshot
  python screen_tracker.py --track 60    # Track every 60 seconds
  python screen_tracker.py --analyze     # Analyze session

FULL DAY FLOW:
  1. Morning: Start tracking
     $ python screen_tracker.py --track 300

  2. Work normally throughout the day
     (Distill captures screenshots every 5 minutes)

  3. Evening: Stop tracking (Ctrl+C)
     Distill analyzes your session and identifies incomplete work

  4. Overnight: Distill extends your work
     Uses the context from your day to continue documents

  5. Morning: Review what Distill did
     Get a report of extensions and changes

""")

    else:
        # Default: show status
        session = WorkSession()
        print(f"Session: {session.session_id}")
        print(f"Activities recorded: {len(session.data['activities'])}")
        if session.data['activities']:
            print(f"Last capture: {session.data['activities'][-1]['timestamp']}")
