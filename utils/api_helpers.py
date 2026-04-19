"""
Utility functions for API integrations
"""

import os
import json
import requests
from datetime import datetime
from typing import Optional, Dict, List


def load_env_var(key: str, required: bool = True) -> Optional[str]:
    """Load an environment variable."""
    value = os.getenv(key)
    if required and not value:
        raise ValueError(f"Missing required environment variable: {key}")
    return value


def fetch_url(url: str, headers: Dict = None) -> Dict:
    """Fetch data from a URL."""
    try:
        response = requests.get(url, headers=headers or {}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}


def save_to_file(data: any, filename: str, format: str = "json") -> str:
    """Save data to a file."""
    filepath = f"data/{filename}"
    os.makedirs("data", exist_ok=True)

    if format == "json":
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
    else:
        with open(filepath, "w") as f:
            f.write(str(data))

    return filepath


def read_file(filepath: str) -> str:
    """Read content from a file."""
    with open(filepath, "r") as f:
        return f.read()


def format_timestamp(dt: datetime = None) -> str:
    """Format a datetime for display."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def chunk_text(text: str, max_length: int = 4000) -> List[str]:
    """Split text into chunks for processing."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def extract_json_from_text(text: str) -> Optional[Dict]:
    """Try to extract JSON from text that might contain other content."""
    import re

    # Try to find JSON object
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, text)

    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue

    return None


# File type handlers
def read_pdf(filepath: str) -> str:
    """Extract text from PDF (requires pypdf)."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except ImportError:
        return "Error: pypdf not installed. Run: pip install pypdf"


def read_docx(filepath: str) -> str:
    """Extract text from Word document (requires python-docx)."""
    try:
        from docx import Document
        doc = Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    except ImportError:
        return "Error: python-docx not installed. Run: pip install python-docx"
