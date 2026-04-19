# Distill - Pitch Script

**Total Time: 90 seconds**

---

## OPENING (0:00 - 0:15)

**[SHOW: You working late, leaving unfinished work on screen]**

> "Every night, I close my laptop with work unfinished. That README half-written. Those docstrings missing. That research tab still open.
>
> I tell myself I'll finish it tomorrow. But tomorrow brings NEW work."

---

## THE PROBLEM (0:15 - 0:25)

**[SHOW: Split screen - person sleeping vs. cursor blinking on incomplete document]**

> "While I sleep, my unfinished work just sits there. Waiting.
>
> By morning, I've lost context. I've lost momentum. I start over."

---

## THE SOLUTION (0:25 - 0:50)

**[SHOW: Distill logo, then animated screen capture montage]**

> "Introducing **Distill** — an AI shadow that watches you work all day, then continues your work while you sleep.
>
> All day, Distill captures your screen. It learns what apps you use. What documents you edit. How you write. Your style.
>
> At 3 AM, while you're asleep, Distill gets to work. It extends your README. Adds docstrings to your code. Researches topics you were exploring.
>
> In YOUR voice. In YOUR style."

---

## THE DELIVERY (0:50 - 1:05)

**[SHOW: Phone receiving Telegram message with morning report]**

> "Then at 7 AM, you get a message:
>
> 'Good morning. I extended 3 documents. Added 1,200 words. Completed your API documentation. Ready for review.'
>
> **You wake up to finished work. Not unfinished lists.**"

---

## WHY ARA (1:05 - 1:20)

**[SHOW: Ara logo, cloud infrastructure visualization]**

> "Distill runs 24/7 on Ara's cloud infrastructure.
>
> Isolated sandboxes keep your data secure. Multi-channel messaging meets you where you are.
>
> This is the future: **AI that doesn't just assist — it EXTENDS you.**"

---

## CLOSING (1:20 - 1:30)

**[SHOW: Demo website, tagline]**

> "We're Distill. Your AI shadow.
>
> **Always watching. Always working. Always you.**"

---

# Recording Instructions

## Option 1: Screen Recording (Easiest)
1. Open `demo/distill-full-demo.html` in Chrome
2. Use QuickTime (Mac) or OBS to record screen
3. Record yourself reading the script as voiceover
4. Click through the demo stages as you speak

## Option 2: Loom (Quick & Easy)
1. Install Loom Chrome extension
2. Open the demo page
3. Record with face bubble + screen
4. Share link directly

## Option 3: Live Demo
1. Open `distill-full-demo.html` for the tracking visualization
2. Open `distill-live.html` for interactive document extension
3. Show both during your presentation

---

# Key Talking Points for Judges

1. **Technical depth**: "We combine Claude Vision for screen analysis, NLP for style extraction, and agentic document generation. Full pipeline running 24/7."

2. **Why Ara**: "This requires always-on cloud infrastructure. Can't do overnight work without 24/7 runtimes. Ara makes this possible."

3. **The insight**: "The best AI doesn't replace you — it multiplies you. Distill works exactly like you would, just at 3 AM."

4. **Style matching**: "We don't just complete documents — we complete them in YOUR voice. Same tone, same structure, same you."

5. **Why it's viral**: "Imagine posting your morning message: 'My AI wrote 1,200 words while I slept.' Screenshots go viral."

---

# Demo Flow for Live Presentation

1. **Hook** (10 sec): "Raise your hand if you closed your laptop with unfinished work this week."

2. **Problem** (15 sec): "That work is still sitting there. Waiting."

3. **Screen Demo** (30 sec): Open `distill-full-demo.html`, show capture → analysis → extension flow

4. **Live Demo** (30 sec): Open `distill-live.html`, show real-time document extension with style matching

5. **Close** (10 sec): "Distill. Your AI shadow. Always working."

---

# One-Liner Variations

- "Distill: Your AI shadow that works while you sleep"
- "Watch you work. Learn your style. Continue your work."
- "Wake up to finished work, not unfinished lists"
- "The AI that extends you, 24/7"
- "Your work doesn't stop when you do"

---

# Ara Integration Points (For Technical Q&A)

```
┌─────────────────────────────────────────────────────────────┐
│                    DISTILL ON ARA                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Ara Sandbox                                                │
│   ───────────                                                │
│   • Python 3.11 runtime                                      │
│   • 10GB persistent storage for screenshots                  │
│   • Secure credential handling                               │
│   • 24/7 execution                                           │
│                                                              │
│   Ara Channels                                               │
│   ────────────                                               │
│   • Telegram: Morning reports                                │
│   • WhatsApp: Optional delivery                              │
│   • Discord: Team notifications                              │
│                                                              │
│   Ara Scheduling                                             │
│   ──────────────                                             │
│   • Cron: 0 3 * * * (3:00 AM daily)                          │
│   • Function: run_overnight_extension()                      │
│   • Timezone: User's local                                   │
│                                                              │
│   ClawHub Integration                                        │
│   ───────────────────                                        │
│   • Skill: distill/extend                                    │
│   • Commands: /track, /extend, /report                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

# Quick Commands for Demo

```bash
# Open full demo suite
open demo/distill-full-demo.html
open demo/distill-live.html
open demo/ara-integration.html

# Run CLI deployment demo
python3 deploy_to_ara.py --demo

# Show pitch slides
open demo/distill-pitch.html
```
