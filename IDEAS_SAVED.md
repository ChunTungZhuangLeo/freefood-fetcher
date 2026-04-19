# Saved Hackathon Ideas

## IDEA 1: Night Shift
**Status:** ✅ Built, demo ready
**Concept:** 24/7 agent that analyzes inbox/calendar/files while you sleep, delivers morning briefing
**One-liner:** "Your AI organizes your chaos while you sleep"

**Files:**
- `demo/index.html` - Interactive demo
- `demo/pitch-slides.html` - Pitch deck (8 slides)
- `demo/PITCH_SCRIPT.md` - 90-second script
- `agents/night_shift.py` - Core agent
- `run_night_shift.py` - Entry point

---

## IDEA 2: Distill ⭐ RECOMMENDED
**Status:** ✅ Built, demo ready
**Concept:** AI that watches your work, learns your patterns, and CONTINUES your work overnight
**One-liner:** "Your AI continues your work while you sleep"

**Files:**
- `demo/distill-demo.html` - Interactive demo (type animation)
- `demo/distill-pitch.html` - Pitch deck (8 slides)
- `agents/distill.py` - Core agent
- `DISTILL_CONCEPT.md` - Full concept doc

---

## Why Distill is Better

| Aspect | Night Shift | Distill |
|--------|-------------|---------|
| **What it does** | Organizes existing work | Creates NEW work |
| **Value** | Saves 2 hours of triage | Adds 4+ hours of output |
| **Wow factor** | "Cool, it organized my inbox" | "Holy shit, it wrote my report" |
| **Ara alignment** | Good | Perfect - shows computer use + 24/7 value |

---

## Quick Start

### View Night Shift Demo
```bash
open demo/index.html
open demo/pitch-slides.html
```

### View Distill Demo
```bash
open demo/distill-demo.html
open demo/distill-pitch.html
```

### Run Agent (requires API key)
```bash
./setup.sh
# Add ANTHROPIC_API_KEY to .env
python agents/distill.py
```
