#!/usr/bin/env python3
"""
Deploy Distill to Ara Platform
==============================

This script deploys Distill as a 24/7 agent on Ara's cloud infrastructure.

Usage:
    python deploy_to_ara.py              # Deploy with interactive setup
    python deploy_to_ara.py --demo       # Demo mode (no actual deployment)
    python deploy_to_ara.py --schedule   # Deploy with overnight schedule
"""

import os
import sys
import argparse
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from integrations.ara_platform import get_ara_client, AraConfig
from agents.distill import DistillAgent
from agents.screen_tracker import WorkSession


def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║     ██████╗ ██╗███████╗████████╗██╗██╗     ██╗                            ║
║     ██╔══██╗██║██╔════╝╚══██╔══╝██║██║     ██║                            ║
║     ██║  ██║██║███████╗   ██║   ██║██║     ██║                            ║
║     ██║  ██║██║╚════██║   ██║   ██║██║     ██║                            ║
║     ██████╔╝██║███████║   ██║   ██║███████╗███████╗                       ║
║     ╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚═╝╚══════╝╚══════╝                       ║
║                                                                           ║
║              Your AI Shadow on Ara's Cloud                                ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
""")


def step(num, total, message):
    """Print a step indicator."""
    print(f"\n[{num}/{total}] {message}")
    print("─" * 50)


def deploy_demo():
    """Demo deployment flow."""
    print_banner()
    print("🎮 DEMO MODE - Simulating Ara deployment\n")

    total_steps = 6

    # Step 1: Connect to Ara
    step(1, total_steps, "Connecting to Ara Platform...")
    time.sleep(1)
    client = get_ara_client(mock=True)
    print("✅ Connected to Ara (api.ara.so)")
    print("   Account: hackathon@jhu.edu")
    print("   Plan: Hackathon Pro")

    # Step 2: Create Agent
    step(2, total_steps, "Creating Distill Agent...")
    time.sleep(1)
    agent = client.create_agent("distill-jhu", {
        "type": "productivity",
        "features": ["screen_tracking", "document_extension", "style_matching"]
    })
    print("✅ Agent created: distill-jhu")
    print("   ID: agent_distill-jhu_x8k2m")
    print("   Runtime: Python 3.11")

    # Step 3: Create Sandbox
    step(3, total_steps, "Provisioning Sandbox Environment...")
    time.sleep(1.5)
    sandbox = client.sandbox.create("distill-sandbox")
    print("✅ Sandbox ready")
    print("   Environment: Isolated container")
    print("   Storage: 10GB persistent")
    print("   Memory: 4GB RAM")

    # Step 4: Deploy Code
    step(4, total_steps, "Deploying Distill Code...")

    files = [
        "agents/distill.py",
        "agents/screen_tracker.py",
        "integrations/ara_platform.py",
        "integrations/telegram_bot.py"
    ]

    for f in files:
        time.sleep(0.5)
        print(f"   📦 Uploading {f}...")

    print("✅ Code deployed (4 files, 12.3 KB)")

    # Step 5: Configure Channels
    step(5, total_steps, "Configuring Message Channels...")
    time.sleep(1)
    print("✅ Channels configured:")
    print("   📱 Telegram: @DistillBot (connected)")
    print("   💬 WhatsApp: +1-XXX-XXX-XXXX (pending)")
    print("   🎮 Discord: Distill#1234 (connected)")

    # Step 6: Schedule Overnight Run
    step(6, total_steps, "Scheduling Overnight Execution...")
    time.sleep(1)
    agent.schedule_overnight("run_extension", time="03:00")
    print("✅ Schedule configured:")
    print("   🌙 Overnight run: 3:00 AM EST")
    print("   ☀️ Morning report: 7:00 AM EST")
    print("   🔄 Timezone: America/New_York")

    # Summary
    print("\n")
    print("═" * 60)
    print("                    DEPLOYMENT COMPLETE")
    print("═" * 60)
    print("""
🚀 Distill is now running on Ara!

📊 Dashboard:  https://app.ara.so/agents/distill-jhu
📱 Telegram:   @DistillBot
📚 Logs:       https://app.ara.so/logs/distill-jhu

🌙 Tonight at 3:00 AM:
   1. Distill will analyze your screen captures
   2. Identify incomplete work
   3. Extend documents in your style
   4. Send morning report at 7:00 AM

💡 Commands:
   /status  - Check agent status
   /pause   - Pause overnight runs
   /report  - Get latest report
""")

    # Simulate a test message
    print("\n📱 Sending test message...")
    time.sleep(1)

    test_message = """
☀️ *Distill Activated!*

I'm now running 24/7 on Ara's cloud.

Here's what I'll do:
• Watch your screen during the day
• Analyze your work patterns
• Extend your documents overnight
• Send you a morning briefing

Reply /help for commands.

_Powered by Ara_ 🌙
"""

    print("\n┌─────────────────────────────────────┐")
    print("│ 📱 Telegram Preview                 │")
    print("├─────────────────────────────────────┤")
    for line in test_message.strip().split('\n'):
        print(f"│ {line:<35} │")
    print("└─────────────────────────────────────┘")

    print("\n✅ Test message sent to Telegram!")
    print("\n🎉 Deployment demo complete!")


def deploy_real():
    """Real deployment (requires Ara API key)."""
    print_banner()

    if not AraConfig.API_KEY:
        print("❌ ARA_API_KEY not found in environment")
        print("\nTo deploy to Ara:")
        print("1. Get your API key from https://app.ara.so/settings/api")
        print("2. Add to .env: ARA_API_KEY=your_key_here")
        print("3. Run this script again")
        print("\nOr run with --demo flag to see the deployment flow")
        return

    # Real deployment would go here
    client = get_ara_client(mock=False)

    if not client.health_check():
        print("❌ Cannot connect to Ara API")
        return

    print("✅ Connected to Ara")
    # ... rest of real deployment


def main():
    parser = argparse.ArgumentParser(description="Deploy Distill to Ara")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode")
    parser.add_argument("--schedule", type=str, default="03:00", help="Overnight run time")

    args = parser.parse_args()

    if args.demo or not AraConfig.API_KEY:
        deploy_demo()
    else:
        deploy_real()


if __name__ == "__main__":
    main()
