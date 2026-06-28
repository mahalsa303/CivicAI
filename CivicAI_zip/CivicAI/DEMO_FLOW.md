# CivicAI — Hackathon Demonstration Guide & Pitch Flow

This document outlines the step-by-step presentation script to showcase CivicAI's capabilities to hackathon judges in 2-3 minutes.

---

## 📋 Pre-Demo Setup
1. Open the application locally:
   ```bash
   streamlit run app.py
   ```
2. Navigate to the **Settings** page (using the sidebar menu).
3. Set **Default Reporter Name** to `Ananya Sen` (or any custom name).
4. Turn on the **Demo Mode** toggle. This instantly populates the map, charts, feeds, and AI command center with 35 realistic reports, ensuring the platform looks fully populated and production-grade.

---

## 🏁 Step-by-Step Presentation Script

### Step 1: Onboarding Landing & Navbar (30 seconds)
* **Action**: Open the **Dashboard** page.
* **Talk Track**: 
  > *"Welcome to CivicAI — Community Hero, a modern SaaS civic platform designed to connect citizens and municipal departments. At the top of the dashboard, our 'Why CivicAI?' onboarding panel immediately briefs new users on our three pillars: AI Analysis, Geotagged Maps, and Leaderboard Gamification. Banners at the top dynamically highlight current public campaigns like Clean City Drives or Road Safety Weeks."*
* **Key Features to Point Out**:
  * **Top Navbar**: Notification center bell (click to show mock pipeline and repair updates), location profiles, search bar, and active user profile badge.

### Step 2: AI Command Center & Metrics (30 seconds)
* **Action**: Scroll down the dashboard.
* **Talk Track**: 
  > *"Our dashboard metrics are calculated dynamically. The health score penalizes the city's rating based on active high-severity issues. The highlight here is the **AI Command Center**. Gemini reads the current database statistics in real-time and compiles a concise narrative digest, warning authorities of hotspots and suggesting immediate priority actions."*
* **Key Features to Point Out**:
  * Metrics sparklines and weekly deltas.
  * AI Command Center narrative panel.

### Step 3: Recent Reports & Deep-Dive Timelines (30 seconds)
* **Action**: Click `Track Issue 🔍` on any report card (e.g., Road Damage).
* **Talk Track**: 
  > *"Issues are displayed as clean cards with severity badges and vote counters. Clicking 'Track' opens our AI Deep-Dive. This modal renders a visual processing timeline. Judges can review the **Explain AI Decision** section, which uses Gemini to justify why this category was selected, why the department was routed, and how the priority score was determined, establishing complete transparency."*
* **Key Features to Point Out**:
  * Chronological status steps (Open $\rightarrow$ Verified $\rightarrow$ In Progress $\rightarrow$ Resolved).
  * Explainable AI justifications (Category, Department, and Priority explanations).

### Step 4: Standalone Map & Plotly Analytics (30 seconds)
* **Action**: Navigate to **Community Map** and then **Analytics** pages.
* **Talk Track**: 
  > *"Our Map page isolates coordinates. Markers are colored dynamically by severity (Red, Orange, Green), and clicking a marker displays complaint details. In Analytics, we plot 6 Plotly distributions and trend lines, including category counts, workload distributions per department, and community health performance over time. Changing filters in the sidebar updates all map points and Plotly figures instantly."*

### Step 5: Split-Screen Reporting & Duplication Intercept (30 seconds)
* **Action**: Navigate to **Report Issue** page. Explain the ChatGPT-like split screen.
  * Enter a text description: *"Water leak in Hostel road near the main pipeline"*
  * Click **Submit & Analyze**.
* **Talk Track**: 
  > *"When filing a report, the screen splits. While Gemini analyzes the text, a pulsing skeleton loader is shown. If we try to submit a report that is geographically close and in the same category as an existing report, our **Geospatial Proximity Matcher** intercepts the write, warning the citizen of a possible duplicate and allowing them to cancel or force submission, preventing database spam."*
* **Key Features to Point Out**:
  * Skeleton Loader pulse effect.
  * Duplicate detection dialogue popup with review columns.
  * AI resolution preview card (Department, Cost, Steps, Time).
