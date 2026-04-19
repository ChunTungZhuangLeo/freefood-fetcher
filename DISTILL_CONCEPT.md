# Distill - Complete System Design

## One-Liner
**"Your AI shadow that watches you work all day, then continues your work while you sleep."**

---

## The Full Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DISTILL PIPELINE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   DAYTIME                                                                    │
│   ═══════                                                                    │
│   ┌─────────────┐                                                            │
│   │   CAPTURE   │  Screenshots every 5 min                                   │
│   │   ───────   │  Active window tracking                                    │
│   │   📸 👁️     │  App usage monitoring                                      │
│   └──────┬──────┘                                                            │
│          │                                                                   │
│          ▼                                                                   │
│   ┌─────────────┐                                                            │
│   │   ANALYZE   │  Claude Vision on screenshots                              │
│   │   ───────   │  "What is user working on?"                                │
│   │   🧠 🔍     │  "What's incomplete?"                                      │
│   └──────┬──────┘                                                            │
│          │                                                                   │
│   EVENING│                                                                   │
│   ═══════│                                                                   │
│          ▼                                                                   │
│   ┌─────────────┐                                                            │
│   │   DISTILL   │  Summarize the day                                         │
│   │   ───────   │  Extract style from documents                              │
│   │   📊 ✨     │  Identify incomplete work                                  │
│   └──────┬──────┘                                                            │
│          │                                                                   │
│   OVERNIGHT                                                                  │
│   ═════════                                                                  │
│          ▼                                                                   │
│   ┌─────────────┐                                                            │
│   │   EXTEND    │  Continue documents                                        │
│   │   ───────   │  Write in YOUR style                                       │
│   │   ✍️ 📄     │  Research topics you explored                              │
│   └──────┬──────┘                                                            │
│          │                                                                   │
│   MORNING│                                                                   │
│   ═══════│                                                                   │
│          ▼                                                                   │
│   ┌─────────────┐                                                            │
│   │   REPORT    │  "I extended 3 documents"                                  │
│   │   ───────   │  Diff view of changes                                      │
│   │   📱 ☀️     │  Delivered via Telegram                                    │
│   └─────────────┘                                                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Technical Components

### 1. Screen Tracker (`agents/screen_tracker.py`)

```python
# Captures screenshot every N seconds
class ScreenCapture:
    def capture(self) -> str:
        # macOS: screencapture -x screenshot.png
        # Returns filepath

    def get_active_window(self) -> Dict:
        # AppleScript to get frontmost app + window title
        return {"app": "VS Code", "window": "distill.py"}
```

### 2. Vision Analyzer (Claude Vision)

```python
class VisionAnalyzer:
    def analyze_screenshot(self, image_path: str) -> Dict:
        # Send image to Claude Vision
        # Returns: {
        #   "application": "VS Code",
        #   "task": "Writing Python code",
        #   "content_summary": "Implementing screen capture",
        #   "incomplete_work": "Function missing return statement"
        # }
```

### 3. Work Session Manager

```python
class WorkSession:
    def capture_now(self):
        # Take screenshot + analyze

    def start_tracking(self, interval=300):
        # Capture every 5 minutes

    def get_context_for_distill(self) -> Dict:
        # Summarize full day for overnight work
```

### 4. Work Extender (From original Distill)

```python
class WorkExtender:
    def extend_document(self, content, style_samples) -> str:
        # Continue the document matching user's style
```

---

## Data Flow Example

### 9:00 AM - Start Tracking
```
$ python run_distill.py track

📸 Captured: VS Code - editing main.py
📸 Captured: Chrome - researching APIs
📸 Captured: VS Code - editing main.py
...
```

### 6:00 PM - End Day
```
$ Ctrl+C

🧠 Analyzing 78 screenshots...

📊 SESSION SUMMARY
==================
Duration: 8h 32m
Main apps: VS Code (4h), Chrome (2h), Slack (1h)

⚠️ INCOMPLETE WORK DETECTED:
1. README.md - Missing architecture section
2. api_client.py - OAuth flow incomplete
3. Pitch deck - Only 4/8 slides done
```

### 3:00 AM - Overnight Extension
```
🌙 Running overnight extensions...

✍️ Extending README.md...
   → Added 847 words
   → Matched technical writing style

✍️ Extending api_client.py...
   → Added docstrings
   → Completed OAuth flow
```

### 7:00 AM - Morning Report
```
📱 Telegram Message:

☀️ Good morning!

🌙 Distill worked while you slept

📄 3 documents extended:
   • README.md (+847 words)
   • api_client.py (+124 lines)
   • pitch.md (outline complete)

✅ Ready for your review!
```

---

## Hackathon Demo Files

### Interactive Demos
```bash
# Full screen tracking demo (BEST)
open demo/distill-full-demo.html

# Document extension demo
open demo/distill-live.html

# Animated demo (for video)
open demo/distill-demo.html
```

### Pitch Deck
```bash
open demo/distill-pitch.html
```

### CLI Demo
```bash
# Full simulated demo
python run_distill.py demo

# Real tracking (requires screen permission)
python run_distill.py track -i 60
```

---

## Why This Wins

### For Judges
1. **Technical depth**: Computer vision + NLP + multi-stage pipeline
2. **Practical value**: Everyone has unfinished work
3. **Ara alignment**: Shows 24/7 agent value perfectly

### For Ara Founders
1. **Demonstrates computer use**: Screen watching is the future
2. **24/7 infrastructure value**: Can't do this without cloud runtime
3. **Platform potential**: Could be flagship Ara capability

### For Going Viral
1. **Screenshots are shareable**: "What my AI did at 3am"
2. **Relatable problem**: Unfinished work is universal
3. **Magical outcome**: Wake up to completed work

---

## The Pitch (60 seconds)

> "What if your computer remembered everything you worked on today...
> and finished it while you slept?"
>
> "Meet Distill. All day, it watches your screen. Silently learning.
> What apps you use. What documents you edit. What you leave unfinished."
>
> "At 3 AM, while you're asleep, Distill gets to work.
> It continues your README. Adds docstrings to your code.
> Researches topics you were exploring."
>
> "You wake up to a message: 'I extended 3 documents.
> Added 1,200 words. Matched your style. Ready for review.'"
>
> "Distill doesn't replace you. It extends you. 24/7.
> Powered by Ara's always-on cloud infrastructure."
>
> "Your AI shadow. Always watching. Always working."

---

## Quick Commands

```bash
# View the full demo
open demo/distill-full-demo.html

# Run CLI demo
python run_distill.py demo

# Start real tracking
python run_distill.py track

# View pitch slides
open demo/distill-pitch.html
```
