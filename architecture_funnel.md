# 📐 Architecture Funnel — Bible Quiz App
## MVP → Growth-Ready Funnel Architecture

This document describes the **end-to-end funnel architecture** for the **Bible Quiz App**, from anonymous entry to premium conversion, including data flow, models, services, and growth mechanics.

The architecture is intentionally **lean**, **modular**, and **scalable**, optimized for:
- fast MVP shipping
- habit formation (daily streaks)
- viral group growth
- gradual monetization (Teacher Mode)

---

## 🎯 Funnel Overview (High-Level)

Social Media (Question of the Day)
↓
Instant Play (No Login)
↓
Quiz Completion
↓
Save Your Streak (Email Capture)
↓
Nurture Email (Day 1)
↓
Teacher Mode Landing
↓
Group Creation (Premium)
↓
Invites → New Users → Loop


This funnel is designed to **remove friction early**, then **add commitment progressively**.

---

## 🧩 Core Architectural Principles

1. **Anonymous-first**  
   Users can play before creating an account.

2. **Progressive Identity**  
   Email is captured only after value is delivered.

3. **Event-driven**  
   Streaks, emails, upgrades, and analytics are triggered by events.

4. **Modular SaaS Design**  
   Each funnel step maps to a Django app/module.

5. **Growth before Monetization**  
   Teacher Mode converts engaged users, not cold users.

---

## 🏗️ Project Structure (Funnel-Oriented)

project_root/
│
├── core/
│ ├── settings/
│ ├── middleware/
│ ├── logging/
│ └── security/
│
├── quiz/
│ ├── models.py
│ ├── services.py
│ ├── api/
│ └── ui/
│
├── sessions/
│ ├── models.py
│ ├── middleware.py
│ └── services.py
│
├── streaks/
│ ├── models.py
│ ├── services.py
│ └── signals.py
│
├── emails/
│ ├── templates/
│ ├── tasks.py
│ └── models.py
│
├── groups/
│ ├── models.py
│ ├── services.py
│ ├── api/
│ └── ui/
│
├── payments/
│ ├── models.py
│ ├── stripe.py
│ ├── webhooks.py
│ └── permissions.py
│
├── analytics/
│ ├── models.py
│ └── services.py
│
├── dashboard/
├── landing/
├── utils/
└── architecture_funnel.md


---

## 🔁 Funnel Step Architecture

---

## 1️⃣ Entry Point — Social Media Challenge

### Purpose
Drive traffic using curiosity and challenge.

### Key Elements
- “Question of the Day”
- Shareable content
- Deep link into quiz

### Components
- Static or scheduled content
- Optional `MarketingCampaign` model
- UTM tracking support

---

## 2️⃣ Instant Play — Anonymous Quiz

### Purpose
Deliver value immediately with **zero friction**.

### Flow

User arrives → anonymous_session_id created → quiz loaded


### Key Components
**Model**
```python
AnonymousSession
- id (UUID)
- created_at
- last_seen
- metadata (JSON)

Middleware

Assigns cookie-based anonymous session

Reused across requests

API

GET /api/v1/quiz/daily/

POST /api/v1/quiz/submit/

3️⃣ Quiz Completion
Purpose

Create a psychological “win” before asking for commitment.

Components

QuizResult (temporary or persisted)

Score calculation

Difficulty tracking

Event

quiz_completed

Triggers:

result screen

streak prompt eligibility

4️⃣ Lead Capture — Save Your Streak
Purpose

Convert anonymous users into identified users.

UX

Modal shown after quiz completion:

“Great score! Enter your email to save your streak permanently.”

Components

Model

Streak
- email
- current_count
- last_played_at
- source (anonymous / registered)

Flow

AnonymousSession + Email
→ Create Streak
→ Link session → streak
→ Trigger email sequence

API

POST /api/v1/streaks/save/

5️⃣ Nurture Step — Email Automation
Purpose

Build trust, habit, and curiosity.

MVP Scope

Only Day 1 email is required.

Components

Models

EmailEventLog
- email
- event_type
- sent_at

Celery Tasks

send_day1_streak_email

Email Content

Streak confirmation

Free PDF resource

Soft CTA

6️⃣ Conversion — Teacher Mode
Purpose

Turn engaged individuals into community leaders.

Positioning

Teacher Mode is:

leadership

accountability

community impact

Components

Landing Page

/teacher-mode/

Value-driven copy

CTA: “Create Your Group”

7️⃣ Group Creation — Viral Engine
Purpose

Create the viral loop.

Components

Models

Group
- name
- group_code
- owner_email
- created_at

GroupMembership
- group
- email
- role (admin / member)

Flow

Teacher creates group
→ Receives invite link
→ Shares link
→ New users join and play

API

POST /api/v1/groups/create/

POST /api/v1/groups/join/

🔁 Viral Loop Mechanics
Core Loop

Play → Streak → Email → Group → Invites → Play

Amplifiers

Group streak pressure

Leaderboard (post-MVP)

Shareable results

Weekly challenges

💳 Monetization Architecture (Post-MVP Ready)
Strategy

Soft paywall

Upgrade when value is clear

Model

Subscription
- email
- plan (free / teacher)
- stripe_customer_id
- status

Enforcement

Permissions layer

Feature gating on group creation

📊 Analytics Architecture
Purpose

Measure funnel health and growth.

Model

AnalyticsEvent
- event_type
- session_id
- email
- metadata
- created_at

Tracked Events

quiz_started

quiz_completed

streak_saved

email_sent

teacher_mode_viewed

group_created

invite_accepted

🧠 MVP vs Post-MVP Boundary
MVP Includes

Anonymous quiz

Email capture

Day 1 email

Teacher Mode landing

Group creation

Post-MVP

Stripe payments

Leaderboards

Multi-day email sequence

Admin dashboards

Advanced analytics

🏁 Final Notes

This funnel architecture prioritizes:

speed to launch

habit formation

community-driven growth

It is intentionally simple, extensible, and aligned with real-world church and group dynamics.

Build momentum first. Optimize later.

