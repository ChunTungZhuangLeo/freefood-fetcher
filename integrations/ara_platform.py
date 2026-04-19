"""
Ara Platform Integration
========================

Integration with Ara's cloud runtime platform.
https://ara.so | https://docs.ara.so

This module provides:
1. AraClient - Connect to Ara's cloud runtime
2. AraSandbox - Run code in isolated environment
3. AraChannels - Multi-channel messaging (WhatsApp, Telegram, Discord)
4. AraSkills - Register as a ClawHub skill

Usage:
    from integrations.ara_platform import AraClient, AraSandbox

    # Initialize client
    client = AraClient(api_key="your_ara_api_key")

    # Create a sandbox for your agent
    sandbox = client.create_sandbox(name="distill-agent")

    # Run your agent in the sandbox
    sandbox.run(agent_function)

    # Send message via connected channels
    client.channels.send("telegram", "Hello from Distill!")

NOTE: Fill in actual API endpoints once you have access to Ara's SDK.
The structure below is based on Ara's documented capabilities.
"""

import os
import json
import requests
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class AraConfig:
    """Ara platform configuration."""

    # API Endpoints (update with actual Ara endpoints)
    BASE_URL = os.getenv("ARA_API_URL", "https://api.ara.so/v1")
    SANDBOX_URL = os.getenv("ARA_SANDBOX_URL", "https://sandbox.ara.so")

    # Auth
    API_KEY = os.getenv("ARA_API_KEY", "")

    # Channels
    TELEGRAM_ENABLED = os.getenv("ARA_TELEGRAM_ENABLED", "true") == "true"
    WHATSAPP_ENABLED = os.getenv("ARA_WHATSAPP_ENABLED", "false") == "true"
    DISCORD_ENABLED = os.getenv("ARA_DISCORD_ENABLED", "false") == "true"


class AraClient:
    """
    Main client for interacting with Ara's platform.

    Ara provides:
    - 24/7 cloud runtimes for AI agents
    - Isolated sandbox environments
    - Multi-channel messaging
    - Persistent state across sessions
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or AraConfig.API_KEY
        self.base_url = AraConfig.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

        # Sub-clients
        self.sandbox = AraSandbox(self)
        self.channels = AraChannels(self)
        self.skills = AraSkills(self)

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make API request to Ara."""
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ara API error: {e}")
            return {"error": str(e)}

    def health_check(self) -> bool:
        """Check connection to Ara platform."""
        result = self._request("GET", "/health")
        return result.get("status") == "ok"

    def get_account(self) -> Dict:
        """Get current account info."""
        return self._request("GET", "/account")

    def create_agent(self, name: str, config: Dict = None) -> "AraAgent":
        """Create a new agent on Ara's platform."""
        result = self._request("POST", "/agents", json={
            "name": name,
            "config": config or {}
        })
        return AraAgent(self, result.get("agent_id"), name)


class AraSandbox:
    """
    Ara's isolated sandbox environment for running agents.

    Features:
    - Isolated runtime per agent
    - Persistent file storage
    - Secure credential handling
    - 24/7 execution capability
    """

    def __init__(self, client: AraClient):
        self.client = client

    def create(self, name: str, runtime: str = "python3.11") -> Dict:
        """Create a new sandbox environment."""
        return self.client._request("POST", "/sandbox", json={
            "name": name,
            "runtime": runtime,
            "persistent": True
        })

    def execute(self, sandbox_id: str, code: str) -> Dict:
        """Execute code in sandbox."""
        return self.client._request("POST", f"/sandbox/{sandbox_id}/execute", json={
            "code": code
        })

    def upload_file(self, sandbox_id: str, filepath: str, content: bytes) -> Dict:
        """Upload file to sandbox."""
        return self.client._request("POST", f"/sandbox/{sandbox_id}/files", json={
            "path": filepath,
            "content": content.decode("utf-8") if isinstance(content, bytes) else content
        })

    def schedule(self, sandbox_id: str, cron: str, function: str) -> Dict:
        """Schedule a function to run on a cron schedule."""
        return self.client._request("POST", f"/sandbox/{sandbox_id}/schedule", json={
            "cron": cron,
            "function": function
        })


class AraChannels:
    """
    Multi-channel messaging through Ara.

    Supported channels:
    - Telegram
    - WhatsApp
    - Discord
    - iMessage (via Ara bridge)
    - Signal
    """

    def __init__(self, client: AraClient):
        self.client = client

    def list_connected(self) -> List[Dict]:
        """List all connected messaging channels."""
        return self.client._request("GET", "/channels")

    def send(self, channel: str, message: str, recipient: str = None) -> Dict:
        """Send message through a channel."""
        return self.client._request("POST", f"/channels/{channel}/send", json={
            "message": message,
            "recipient": recipient
        })

    def send_telegram(self, message: str, chat_id: str = None) -> Dict:
        """Send message via Telegram."""
        return self.send("telegram", message, chat_id)

    def send_whatsapp(self, message: str, phone: str = None) -> Dict:
        """Send message via WhatsApp."""
        return self.send("whatsapp", message, phone)

    def send_discord(self, message: str, channel_id: str = None) -> Dict:
        """Send message via Discord."""
        return self.send("discord", message, channel_id)

    def broadcast(self, message: str, channels: List[str] = None) -> Dict:
        """Send message to multiple channels."""
        return self.client._request("POST", "/channels/broadcast", json={
            "message": message,
            "channels": channels or ["telegram"]
        })


class AraSkills:
    """
    Register agents as ClawHub skills.

    Skills can be:
    - Published to ClawHub marketplace
    - Installed by other Ara users
    - Triggered via messaging commands
    """

    def __init__(self, client: AraClient):
        self.client = client

    def register(self, skill_config: Dict) -> Dict:
        """Register an agent as a ClawHub skill."""
        return self.client._request("POST", "/skills/register", json=skill_config)

    def publish(self, skill_id: str) -> Dict:
        """Publish skill to ClawHub."""
        return self.client._request("POST", f"/skills/{skill_id}/publish")

    def create_skill_manifest(
        self,
        name: str,
        description: str,
        commands: List[Dict],
        author: str = "hackathon"
    ) -> Dict:
        """Create a SKILL.md manifest for ClawHub."""
        return {
            "name": name,
            "description": description,
            "version": "1.0.0",
            "author": author,
            "commands": commands,
            "runtime": "python",
            "ara_compatible": True
        }


class AraAgent:
    """
    A deployed agent on Ara's platform.

    Lifecycle:
    1. Create agent with config
    2. Deploy to sandbox
    3. Connect channels
    4. Run 24/7
    """

    def __init__(self, client: AraClient, agent_id: str, name: str):
        self.client = client
        self.agent_id = agent_id
        self.name = name

    def deploy(self, code: str) -> Dict:
        """Deploy agent code to Ara."""
        return self.client._request("POST", f"/agents/{self.agent_id}/deploy", json={
            "code": code
        })

    def start(self) -> Dict:
        """Start the agent."""
        return self.client._request("POST", f"/agents/{self.agent_id}/start")

    def stop(self) -> Dict:
        """Stop the agent."""
        return self.client._request("POST", f"/agents/{self.agent_id}/stop")

    def status(self) -> Dict:
        """Get agent status."""
        return self.client._request("GET", f"/agents/{self.agent_id}/status")

    def logs(self, lines: int = 100) -> List[str]:
        """Get agent logs."""
        result = self.client._request("GET", f"/agents/{self.agent_id}/logs", params={
            "lines": lines
        })
        return result.get("logs", [])

    def schedule_overnight(self, function: str, time: str = "03:00") -> Dict:
        """Schedule agent to run overnight at specified time."""
        return self.client._request("POST", f"/agents/{self.agent_id}/schedule", json={
            "time": time,
            "timezone": "America/New_York",
            "function": function
        })


# =============================================================================
# MOCK MODE - For demo without actual Ara API access
# =============================================================================

class MockAraClient:
    """Mock Ara client for demo purposes."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.sandbox = MockAraSandbox(self)
        self.channels = MockAraChannels(self)
        print("🔌 Connected to Ara (mock mode)")

    def health_check(self) -> bool:
        return True

    def create_agent(self, name: str, config: Dict = None) -> "MockAraAgent":
        print(f"✅ Created agent: {name}")
        return MockAraAgent(self, f"agent_{name}", name)


class MockAraSandbox:
    def __init__(self, client):
        self.client = client

    def create(self, name: str, runtime: str = "python3.11") -> Dict:
        print(f"📦 Created sandbox: {name} ({runtime})")
        return {"sandbox_id": f"sandbox_{name}", "status": "ready"}

    def execute(self, sandbox_id: str, code: str) -> Dict:
        print(f"⚡ Executing in {sandbox_id}...")
        return {"status": "success", "output": "Code executed"}

    def schedule(self, sandbox_id: str, cron: str, function: str) -> Dict:
        print(f"⏰ Scheduled {function} with cron: {cron}")
        return {"scheduled": True}


class MockAraChannels:
    def __init__(self, client):
        self.client = client

    def send_telegram(self, message: str, chat_id: str = None) -> Dict:
        print(f"📱 [Telegram] {message[:100]}...")
        return {"sent": True, "channel": "telegram"}

    def send_whatsapp(self, message: str, phone: str = None) -> Dict:
        print(f"📱 [WhatsApp] {message[:100]}...")
        return {"sent": True, "channel": "whatsapp"}

    def broadcast(self, message: str, channels: List[str] = None) -> Dict:
        for ch in (channels or ["telegram"]):
            print(f"📢 [{ch}] {message[:50]}...")
        return {"sent": True, "channels": channels}


class MockAraAgent:
    def __init__(self, client, agent_id: str, name: str):
        self.client = client
        self.agent_id = agent_id
        self.name = name

    def deploy(self, code: str) -> Dict:
        print(f"🚀 Deployed {self.name}")
        return {"status": "deployed"}

    def start(self) -> Dict:
        print(f"▶️ Started {self.name}")
        return {"status": "running"}

    def schedule_overnight(self, function: str, time: str = "03:00") -> Dict:
        print(f"🌙 {self.name} scheduled for {time}")
        return {"scheduled": True, "time": time}


# =============================================================================
# Helper to get the right client
# =============================================================================

def get_ara_client(mock: bool = None) -> AraClient:
    """
    Get Ara client (real or mock).

    Uses mock mode if:
    - mock=True is passed
    - ARA_API_KEY is not set
    - ARA_MOCK_MODE=true in env
    """
    if mock is None:
        mock = (
            not AraConfig.API_KEY or
            os.getenv("ARA_MOCK_MODE", "false").lower() == "true"
        )

    if mock:
        return MockAraClient()
    return AraClient()


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════╗
║              ARA PLATFORM INTEGRATION                      ║
╚═══════════════════════════════════════════════════════════╝
""")

    # Get client (will use mock if no API key)
    client = get_ara_client()

    # Health check
    print("1. Health check:", "✅" if client.health_check() else "❌")

    # Create agent
    print("\n2. Creating Distill agent...")
    agent = client.create_agent("distill", {
        "type": "productivity",
        "schedule": "overnight"
    })

    # Create sandbox
    print("\n3. Creating sandbox...")
    sandbox = client.sandbox.create("distill-sandbox")

    # Schedule overnight run
    print("\n4. Scheduling overnight execution...")
    agent.schedule_overnight("run_distill", time="03:00")

    # Send test message
    print("\n5. Testing channel messaging...")
    client.channels.broadcast(
        "🌙 Distill is now running on Ara!\n\nI'll analyze your work and extend it overnight.",
        channels=["telegram"]
    )

    print("\n✅ Integration complete!")
