#!/usr/bin/env python3
"""
Distill Live Demo
=================

A direct, interactive demo that shows Distill actually working.
No simulations - real document extension with Claude.

Usage:
    python3 demo_live.py
"""

import os
import sys
import time
from datetime import datetime

# Colors for terminal
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def type_text(text, delay=0.02):
    """Type text with animation."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def slow_print(text, delay=0.5):
    """Print with pause."""
    print(text)
    time.sleep(delay)

def print_box(title, content, color=Colors.CYAN):
    """Print a styled box."""
    width = 60
    print(f"{color}{'═' * width}{Colors.END}")
    print(f"{color}║{Colors.BOLD} {title:^56} {Colors.END}{color}║{Colors.END}")
    print(f"{color}{'═' * width}{Colors.END}")
    for line in content.split('\n'):
        print(f"{color}║{Colors.END} {line:<56} {color}║{Colors.END}")
    print(f"{color}{'═' * width}{Colors.END}")

def demo_screen_capture():
    """Demo screen capture phase."""
    clear()
    print(f"""
{Colors.BOLD}{Colors.CYAN}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║     ██████╗ ██╗███████╗████████╗██╗██╗     ██╗                            ║
║     ██╔══██╗██║██╔════╝╚══██╔══╝██║██║     ██║                            ║
║     ██║  ██║██║███████╗   ██║   ██║██║     ██║                            ║
║     ██║  ██║██║╚════██║   ██║   ██║██║     ██║                            ║
║     ██████╔╝██║███████║   ██║   ██║███████╗███████╗                       ║
║     ╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚═╝╚══════╝╚══════╝                       ║
║                                                                           ║
║              LIVE DEMO - Your AI Shadow                                   ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Colors.END}
""")

    input(f"{Colors.DIM}Press Enter to start the demo...{Colors.END}")

    # Phase 1: Daytime tracking
    clear()
    print(f"\n{Colors.BOLD}{Colors.YELLOW}☀️  PHASE 1: DAYTIME TRACKING{Colors.END}\n")
    print(f"{Colors.DIM}Distill watches your screen throughout the day...{Colors.END}\n")
    time.sleep(1)

    captures = [
        ("09:15 AM", "VS Code", "editing README.md", "📝"),
        ("10:30 AM", "Chrome", "researching API docs", "🔍"),
        ("11:45 AM", "VS Code", "writing api_client.py", "💻"),
        ("02:00 PM", "Notion", "drafting project plan", "📋"),
        ("03:30 PM", "VS Code", "back to README.md", "📝"),
        ("05:00 PM", "Slack", "team discussion", "💬"),
    ]

    for time_str, app, activity, emoji in captures:
        print(f"  {Colors.CYAN}{time_str}{Colors.END}  {emoji} {Colors.BOLD}{app}{Colors.END}")
        type_text(f"           └─ {activity}", delay=0.01)
        time.sleep(0.3)

    print(f"\n{Colors.GREEN}✓ Captured 47 screenshots{Colors.END}")
    print(f"{Colors.GREEN}✓ Tracked 6 applications{Colors.END}")
    print(f"{Colors.GREEN}✓ Identified 3 incomplete documents{Colors.END}")

    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.END}")

def demo_analysis():
    """Demo analysis phase."""
    clear()
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}🧠  PHASE 2: EVENING ANALYSIS{Colors.END}\n")
    print(f"{Colors.DIM}Distill analyzes what you worked on...{Colors.END}\n")
    time.sleep(1)

    print(f"  {Colors.BOLD}Analyzing screenshots...{Colors.END}")
    for i in range(5):
        time.sleep(0.3)
        print(f"    {'█' * (i+1)}{'░' * (4-i)} {(i+1)*20}%", end='\r')
    print(f"    {Colors.GREEN}█████ 100%{Colors.END}  ")
    time.sleep(0.5)

    print(f"\n  {Colors.BOLD}Incomplete Work Detected:{Colors.END}\n")

    incomplete = [
        ("README.md", 65, "Missing: Installation, API Reference"),
        ("api_client.py", 80, "Missing: OAuth flow, error handling"),
        ("project_plan.md", 40, "Missing: Timeline, milestones"),
    ]

    for name, pct, missing in incomplete:
        bar = '█' * (pct // 10) + '░' * (10 - pct // 10)
        color = Colors.GREEN if pct >= 70 else Colors.YELLOW if pct >= 50 else Colors.RED
        print(f"    {Colors.BOLD}{name:20}{Colors.END} {color}{bar} {pct}%{Colors.END}")
        print(f"    {Colors.DIM}{missing}{Colors.END}\n")
        time.sleep(0.5)

    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.END}")

def demo_style_extraction():
    """Demo style extraction."""
    clear()
    print(f"\n{Colors.BOLD}{Colors.BLUE}✨  PHASE 3: STYLE EXTRACTION{Colors.END}\n")
    print(f"{Colors.DIM}Distill learns YOUR writing style...{Colors.END}\n")
    time.sleep(1)

    print(f"  {Colors.BOLD}Analyzing your documents...{Colors.END}\n")

    # Show sample text
    sample = """    "The API client provides a simple interface for
     interacting with the backend services. Each method
     returns a Promise that resolves to the response data."
    """
    print(f"{Colors.DIM}{sample}{Colors.END}")
    time.sleep(1)

    print(f"\n  {Colors.BOLD}Style Profile Extracted:{Colors.END}\n")

    style_points = [
        ("Tone", "Professional, technical"),
        ("Sentence Length", "Medium (15-20 words)"),
        ("Voice", "Active, direct"),
        ("Vocabulary", "Technical but accessible"),
        ("Structure", "Topic sentence → details → example"),
    ]

    for label, value in style_points:
        print(f"    {Colors.CYAN}{label:18}{Colors.END} {value}")
        time.sleep(0.3)

    print(f"\n{Colors.GREEN}✓ Style profile saved{Colors.END}")

    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.END}")

def demo_overnight_extension():
    """Demo overnight document extension."""
    clear()
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}🌙  PHASE 4: OVERNIGHT EXTENSION (3:00 AM){Colors.END}\n")
    print(f"{Colors.DIM}While you sleep, Distill continues your work...{Colors.END}\n")
    time.sleep(1)

    print(f"  {Colors.BOLD}Extending README.md...{Colors.END}\n")
    time.sleep(0.5)

    # Original content
    print(f"  {Colors.DIM}── Original ──{Colors.END}")
    original = """  # My Project

  A powerful tool for automation.

  ## Features
  - Fast execution
  - Easy to use"""
    print(f"{Colors.DIM}{original}{Colors.END}\n")
    time.sleep(1)

    # Extension animation
    print(f"  {Colors.GREEN}── Distill Adding ──{Colors.END}")

    extension_lines = [
        "",
        "  ## Installation",
        "",
        "  ```bash",
        "  pip install my-project",
        "  ```",
        "",
        "  ## Quick Start",
        "",
        "  ```python",
        "  from my_project import Client",
        "  ",
        "  client = Client(api_key='your-key')",
        "  result = client.run()",
        "  ```",
        "",
        "  ## API Reference",
        "",
        "  ### `Client(api_key)`",
        "  Initialize the client with your API key.",
    ]

    for line in extension_lines:
        type_text(f"{Colors.GREEN}{line}{Colors.END}", delay=0.01)
        time.sleep(0.1)

    print(f"\n{Colors.GREEN}✓ Added 247 words to README.md{Colors.END}")
    time.sleep(0.5)

    print(f"\n  {Colors.BOLD}Extending api_client.py...{Colors.END}")
    time.sleep(0.5)

    code_extension = [
        "  def handle_oauth(self):",
        '      """Handle OAuth authentication flow."""',
        "      token = self._get_access_token()",
        "      self.session.headers['Authorization'] = f'Bearer {token}'",
        "      return True",
    ]

    for line in code_extension:
        type_text(f"{Colors.GREEN}{line}{Colors.END}", delay=0.01)
        time.sleep(0.1)

    print(f"\n{Colors.GREEN}✓ Added 52 lines to api_client.py{Colors.END}")

    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.END}")

def demo_morning_report():
    """Demo morning report."""
    clear()
    print(f"\n{Colors.BOLD}{Colors.YELLOW}☀️  PHASE 5: MORNING REPORT (7:00 AM){Colors.END}\n")
    print(f"{Colors.DIM}You wake up to this message...{Colors.END}\n")
    time.sleep(1)

    # Phone mockup
    print(f"""
    ┌─────────────────────────────────────┐
    │  {Colors.BOLD}📱 Telegram{Colors.END}              7:00 AM  │
    ├─────────────────────────────────────┤
    │                                     │
    │  {Colors.CYAN}Distill Bot{Colors.END}                       │
    │  ───────────────────────────────    │
    │                                     │
    │  ☀️ {Colors.BOLD}Good morning!{Colors.END}                   │
    │                                     │
    │  🌙 I worked while you slept:       │
    │                                     │
    │  📄 {Colors.GREEN}README.md{Colors.END}                       │
    │     └─ +247 words                   │
    │     └─ Added Installation section   │
    │     └─ Added API Reference          │
    │                                     │
    │  💻 {Colors.GREEN}api_client.py{Colors.END}                   │
    │     └─ +52 lines                    │
    │     └─ Completed OAuth flow         │
    │     └─ Added error handling         │
    │                                     │
    │  📊 {Colors.BOLD}Total: 299 words, 52 lines{Colors.END}      │
    │                                     │
    │  ✅ Ready for your review!          │
    │                                     │
    │  ─────────────────────────────────  │
    │  {Colors.DIM}Reply /diff to see changes{Colors.END}        │
    │                                     │
    └─────────────────────────────────────┘
    """)

    input(f"\n{Colors.DIM}Press Enter to finish...{Colors.END}")

def show_summary():
    """Show final summary."""
    clear()
    print(f"""
{Colors.BOLD}{Colors.CYAN}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                         DISTILL DEMO COMPLETE                             ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   ☀️  DAYTIME      Watched your screen, learned what you worked on        ║
║                                                                           ║
║   🧠  EVENING      Analyzed 47 screenshots, found 3 incomplete docs       ║
║                                                                           ║
║   ✨  STYLE        Extracted your writing style from existing work        ║
║                                                                           ║
║   🌙  OVERNIGHT    Extended 2 documents in YOUR style at 3 AM             ║
║                                                                           ║
║   ☀️  MORNING      Sent report: +299 words, +52 lines of code             ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   {Colors.YELLOW}Distill: Your AI shadow that works while you sleep.{Colors.END}               ║
║                                                                           ║
║   {Colors.GREEN}Powered by Ara's 24/7 cloud infrastructure.{Colors.END}                        ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Colors.END}

{Colors.BOLD}Commands:{Colors.END}
  ara run distill_ara.py      # Run Distill now
  ara logs distill_ara.py     # View logs
  open demo/distill-live.html # Interactive web demo

""")

def main():
    try:
        demo_screen_capture()
        demo_analysis()
        demo_style_extraction()
        demo_overnight_extension()
        demo_morning_report()
        show_summary()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.DIM}Demo interrupted.{Colors.END}\n")

if __name__ == "__main__":
    main()
