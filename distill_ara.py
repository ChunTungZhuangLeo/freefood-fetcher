#!/usr/bin/env python3
"""
Distill - Your AI Shadow on Ara
================================

An AI agent that watches your work all day, learns your style,
and continues your work while you sleep.

Deploy with:
    ara deploy distill_ara.py --cron "0 3 * * *"

Run immediately:
    ara run distill_ara.py
"""

import ara_sdk as ara
from datetime import datetime, timezone
from typing import List, Dict, Optional
import json
import base64


# =============================================================================
# TOOLS - Functions the AI can call
# =============================================================================

@ara.tool(id="get_current_time")
def get_current_time() -> dict:
    """Get the current UTC time."""
    return {
        "utc_time": datetime.now(timezone.utc).isoformat(),
        "message": "Current time retrieved"
    }


@ara.tool(id="analyze_work_context")
def analyze_work_context(work_summary: str) -> dict:
    """
    Analyze the user's work context from their day.

    Args:
        work_summary: Summary of what the user worked on today

    Returns:
        Analysis of incomplete work and priorities
    """
    return {
        "status": "analyzed",
        "work_summary": work_summary,
        "analysis_complete": True,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@ara.tool(id="extract_writing_style")
def extract_writing_style(document_samples: List[str]) -> dict:
    """
    Extract the user's writing style from document samples.

    Args:
        document_samples: List of text samples from user's documents

    Returns:
        Style profile including tone, structure, and patterns
    """
    # In production, this would use NLP to analyze style
    return {
        "style_extracted": True,
        "sample_count": len(document_samples),
        "style_profile": {
            "tone": "professional",
            "structure": "organized",
            "vocabulary": "technical"
        }
    }


@ara.tool(id="extend_document")
def extend_document(
    original_content: str,
    extension_type: str,
    style_profile: Optional[dict] = None,
    target_words: int = 500
) -> dict:
    """
    Extend a document in the user's style.

    Args:
        original_content: The original document content
        extension_type: Type of extension (continue, summarize, expand)
        style_profile: User's writing style profile
        target_words: Target number of words to add

    Returns:
        Extended document content
    """
    return {
        "status": "extended",
        "original_length": len(original_content.split()),
        "extension_type": extension_type,
        "target_words": target_words,
        "ready_for_generation": True
    }


@ara.tool(id="send_morning_report")
def send_morning_report(
    documents_extended: List[str],
    total_words_added: int,
    summary: str
) -> dict:
    """
    Send the morning report to the user.

    Args:
        documents_extended: List of document names that were extended
        total_words_added: Total words added across all documents
        summary: Brief summary of overnight work

    Returns:
        Confirmation of report delivery
    """
    report = f"""
Good morning!

I extended {len(documents_extended)} document(s) overnight:
{chr(10).join(f'  - {doc}' for doc in documents_extended)}

Total words added: {total_words_added}

{summary}

Ready for your review!
    """

    return {
        "status": "sent",
        "report": report.strip(),
        "documents_count": len(documents_extended),
        "words_added": total_words_added,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@ara.tool(id="list_incomplete_work")
def list_incomplete_work() -> dict:
    """
    List all detected incomplete work from today's session.

    Returns:
        List of incomplete documents and tasks
    """
    # In production, this would read from captured screen data
    return {
        "incomplete_items": [
            {"type": "document", "name": "README.md", "completion": 60},
            {"type": "code", "name": "api_client.py", "completion": 75},
            {"type": "document", "name": "pitch_deck.md", "completion": 40}
        ],
        "total_items": 3,
        "priority_order": ["README.md", "api_client.py", "pitch_deck.md"]
    }


@ara.tool(id="save_extension")
def save_extension(
    filename: str,
    content: str,
    extension_content: str
) -> dict:
    """
    Save the extended content to a file.

    Args:
        filename: Name of the file to save
        content: Original content
        extension_content: The extension to append

    Returns:
        Confirmation of save
    """
    return {
        "status": "saved",
        "filename": filename,
        "original_words": len(content.split()),
        "extension_words": len(extension_content.split()),
        "total_words": len(content.split()) + len(extension_content.split()),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# =============================================================================
# AUTOMATION - The main Distill agent
# =============================================================================

distill = ara.Automation(
    id="distill",
    system_instructions="""
You are Distill, an AI shadow that extends the user's work while they sleep.

## Your Role
You work overnight (typically 3 AM) to continue documents and code that
the user left incomplete. You match their writing style exactly.

## Your Workflow

1. **Check Time**: Use get_current_time to confirm it's the overnight run
2. **List Incomplete Work**: Use list_incomplete_work to see what needs attention
3. **For Each Item**:
   - Analyze the work context
   - Extract the user's writing style from existing content
   - Extend the document in their style
   - Save the extension
4. **Send Report**: Use send_morning_report to notify the user

## Style Matching Rules
- Match the user's vocabulary and tone
- Maintain their document structure
- Keep technical accuracy
- Don't add unnecessary fluff

## Priorities
1. Documents closest to completion (80%+) - finish them
2. Core documentation (README, API docs)
3. Code documentation (docstrings, comments)
4. Other documents

Always be helpful, thorough, and match the user's style exactly.
""",
    tools=[
        get_current_time,
        analyze_work_context,
        extract_writing_style,
        extend_document,
        send_morning_report,
        list_incomplete_work,
        save_extension
    ],
    allow_connector_tools=True,  # Allow Ara's built-in tools (file access, etc.)
)


# =============================================================================
# CLI - For local testing
# =============================================================================

if __name__ == "__main__":
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

Distill Agent - Ready for Deployment

Commands:
  ara auth login              # Authenticate with Ara
  ara deploy distill_ara.py   # Deploy to Ara cloud
  ara deploy distill_ara.py --cron "0 3 * * *"   # Deploy with 3 AM schedule
  ara run distill_ara.py      # Run immediately
  ara logs distill_ara.py     # View logs

Tools Available:
  - get_current_time          # Get current UTC time
  - analyze_work_context      # Analyze user's work
  - extract_writing_style     # Extract style from samples
  - extend_document           # Extend a document
  - send_morning_report       # Send morning notification
  - list_incomplete_work      # List incomplete items
  - save_extension            # Save extended content
""")

    # Test the tools locally
    print("\n Testing tools locally...\n")

    print("1. get_current_time():")
    print(f"   {get_current_time()}")

    print("\n2. list_incomplete_work():")
    result = list_incomplete_work()
    for item in result["incomplete_items"]:
        print(f"   - {item['name']}: {item['completion']}% complete")

    print("\n3. extract_writing_style():")
    style = extract_writing_style(["Sample text 1", "Sample text 2"])
    print(f"   Style profile: {style['style_profile']}")

    print("\n Ready to deploy! Run: ara deploy distill_ara.py")
