# 🍕 Free Food Fetcher

**Never miss free food on campus again.**

An AI agent that scans JHU campus 24/7 and alerts you when there's free food. Built on [Ara](https://ara.so) for the Ara x Johns Hopkins Hackathon.

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

## 🚀 Quick Start

### Try the Demo
```bash
# Open the pitch demo
open demo/freefood-pitch.html

# Or the interactive map
open demo/freefood-map.html
```

### Run on Ara
```bash
# Install Ara SDK
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
│   ├── freefood-pitch.html      # Main pitch demo
│   ├── freefood-map.html        # Interactive map
│   └── freefood-demo.html       # Card-based demo
├── freefood_full.py             # Main Ara agent
├── freefood_live.py             # Real web scraping version
├── freefood_ara.py              # Basic version
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
