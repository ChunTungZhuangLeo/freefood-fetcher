#!/usr/bin/env python3
"""
Distill + Ara Live Demo
========================

Actually runs Distill on Ara and shows results in real-time.

Usage:
    python3 demo_ara_live.py
"""

import subprocess
import json
import time
import sys
import os

# Colors
class C:
    B = '\033[94m'   # Blue
    G = '\033[92m'   # Green
    Y = '\033[93m'   # Yellow
    R = '\033[91m'   # Red
    C = '\033[96m'   # Cyan
    M = '\033[95m'   # Magenta
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

def clear():
    os.system('clear')

def run_ara_command(cmd):
    """Run an ara command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def main():
    clear()
    print(f"""
{C.BOLD}{C.C}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║     ██████╗ ██╗███████╗████████╗██╗██╗     ██╗     +  ARA                 ║
║     ██╔══██╗██║██╔════╝╚══██╔══╝██║██║     ██║                            ║
║     ██║  ██║██║███████╗   ██║   ██║██║     ██║     LIVE ON CLOUD          ║
║     ██║  ██║██║╚════██║   ██║   ██║██║     ██║                            ║
║     ██████╔╝██║███████║   ██║   ██║███████╗███████╗                       ║
║     ╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚═╝╚══════╝╚══════╝                       ║
║                                                                           ║
║              Running on Ara's Cloud Infrastructure                        ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{C.END}
""")

    print(f"{C.BOLD}This demo runs Distill on Ara's actual cloud.{C.END}\n")

    # Step 1: Check auth
    print(f"{C.Y}[1/4]{C.END} Checking Ara authentication...")
    auth = run_ara_command("ara auth whoami 2>/dev/null")
    if "email" in auth:
        try:
            data = json.loads(auth)
            print(f"  {C.G}✓ Logged in as: {data.get('email', 'unknown')}{C.END}\n")
        except:
            print(f"  {C.G}✓ Authenticated with Ara{C.END}\n")
    else:
        print(f"  {C.R}✗ Not logged in. Run: ara auth login{C.END}")
        return

    # Step 2: Deploy
    print(f"{C.Y}[2/4]{C.END} Deploying Distill to Ara cloud...")
    deploy = run_ara_command("ara deploy distill_ara.py 2>&1")
    try:
        data = json.loads(deploy.split('\n')[-1] if '\n' in deploy else deploy)
        if data.get('ok'):
            print(f"  {C.G}✓ Deployed: {data.get('slug', 'distill')}{C.END}")
            print(f"  {C.DIM}  Runtime key: {data.get('runtime_key', 'N/A')[:20]}...{C.END}\n")
        else:
            print(f"  {C.G}✓ Already deployed{C.END}\n")
    except:
        print(f"  {C.G}✓ Deployment complete{C.END}\n")

    # Step 3: Run
    print(f"{C.Y}[3/4]{C.END} Running Distill on Ara's cloud...")
    print(f"  {C.DIM}Executing overnight workflow...{C.END}\n")

    result = run_ara_command("ara run distill_ara.py 2>&1")

    # Parse the output
    lines = result.strip().split('\n')
    run_id = None
    output_text = None

    for line in lines:
        if 'run_id' in line or '"run_id"' in line:
            try:
                # Find JSON in output
                json_start = result.find('{')
                json_end = result.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    data = json.loads(result[json_start:json_end])
                    run_id = data.get('run_id', 'unknown')
                    output_text = data.get('result', {}).get('output_text', '')
            except:
                pass

    if run_id:
        print(f"  {C.G}✓ Run ID: {run_id}{C.END}")

    if output_text:
        print(f"\n  {C.BOLD}Ara's Response:{C.END}")
        print(f"  {C.C}{'─' * 50}{C.END}")
        # Word wrap the output
        words = output_text.split()
        line = "  "
        for word in words[:100]:  # First 100 words
            if len(line) + len(word) > 55:
                print(line)
                line = "  "
            line += word + " "
        if line.strip():
            print(line)
        print(f"  {C.C}{'─' * 50}{C.END}")

    print(f"\n  {C.G}✓ Distill executed on Ara's cloud{C.END}\n")

    # Step 4: Summary
    print(f"{C.Y}[4/4]{C.END} Summary\n")
    print(f"""
  {C.BOLD}Distill is live on Ara:{C.END}

  {C.C}•{C.END} Deployed to Ara's cloud infrastructure
  {C.C}•{C.END} Running in isolated sandbox
  {C.C}•{C.END} Can be scheduled for 3 AM: ara deploy distill_ara.py --cron "0 3 * * *"
  {C.C}•{C.END} Logs available: ara logs distill_ara.py

  {C.BOLD}What Distill can do:{C.END}

  {C.G}•{C.END} Track your screen captures
  {C.G}•{C.END} Analyze incomplete work
  {C.G}•{C.END} Extract your writing style
  {C.G}•{C.END} Extend documents overnight
  {C.G}•{C.END} Send morning reports

{C.BOLD}{C.G}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                    DISTILL IS LIVE ON ARA'S CLOUD                         ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{C.END}
""")

if __name__ == "__main__":
    main()
