# Free Food Fetcher - Design Plan v2.0

## Vision
**"The Yelp of Free Food for College Students"**

Transform from a simple alert system into a social platform where students share, rate, and discover free food across campus.

---

## 1. User Tiers & Access

### Public Users (No Login)
```
┌─────────────────────────────────────────┐
│  🌐 PUBLIC ACCESS                        │
├─────────────────────────────────────────┤
│  Can View:                              │
│  • Baltimore city events                │
│  • Public JHU events (hub.jhu.edu)      │
│  • Homewood campus map                  │
│                                         │
│  Cannot View:                           │
│  • Department-specific events           │
│  • Private club events                  │
│  • Student-submitted events             │
│                                         │
│  Cannot Do:                             │
│  • Submit reviews                       │
│  • Connect Outlook/Calendar             │
│  • Get personalized alerts              │
└─────────────────────────────────────────┘
```

### JHU Authenticated Users
```
┌─────────────────────────────────────────┐
│  🔒 JHU LOGIN (xxxxx@jhu.edu)           │
├─────────────────────────────────────────┤
│  Can View:                              │
│  • Everything public users see          │
│  • ALL department events (shared pool)  │
│  • Private club submissions             │
│  • Reviews and ratings                  │
│                                         │
│  Can Do:                                │
│  • Connect Outlook/Google Calendar      │
│  • Submit events from their department  │
│  • Write reviews with photos            │
│  • Earn badges and titles               │
│  • Get personalized Telegram alerts     │
└─────────────────────────────────────────┘
```

---

## 2. The "Shared Pool" Concept

### How Cross-Department Sharing Works

```
┌────────────────────────────────────────────────────────────────┐
│                     SHARED FOOD POOL                            │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Physics Student         ECE Student          CS Student      │
│   connects Outlook   →    connects Outlook →   connects Outlook│
│        │                       │                    │          │
│        ▼                       ▼                    ▼          │
│   ┌─────────┐            ┌─────────┐          ┌─────────┐     │
│   │ Physics │            │   ECE   │          │   CS    │     │
│   │ Events  │            │ Events  │          │ Events  │     │
│   └────┬────┘            └────┬────┘          └────┬────┘     │
│        │                      │                    │           │
│        └──────────────────────┼────────────────────┘           │
│                               ▼                                 │
│                    ╔═══════════════════╗                       │
│                    ║   SHARED POOL     ║                       │
│                    ║                   ║                       │
│                    ║  All JHU students ║                       │
│                    ║  can see ALL      ║                       │
│                    ║  department food  ║                       │
│                    ║  events!          ║                       │
│                    ╚═══════════════════╝                       │
│                                                                 │
│   "I'm Physics but I can see ECE's Chipotle event!"           │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### Privacy Rules
- Events are **opt-in** to share (default: shared)
- Users can mark events as "My Department Only"
- No personal calendar data is shared, only events with food signals

---

## 3. Review & Rating System

### Event Rating
```
┌─────────────────────────────────────────────────────────────┐
│  📸 REVIEW: ACM Meeting Pizza                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ⭐⭐⭐⭐☆  4.2 / 5  (23 reviews)                           │
│                                                              │
│  📊 Ratings Breakdown:                                       │
│  ├── 🍕 Food Quality:     ████████░░ 4.3                    │
│  ├── 📦 Portion Size:     ███████░░░ 3.8                    │
│  ├── ⏰ Availability:     █████████░ 4.5                    │
│  └── 🎯 Accuracy:         ████████░░ 4.1                    │
│                                                              │
│  📷 Photos (12)                                              │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                           │
│  │ 🍕  │ │ 🍕  │ │ 🍕  │ │ 📍  │                           │
│  └─────┘ └─────┘ └─────┘ └─────┘                           │
│                                                              │
│  💬 Recent Reviews:                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 🏆 PizzaHunter99 (Gold Reviewer)                    │    │
│  │ "Dominos but still free. Arrived 5min early,        │    │
│  │  got 3 slices. Pro tip: sit near the door."        │    │
│  │ ⭐⭐⭐⭐☆ • 2 hours ago                              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Review Tags (Quick Select)
```
Food Tags:        [ 🍕 Pizza ] [ 🌮 Mexican ] [ 🍜 Asian ] [ 🥗 Healthy ]
Vibe Tags:        [ 👥 Crowded ] [ 😌 Chill ] [ ⚡ Grab & Go ] [ 🎉 Party ]
Quality Tags:     [ 🔥 Worth It ] [ 😐 Mid ] [ 💀 Gone Fast ] [ ♻️ Leftovers ]
```

---

## 4. Gamification: Reviewer Titles

### Title System (Esports-Inspired)

```
┌─────────────────────────────────────────────────────────────┐
│  🎮 REVIEWER RANKS                                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  TIER 1: Starter (0-5 reviews)                              │
│  ├── 🥄 "Hungry Student"                                    │
│  └── 🍽️ "Food Curious"                                      │
│                                                              │
│  TIER 2: Regular (5-20 reviews)                             │
│  ├── 🍕 "Pizza Scout"                                       │
│  ├── 🌮 "Taco Tracker"                                      │
│  └── 🍜 "Noodle Navigator"                                  │
│                                                              │
│  TIER 3: Expert (20-50 reviews)                             │
│  ├── 🏃 "Speed Eater" (first to review)                     │
│  ├── 📸 "Food Paparazzi" (most photos)                      │
│  └── 🎯 "Accuracy King" (predictions match reality)         │
│                                                              │
│  TIER 4: Legend (50+ reviews)                               │
│  ├── 👑 "Campus Food God"                                   │
│  ├── 🦁 "The Jungle King" (dominates one area)              │
│  └── 🌍 "Free Food Legend"                                  │
│                                                              │
│  SPECIAL TITLES (Achievement-Based)                         │
│  ├── 🥇 "First Blood" (first review of an event)            │
│  ├── 🔥 "Hot Streak" (reviewed 7 days in a row)             │
│  ├── 🌙 "Night Owl" (reviews after 10pm)                    │
│  ├── 🌅 "Early Bird" (reviews before 9am)                   │
│  ├── 📍 "Explorer" (reviewed in 10+ buildings)              │
│  └── 💯 "Perfect Taste" (all reviews rated helpful)         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Leaderboard
```
┌─────────────────────────────────────────────────────────────┐
│  🏆 THIS WEEK'S TOP REVIEWERS                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 👑 PizzaHunter99      │ 12 reviews │ "Campus Food God"  │
│  2. 🦁 TacoMaster_JHU     │ 9 reviews  │ "The Jungle King"  │
│  3. 🏃 SpeedyEats         │ 8 reviews  │ "Speed Eater"      │
│  4. 📸 FoodiePhotos       │ 7 reviews  │ "Food Paparazzi"   │
│  5. 🍜 NoodleFan2026      │ 6 reviews  │ "Noodle Navigator" │
│                                                              │
│  YOUR RANK: #23 🍕 "Pizza Scout"                            │
│  Next title in: 3 more reviews                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. UI/UX Design

### Main Feed (Authenticated)
```
┌─────────────────────────────────────────────────────────────┐
│  🍕 Free Food Fetcher                    [🔔] [👤 Leo Z]    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  🔥 HAPPENING NOW                                    │    │
│  │                                                      │    │
│  │  ┌────────────────────────────────────────────────┐ │    │
│  │  │ 🍕 CS Department Talk           📍 Hackerman   │ │    │
│  │  │ ⭐ 4.5 (8 reviews) • 🔒 JHU Only              │ │    │
│  │  │ "Pizza after the talk" • Ends in 45min        │ │    │
│  │  │ [📸 2 photos] [💬 View Reviews]               │ │    │
│  │  └────────────────────────────────────────────────┘ │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  📅 COMING UP                                        │    │
│  │                                                      │    │
│  │  6:00 PM • 🌮 ACM Meeting        • Malone Hall      │    │
│  │           └ Chipotle! • 🔒 JHU • ⭐ 4.8 avg        │    │
│  │                                                      │    │
│  │  7:00 PM • 🍕 Game Showcase      • Hodson Hall      │    │
│  │           └ Free pizza • 🌐 Public • NEW           │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  [🗺️ Map] [📋 List] [⭐ Top Rated] [🔥 Trending]           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Event Detail Page
```
┌─────────────────────────────────────────────────────────────┐
│  ← Back                                         [🔔 Alert]  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                    [MAP VIEW]                        │    │
│  │                  📍 Malone Hall                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  🌮 ACM Club Meeting                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                              │
│  📍 Malone Hall 228                                         │
│  🕐 Today, 6:00 PM - 7:30 PM                                │
│  🍽️ Chipotle burritos and bowls                            │
│  🔒 JHU Students Only                                       │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  📊 COMMUNITY RATINGS                                │    │
│  │                                                      │    │
│  │  ⭐⭐⭐⭐⭐ 4.8 / 5  (34 reviews)                    │    │
│  │                                                      │    │
│  │  🍕 Food:  █████████░ 4.9                           │    │
│  │  📦 Size:  ████████░░ 4.2                           │    │
│  │  ⏰ Wait:  ███████░░░ 3.8                           │    │
│  │                                                      │    │
│  │  Top Tags: [🔥 Worth It] [🌮 Mexican] [👥 Crowded]  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  📸 PHOTOS (18)                                             │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                  │
│  │     │ │     │ │     │ │     │ │ +14 │                  │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘                  │
│                                                              │
│  [✍️ Write Review]  [📸 Add Photo]  [📤 Share]             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Technical Architecture

### System Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                        ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│   │   Frontend   │     │   Backend    │     │   Ara Cloud  │   │
│   │   (React)    │◄───►│   (FastAPI)  │◄───►│   (Agent)    │   │
│   └──────────────┘     └──────────────┘     └──────────────┘   │
│          │                    │                    │            │
│          ▼                    ▼                    ▼            │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│   │  JHU SSO     │     │  PostgreSQL  │     │  Web Scraper │   │
│   │  (SAML)      │     │  + Redis     │     │  (24/7)      │   │
│   └──────────────┘     └──────────────┘     └──────────────┘   │
│                               │                                  │
│                               ▼                                  │
│                        ┌──────────────┐                         │
│                        │  S3 / CDN    │                         │
│                        │  (Photos)    │                         │
│                        └──────────────┘                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Database Schema (Simplified)
```sql
-- Users
users (
    id, jhu_email, display_name, department,
    title, review_count, created_at
)

-- Events
events (
    id, title, location, building, coords,
    start_time, end_time, food_description,
    food_score, source, is_public,
    submitted_by, created_at
)

-- Reviews
reviews (
    id, event_id, user_id,
    food_rating, portion_rating, wait_rating,
    comment, tags, created_at
)

-- Photos
photos (
    id, review_id, user_id, url, created_at
)

-- User Connections (OAuth)
connections (
    id, user_id, provider, access_token,
    refresh_token, created_at
)
```

---

## 7. Viral Features

### 1. Share Cards
```
┌─────────────────────────────────────────┐
│  🍕 FREE PIZZA ALERT                    │
│                                         │
│  ACM Meeting @ Malone Hall              │
│  Today 6:00 PM                          │
│                                         │
│  ⭐ 4.8 rating • 34 reviews             │
│  "Best Chipotle on campus" - @user      │
│                                         │
│  🔗 freefoodfetcher.com/e/acm-123       │
│                                         │
│  #FreeFoodJHU #JHU #FreePizza           │
└─────────────────────────────────────────┘
```

### 2. Weekly Digest Email
```
Subject: 🍕 You saved $47 on food this week!

Hey Leo!

This week you attended 4 free food events:
• ACM Meeting (Chipotle) - ⭐ You rated 5/5
• CS Talk (Pizza) - ⭐ You rated 4/5
• Study Break (Snacks)
• Game Night (Pizza)

💰 Estimated savings: $47

🏆 Your rank: #23 on campus
📈 2 spots up from last week!

Next title: "Pizza Scout" (3 more reviews)

See what's coming up → [View Events]
```

### 3. Push Notification Copy
```
🍕🔥 PIZZA ALERT: CS Talk in Hackerman (15 min)
Last time this event got ⭐4.8 - don't miss it!

🌮 Chipotle at ACM in 2 hours
Pro tip: Arrive 10min early - it goes FAST

👑 You're #5 on the leaderboard this week!
2 more reviews to reach "Pizza Scout" 🍕
```

### 4. Referral System
```
"Invite friends, get titles faster!"

Share your code: LEOZ-PIZZA

Benefits:
• You: +5 review points per signup
• Friend: Starts with "Food Explorer" title

Milestones:
• 5 referrals → 🎁 "Recruiter" badge
• 10 referrals → 🏆 "Campus Ambassador" title
• 25 referrals → 👑 "Food Network" legendary status
```

---

## 8. MVP Scope (Hackathon)

### Phase 1: Demo (TODAY)
- [x] Public event scraping via Ara
- [x] Interactive campus map
- [x] Basic event cards
- [x] Mobile-friendly pitch page

### Phase 2: Auth + Reviews (Week 1)
- [ ] JHU SSO integration (mock for demo)
- [ ] Public/Private event tags
- [ ] Basic review submission
- [ ] Photo upload

### Phase 3: Social (Week 2-3)
- [ ] Leaderboard
- [ ] Titles and badges
- [ ] Share cards
- [ ] Weekly digest

### Phase 4: Full Integration (Month 1)
- [ ] Outlook/Google Calendar OAuth
- [ ] Cross-department event sharing
- [ ] Telegram bot alerts
- [ ] Mobile app (React Native)

---

## 9. Success Metrics

| Metric | Target (Month 1) |
|--------|-----------------|
| Registered Users | 500 JHU students |
| Daily Active Users | 100 |
| Events Tracked | 50/week |
| Reviews Submitted | 200 |
| Avg Rating Accuracy | 85% |
| Referral Rate | 20% |

---

## 10. Monetization (Future)

**Free Forever for Students**

Revenue ideas:
1. **Campus Partnerships** - Dining services pay for promotion
2. **Sponsored Events** - Brands pay to be featured
3. **Expand to Other Schools** - License the platform
4. **Premium Titles** - Custom titles for $1.99

---

## Summary

**Free Food Fetcher v2.0** transforms from an alert tool into a **social platform** where:

1. **Anyone** can see public Baltimore/JHU events
2. **JHU students** share department-specific food finds
3. **Reviews & photos** help others know what to expect
4. **Gamification** makes it fun and viral
5. **Ara powers** the 24/7 backend scraping

**Tagline Options:**
- "The Yelp of Free Food"
- "Never Miss. Always Rate. Eat Free."
- "Campus Food, Crowdsourced"
