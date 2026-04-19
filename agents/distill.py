"""
Distill Agent
=============

An AI that watches your work, learns your patterns, and CONTINUES your work overnight.

Components:
1. DocumentAnalyzer - Understands structure, style, intent
2. StyleExtractor - Captures your writing voice
3. WorkExtender - Continues incomplete work
4. ResearchAgent - Gathers supporting information
5. ReportGenerator - Summarizes what was done
"""

import os
import json
import difflib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class DocumentAnalyzer:
    """Analyzes documents to understand structure, style, and intent."""

    def analyze(self, content: str, context: str = "") -> Dict:
        """Analyze a document and extract key information."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": f"""Analyze this document and provide a detailed assessment.

DOCUMENT:
{content}

ADDITIONAL CONTEXT:
{context}

Provide analysis in JSON format:
{{
    "document_type": "report/email/code/notes/essay/other",
    "completion_percentage": 0-100,
    "structure": {{
        "existing_sections": ["list of sections"],
        "missing_sections": ["what seems to be missing"],
        "logical_next_sections": ["what should come next"]
    }},
    "style": {{
        "tone": "formal/casual/technical/friendly",
        "voice": "first_person/third_person/passive",
        "avg_sentence_length": "short/medium/long",
        "vocabulary_level": "simple/intermediate/advanced",
        "notable_patterns": ["any stylistic patterns"]
    }},
    "intent": {{
        "apparent_goal": "what the author is trying to achieve",
        "target_audience": "who this is for",
        "key_arguments": ["main points being made"],
        "unfinished_thoughts": ["ideas that seem incomplete"]
    }},
    "extension_opportunities": [
        {{
            "type": "section/paragraph/research/data",
            "description": "what could be added",
            "priority": "high/medium/low"
        }}
    ]
}}"""
            }]
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"raw_analysis": response.content[0].text}


class StyleExtractor:
    """Extracts and learns writing style from samples."""

    def extract_style(self, samples: List[str]) -> Dict:
        """Extract style patterns from writing samples."""

        combined_samples = "\n\n---\n\n".join(samples[:5])  # Max 5 samples

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": f"""Analyze these writing samples and extract the author's unique style.

SAMPLES:
{combined_samples}

Create a style guide in JSON:
{{
    "voice_characteristics": {{
        "perspective": "first/second/third person",
        "formality": 1-10,
        "confidence_level": "tentative/balanced/assertive",
        "emotional_tone": "neutral/warm/enthusiastic/serious"
    }},
    "sentence_patterns": {{
        "avg_length": "short/medium/long",
        "complexity": "simple/compound/complex",
        "opener_styles": ["how sentences typically start"],
        "transition_words": ["commonly used transitions"]
    }},
    "vocabulary": {{
        "technical_level": 1-10,
        "jargon_examples": ["domain-specific terms used"],
        "favorite_phrases": ["recurring expressions"],
        "avoided_words": ["words they seem to avoid"]
    }},
    "structural_habits": {{
        "paragraph_length": "short/medium/long",
        "uses_headers": true/false,
        "uses_bullets": true/false,
        "uses_examples": true/false
    }},
    "replication_notes": "Brief guide for writing like this author"
}}"""
            }]
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"raw_style": response.content[0].text}


class WorkExtender:
    """Extends incomplete work based on analysis and style."""

    def __init__(self):
        self.analyzer = DocumentAnalyzer()
        self.style_extractor = StyleExtractor()

    def extend_document(
        self,
        original_content: str,
        context: str = "",
        style_samples: List[str] = None,
        extension_type: str = "auto"
    ) -> Tuple[str, Dict]:
        """
        Extend a document with new content.

        Returns:
            Tuple of (extended_document, metadata)
        """

        # Analyze the document
        analysis = self.analyzer.analyze(original_content, context)

        # Extract style if samples provided
        style_guide = None
        if style_samples:
            style_guide = self.style_extractor.extract_style(style_samples)

        # Build the extension prompt
        style_instructions = ""
        if style_guide:
            style_instructions = f"""
STYLE GUIDE (match this writing style):
{json.dumps(style_guide, indent=2)}
"""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": f"""You are continuing someone else's work. Your job is to extend this document seamlessly, matching their style perfectly.

ORIGINAL DOCUMENT:
{original_content}

DOCUMENT ANALYSIS:
{json.dumps(analysis, indent=2)}

CONTEXT:
{context}
{style_instructions}

TASK:
1. Continue this document naturally from where it left off
2. Add logical next sections based on the analysis
3. Match the original author's style EXACTLY
4. Do NOT repeat existing content
5. Mark new content clearly with [DISTILL START] and [DISTILL END] tags

Write the EXTENDED CONTENT ONLY (not the original). Start where the original ends."""
            }]
        )

        new_content = response.content[0].text

        # Combine original + new content
        extended_document = original_content.strip() + "\n\n" + new_content

        # Create metadata
        metadata = {
            "original_length": len(original_content),
            "new_length": len(new_content),
            "total_length": len(extended_document),
            "analysis": analysis,
            "style_guide": style_guide,
            "timestamp": datetime.now().isoformat(),
            "sections_added": self._count_sections(new_content)
        }

        return extended_document, metadata

    def _count_sections(self, content: str) -> int:
        """Count number of sections/headers added."""
        import re
        headers = re.findall(r'^#+\s+.+$', content, re.MULTILINE)
        return len(headers)


class ResearchAgent:
    """Conducts research to support document extension."""

    def research_topic(self, topic: str, num_points: int = 5) -> Dict:
        """Research a topic and compile findings."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": f"""Research this topic and provide comprehensive findings.

TOPIC: {topic}

Provide {num_points} key findings in JSON:
{{
    "topic": "{topic}",
    "key_findings": [
        {{
            "point": "Main finding",
            "details": "Supporting information",
            "relevance": "Why this matters"
        }}
    ],
    "suggested_citations": ["Recommended sources to cite"],
    "data_points": ["Any statistics or data"],
    "counter_arguments": ["Potential objections to consider"],
    "synthesis": "Overall summary of research"
}}"""
            }]
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"raw_research": response.content[0].text}


class DistillAgent:
    """
    Main Distill Agent - orchestrates the watch, learn, extend cycle.
    """

    def __init__(self):
        self.extender = WorkExtender()
        self.researcher = ResearchAgent()

    def process_work_session(
        self,
        documents: List[Dict],  # {"content": str, "filename": str, "context": str}
        style_samples: List[str] = None,
        research_topics: List[str] = None
    ) -> Dict:
        """
        Process a full work session overnight.

        Args:
            documents: List of documents to potentially extend
            style_samples: Examples of the user's writing
            research_topics: Topics to research

        Returns:
            Complete session report
        """

        results = {
            "timestamp": datetime.now().isoformat(),
            "documents_processed": [],
            "research_completed": [],
            "summary": ""
        }

        # Process each document
        for doc in documents:
            try:
                extended, metadata = self.extender.extend_document(
                    original_content=doc["content"],
                    context=doc.get("context", ""),
                    style_samples=style_samples
                )

                results["documents_processed"].append({
                    "filename": doc.get("filename", "untitled"),
                    "original_length": metadata["original_length"],
                    "new_content_length": metadata["new_length"],
                    "sections_added": metadata["sections_added"],
                    "extended_content": extended,
                    "diff": self._create_diff(doc["content"], extended)
                })
            except Exception as e:
                results["documents_processed"].append({
                    "filename": doc.get("filename", "untitled"),
                    "error": str(e)
                })

        # Conduct research
        if research_topics:
            for topic in research_topics:
                try:
                    research = self.researcher.research_topic(topic)
                    results["research_completed"].append({
                        "topic": topic,
                        "findings": research
                    })
                except Exception as e:
                    results["research_completed"].append({
                        "topic": topic,
                        "error": str(e)
                    })

        # Generate summary
        results["summary"] = self._generate_summary(results)

        return results

    def _create_diff(self, original: str, extended: str) -> str:
        """Create a readable diff between original and extended."""
        original_lines = original.splitlines(keepends=True)
        extended_lines = extended.splitlines(keepends=True)

        diff = difflib.unified_diff(
            original_lines,
            extended_lines,
            fromfile='original',
            tofile='extended',
            lineterm=''
        )

        return ''.join(diff)

    def _generate_summary(self, results: Dict) -> str:
        """Generate a human-readable summary of work done."""

        docs_count = len([d for d in results["documents_processed"] if "error" not in d])
        research_count = len([r for r in results["research_completed"] if "error" not in r])

        total_new_content = sum(
            d.get("new_content_length", 0)
            for d in results["documents_processed"]
            if "error" not in d
        )

        total_sections = sum(
            d.get("sections_added", 0)
            for d in results["documents_processed"]
            if "error" not in d
        )

        summary = f"""
🌙 DISTILL OVERNIGHT REPORT
{'='*40}

📄 Documents Extended: {docs_count}
   → {total_new_content:,} characters added
   → {total_sections} new sections

🔍 Research Completed: {research_count} topics

📋 Details:
"""

        for doc in results["documents_processed"]:
            if "error" not in doc:
                summary += f"\n• {doc['filename']}"
                summary += f"\n  Added {doc['new_content_length']:,} chars, {doc['sections_added']} sections"

        if results["research_completed"]:
            summary += "\n\n🔬 Research Topics:"
            for r in results["research_completed"]:
                if "error" not in r:
                    summary += f"\n• {r['topic']}"

        summary += f"\n\n{'='*40}"
        summary += "\nReview your extended documents and approve changes."

        return summary

    def generate_morning_report(self, results: Dict) -> str:
        """Generate the morning Telegram/WhatsApp message."""

        docs_count = len([d for d in results["documents_processed"] if "error" not in d])

        if docs_count == 0:
            return "🌙 Distill ran overnight but found no documents to extend."

        total_chars = sum(
            d.get("new_content_length", 0)
            for d in results["documents_processed"]
            if "error" not in d
        )

        total_sections = sum(
            d.get("sections_added", 0)
            for d in results["documents_processed"]
            if "error" not in d
        )

        message = f"""☀️ Good morning!

🌙 **Distill worked while you slept**

📄 **{docs_count} document{'s' if docs_count > 1 else ''} extended**
→ Added {total_chars:,} characters
→ {total_sections} new section{'s' if total_sections != 1 else ''}

"""

        for doc in results["documents_processed"][:3]:  # Show top 3
            if "error" not in doc:
                message += f"📝 **{doc['filename']}**\n"
                message += f"   +{doc['new_content_length']:,} chars, {doc['sections_added']} sections\n\n"

        if len(results["research_completed"]) > 0:
            message += f"🔍 **Research compiled**: {len(results['research_completed'])} topics\n\n"

        message += "✅ Ready for your review!"

        return message


# Demo / Testing
if __name__ == "__main__":
    # Example: Extend an incomplete document
    incomplete_doc = """
# Ara Hackathon Project: Night Shift

## Introduction

Night Shift is an AI agent that works while you sleep. The core idea is simple:
instead of waking up to chaos, you wake up to clarity.

## The Problem

Every morning, knowledge workers face the same challenge:
- 50+ unread emails
- Back-to-back meetings
- Scattered files and notes

This leads to spending the first 2 hours just figuring out what to do.

## Our Solution

Night Shift runs overnight on Ara's cloud infrastructure. It:
"""

    context = """
    This is a hackathon project README for the Ara x JHU hackathon.
    The project is about a 24/7 AI productivity agent.
    Target audience: hackathon judges and potential users.
    The document should explain the technical architecture and value proposition.
    """

    # Run Distill
    agent = DistillAgent()

    print("🌙 Distill Agent Starting...")
    print("=" * 50)

    results = agent.process_work_session(
        documents=[{
            "content": incomplete_doc,
            "filename": "README.md",
            "context": context
        }],
        research_topics=["AI agent cloud infrastructure 2026"]
    )

    # Show summary
    print(results["summary"])

    # Show morning message
    print("\n" + "=" * 50)
    print("TELEGRAM MESSAGE:")
    print("=" * 50)
    print(agent.generate_morning_report(results))

    # Show the extended content
    print("\n" + "=" * 50)
    print("EXTENDED DOCUMENT:")
    print("=" * 50)
    if results["documents_processed"]:
        print(results["documents_processed"][0].get("extended_content", "No content"))
