# Executive Summary: Real-Time Ferry Ticket Sales & Redemption Analytics for Toronto Island Park

**Prepared For:** Toronto Government Parks, Forestry & Recreation & Ferry Management Stakeholders  
**Prepared By:** Etuka Leela Prasad  
**Audit Scope:** 261,538 15-Minute Intervals (May 1, 2015 – December 21, 2025) | Jack Layton Ferry Terminal  

---

## 1. Executive Purpose
This executive briefing synthesizes decade-long 15-minute passenger flow data from the **Jack Layton Ferry Terminal** (serving Centre Island, Hanlan's Point, and Ward's Island). It provides government policymakers, terminal operations teams, and fleet managers with validated performance benchmarks and target-bound recommendations to improve ferry scheduling, eliminate midday terminal bottlenecks, and optimize seasonal fleet utilization.

---

## 2. Validated Key Performance Indicators (KPIs) & Definitions

| KPI Name | Mathematical Formula | Verified Figure (2015–2025) | Strategic & Operational Meaning |
| :--- | :--- | :--- | :--- |
| **Tickets Sold per Hour** | $\text{Sum(Sales)} / (\text{Intervals} / 4)$ | **198.40 tickets / hr** | **12,972,051** total tickets sold across **65,384.50** recorded hours |
| **Tickets Redeemed per Hour** | $\text{Sum(Redemptions)} / (\text{Intervals} / 4)$ | **195.54 tickets / hr** | **12,785,293** total turnstile boardings (**98.56%** redemption rate) |
| **Net Passenger Movement** | $\text{Sum(Sales)} - \text{Sum(Redemptions)}$ | **+186,758 tickets** | **+385,104** Weekday advance buffer vs. **-198,346** Weekend gate drawdown |
| **Peak Demand Windows** | $(\text{Redemptions}_{10:00-17:59} / \text{Total}) \times 100$ | **79.43% Share (12:00 Peak)** | **10,155,154** boardings occur in the 8-hour window (`10:00–17:59`) |
| **Off-Season Utilization Index** | $(\text{Non-Summer Redemptions} / \text{Total}) \times 100$ | **37.42% Non-Summer Share** | **4,784,332** off-season boardings vs. **8,000,961 (62.58%)** in Summer |
| **Extreme Surge Thresholds (P99)** | $99\text{th Percentile per 15-Min Interval}$ | **Sales > 458 | Redemp > 508** | **3,236 intervals (1.24%)** exceed critical terminal congestion limits |

---

## 3. Core Empirical Insights for Government Stakeholders
1. **Midday Turnstile Compression (10:00–17:59):** Nearly four out of five passengers (**79.43% / 10,155,154**) board between **10:00 AM and 5:59 PM**, peaking sharply at **12:00 noon**. During this window, redemptions exceed concurrent ticket sales by **-488,030**, as visitors arrive with pre-purchased online tickets.
2. **Friday Pre-Buying Fuels Weekend Gate Surges:** On Weekdays, sales exceed redemptions by **+385,104** (led by **Friday at +163,905**). Those pre-bought tickets are redeemed en masse on **Saturday (21.86% share / -67,614 net)** and **Sunday (20.98% share / -130,732 net)**, concentrating **42.84% (5,476,734)** of all passenger traffic into just two days.
3. **Strong Shoulder-Season Demand (37.42% Off-Season Index):** While Summer drives **62.58% (8.00M)** of traffic, **Fall captures 20.39% (2.61M)** and **Spring captures 13.02% (1.66M)**, with **Winter maintaining a 4.01% (513K)** baseline for island residents and year-round visitors.

---

## 4. Actionable Policy and Operational Recommendations
1. **Deploy Rolling-Average Surge Triggers at Terminal Gates (Operations Team):**
   - **Action:** Use the **1-Hour Rolling Redemption Average (4-interval mean)** as a real-time dispatch trigger. When rolling throughput exceeds **350 tickets per 15-minute interval** (70% of the P99 surge limit of 508), automatically deploy backup vessels and open all turnstile lanes.
   - **Target Impact:** Cut peak midday terminal queue wait times by **25%–30%** between **11:00 AM and 3:00 PM**.
2. **Introduce Weekend Timed-Entry Slots & Early-Bird Off-Peak Pricing (Policy Planners):**
   - **Action:** Address the **-198,346 weekend pre-purchase drawdown** by requiring timed-boarding window selections on **Saturdays and Sundays (10:00–15:00)**, paired with a **15% fare discount** for off-peak departures before **10:00 AM** (currently only **20.57%** of volume).
   - **Target Impact:** Shift **10%–12% of midday weekend demand** into pre-10:00 AM sailings, smoothing vessel load factors.
3. **Align Fleet Maintenance with Seasonal Demand Realities (Management Stakeholders):**
   - **Action:** Retain high-capacity summer vessel schedules through **September and October** to accommodate **Fall's 20.39% (2.61M) ridership share**, confining major vessel dry-dock overhauls strictly to **Winter (4.01% share)** and early **Spring (13.02% share)**.