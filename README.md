# 🍕 Free Food Fetcher v2.0 - We won the hackathon! 

**Never miss free food on campus again.**

An AI agent that scans JHU campus 24/7 and alerts you when there's free food. Built on [Ara](https://ara.so) for the Ara x Johns Hopkins Hackathon.

**[🚀 Try Live Demo](https://chuntungzhuangleo.github.io/freefood-fetcher/)**

![Demo](demo/screenshot.png)

## 🎯 The Problem

- You miss free pizza because you found out 2 hours late
- Events are scattered across Instagram, email, GroupMe...
- You spent $15 on lunch when there was free Chipotle next door

## ✨ The Solution

Free Food Fetcher uses AI to:
1. **Scan** JHU event calendars every hour
2. **Detect** food signals ("pizza provided", "catered lunch")
3. **Map** events on an interactive campus map
4. **Alert** you instantly via Telegram

## 🆕 v2.0 Features

### 🔐 Public & Private Events
- **Public events** visible to everyone
- **Private events** require JHU SSO login
- Cross-department sharing - connect your department, share with others!

### 🏆 Gamification & Leaderboard
Earn titles like esports pros:
| Rank | Title | Points |
|------|-------|--------|
| 🥇 | Campus Food God | 500+ |
| 🥈 | Pizza Hunter | 200+ |
| 🥉 | Food Scout | 100+ |
| - | Hungry Student | 0+ |

### ⭐ Review System
- Rate events (1-5 stars)
- Add photos of the food
- Tag quality: "Worth the Walk", "Gone in 5 min", "Amazing Quality"
- Help others know what to expect!

### 📊 Shared Pool
- ECE students see Physics events
- CS department shares with Math
- Growing network effect across campus

## 🚀 Quick Start

### Try the Demo
```bash
# Open the v2 demo (recommended)
open demo/freefood-v2.html

# Or the pitch demo
open demo/freefood-pitch.html
```

### Run on Ara
```bash
# Install Ara SDK (requires Python 3.10+)
pip install ara-sdk

# Login to Ara
ara auth login

# Deploy (runs every hour)
ara deploy freefood_full.py --cron "0 * * * *"

# Run now
ara run freefood_full.py
```

## 📁 Project Structure

```
├── demo/
│   ├── freefood-v2.html          # 🆕 Full v2 demo with all features
│   ├── freefood-pitch.html       # Pitch presentation
│   ├── freefood-map.html         # Interactive map
│   └── freefood-demo.html        # Card-based demo
├── freefood_full.py              # Main Ara agent
├── freefood_live.py              # Real web scraping version
├── DESIGN_PLAN.md                # v2.0 architecture & design
└── README.md
```

## 🔧 How It Works

```
┌─────────────────────────────────────────────────────────┐
│                   FREE FOOD FETCHER                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   1. SCAN          Ara browses JHU event pages          │
│        ↓                                                 │
│   2. DETECT        AI finds "free pizza" signals        │
│        ↓                                                 │
│   3. MAP           Events appear on campus map          │
│        ↓                                                 │
│   4. ALERT         Telegram notification sent           │
│        ↓                                                 │
│   5. REVIEW        Users rate & share photos            │
│        ↓                                                 │
│   6. RANK UP       Earn points and titles!              │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## ⚡ Powered by Ara

- **24/7 Execution** - Runs hourly in the cloud
- **Web Browsing** - AI actually visits event pages
- **Multi-Channel** - Telegram, WhatsApp, Discord alerts
- **One Command Deploy** - `ara deploy app.py`

## 📊 Features

| Feature | Status |
|---------|--------|
| JHU Event Calendar Scraping | ✅ Live |
| AI Food Detection | ✅ Live |
| Interactive Campus Map | ✅ Live |
| Telegram Alerts | ✅ Ready |
| Public/Private Events | ✅ v2.0 |
| JHU SSO Integration | ✅ v2.0 |
| Leaderboard & Titles | ✅ v2.0 |
| Review System | ✅ v2.0 |
| Cross-Department Sharing | ✅ v2.0 |
| Instagram Monitoring | 🔜 Coming |
| Email Scanning | 🔜 Coming |
| GroupMe Integration | 🔜 Coming |

## 🎓 Built For

**Ara x Johns Hopkins: Build Your Own AI Computer Hackathon**

April 19, 2026

## 👥 Team

- Leo Z ([@ChunTungZhuangLeo](https://github.com/ChunTungZhuangLeo))

## 📄 License

MIT License - feel free to use this for your campus!

---

**🍕 Never miss free food again!**
