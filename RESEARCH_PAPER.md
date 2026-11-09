# Technical Research Paper: Real-Time Ferry Ticket Sales & Redemption Analytics for Toronto Island Park

**Author:** Etuka Leela Prasad  
**Organization:** Unified Mentor Data Analytics Internship  
**Public Sector Context:** Toronto Government Parks, Forestry & Recreation — Jack Layton Ferry Terminal  
**Dataset Scope:** 261,538 15-Minute Intervals (May 1, 2015 – December 21, 2025)

---

## 1. Executive Abstract
Year-round ferry service connecting the Jack Layton Ferry Terminal to Centre Island, Hanlan's Point, and Ward's Island is a vital municipal transit lifeline and recreational corridor. While automated turnstiles and ticketing kiosks log transaction counts every 15 minutes, operational planners lacked an integrated analytical framework to quantify real-time passenger flow, advance ticket buffers, and seasonal capacity thresholds.

This study analyzes **261,538 15-minute intervals** spanning **65,384.50 operating hours** from May 2015 through December 2025, encompassing **12,972,051 tickets sold** and **12,785,293 tickets redeemed**. Empirical findings establish five core operational benchmarks:
1. **System Throughput & Advance Ticket Buffer:** The terminal averages **198.40 tickets sold per hour** and **195.54 tickets redeemed per hour**, producing a cumulative net positive movement of **+186,758 tickets** (`98.56%` overall redemption conversion).
2. **Midday Peak Window Concentration:** Exactly **79.43% (10,155,154)** of all passenger redemptions occur inside the 8-hour window between **10:00 and 17:59**, with **12:00 noon** serving as both the peak sales hour and peak redemption hour.
3. **Weekday Pre-Purchase vs. Weekend Turnstile Drawdown:** Weekdays generate **57.16% (7,308,559)** of redemptions with a net pre-purchase accumulation of **+385,104 tickets** (peaking on Fridays at `+163,905`), whereas Weekends pack **42.84% (5,476,734)** of redemptions into just two days (`Saturday: 21.86%`, `Sunday: 20.98%`) and experience a net turnstile drawdown of **-198,346 pre-purchased tickets**.
4. **Seasonal Distribution & Off-Season Utilization:** While Summer accounts for **62.58% (8,000,961)** of annual boardings, the **Off-Season Utilization Index reaches 37.42% (4,784,332)**—driven by **Fall (20.39% / 2,606,380)**, **Spring (13.02% / 1,664,773)**, and **Winter (4.01% / 513,179)**.
5. **Extreme Surge Outliers (99th Percentile):** The 99th-percentile threshold stands at **458 tickets sold** and **508 tickets redeemed** per 15-minute interval, with **3,236 intervals (1.24% of observations)** exceeding these critical congestion benchmarks.

---

## 2. Problem Statement and Research Objectives
Despite recording 15-minute transaction logs across a decade of operations, ferry management lacked a centralized analytics system to:
1. Identify exact peak passenger flow windows and intraday turnstile bottlenecks.
2. Track net passenger movement ($\text{Sales} - \text{Redemptions}$) to distinguish between online advance purchasing and physical terminal arrivals.
3. Quantify multi-scale rolling demand (`1-hour` and `4-hour` smoothing) and extreme 99th-percentile crowding events.
4. Establish data-driven scheduling, gate staffing, and vessel maintenance rules for Operations Teams, Policy Planners, and Management Stakeholders.

---

## 3. Data Architecture and Analytical Methodology

### 3.1 Data Ingestion and Cleaning Pipeline
The raw dataset (`Toronto Island Ferry Tickets.csv`) contains four attributes: `_id`, `Timestamp`, `Sales Count`, and `Redemption Count`.
- **Chronological Standardization:** All `Timestamp` strings were parsed into ISO-8601 `datetime64` objects and sorted ascending from `2015-05-01 13:30:00` to `2025-12-21 22:30:00`, yielding `261,538` valid 15-minute intervals.
- **Data Consistency Validation:** `Sales Count` and `Redemption Count` were validated as non-negative integers (`clip(lower=0)`), confirming zero corrupt negative entries.
- **Outlier Detection:** Using non-parametric percentile thresholding, intervals exceeding the 99th percentile (`Sales > 458` or `Redemptions > 508` per 15 minutes) were flagged via `Is_Outlier` (`3,236` total surge intervals).

### 3.2 Feature Engineering and Mathematical Definitions
Because observations occur at 15-minute intervals ($\Delta t = 0.25\text{ hours}$), 4 intervals equal 1 operating hour and 16 intervals equal 4 operating hours. All dashboard scorecards and report tables are governed by the following equations:

| KPI / Engineered Feature | Mathematical Formula | Verified Baseline Value | Analytical Interpretation |
| :--- | :--- | :---: | :--- |
| **Recorded Operating Hours ($H_{\text{total}}$)** | $\frac{N_{\text{intervals}}}{4}$ | $65,384.50\text{ hrs}$ | Total monitored time span across 261,538 intervals |
| **Tickets Sold per Hour ($R_{\text{sold}}$)** | $\frac{\sum \text{Sales Count}}{H_{\text{total}}}$ | $198.40\text{ / hr}$ | Mean hourly ticket sales velocity (`12,972,051` total) |
| **Tickets Redeemed per Hour ($R_{\text{redeemed}}$)** | $\frac{\sum \text{Redemption Count}}{H_{\text{total}}}$ | $195.54\text{ / hr}$ | Mean hourly turnstile boarding rate (`12,785,293` total) |
| **Net Passenger Movement ($\Delta P$)** | $\sum \text{Sales Count} - \sum \text{Redemption Count}$ | $+186,758$ | Net unredeemed advance ticket buffer (`+2.86 / hr`) |
| **Peak Demand Window Share ($S_{\text{peak}}$)** | $\left(\frac{\sum_{\text{hr}=10}^{17} \text{Redemptions}}{\sum \text{Redemptions}}\right) \times 100$ | $79.43\%$ | Share of boardings inside `10:00–17:59` (`10,155,154`) |
| **Off-Season Utilization Index ($I_{\text{off}}$)** | $\left(\frac{\sum_{\text{Spring,Fall,Winter}} \text{Redemptions}}{\sum \text{Redemptions}}\right) \times 100$ | $37.42\%$ | Non-summer utilization share (`4,784,332` redemptions) |
| **1-Hour Rolling Average ($MA_{1\text{H}}$)** | $\frac{1}{4}\sum_{i=0}^{3} X_{t-i}$ | Dynamic Series | Smooths 15-minute noise into hourly queue velocity |
| **4-Hour Rolling Average ($MA_{4\text{H}}$)** | $\frac{1}{16}\sum_{i=0}^{15} X_{t-i}$ | Dynamic Series | Captures half-shift macro passenger flow waves |

---

## 4. Exploratory Data Analysis (EDA) and Empirical Findings

### 4.1 Peak vs. Off-Peak Demand Windows
| Operational Demand Window | Total Tickets Sold | Total Tickets Redeemed | Net Passenger Movement | Share of Total Redemptions (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Peak Window (10:00–17:59)** | 9,667,124 | 10,155,154 | -488,030 | **79.43%** |
| **Off-Peak Window (Before 10:00 & After 18:00)** | 3,304,927 | 2,630,139 | +674,788 | **20.57%** |
| **Total System** | **12,972,051** | **12,785,293** | **+186,758** | **100.00%** |

**Key Insight:**
- During **Off-Peak hours**, ticket sales exceed redemptions by **+674,788**, reflecting early-morning and late-night online advance purchasing.
- During the **Peak Window (10:00–17:59)**, redemptions exceed concurrent sales by **-488,030** (`10,155,154` redeemed vs. `9,667,124` sold), proving that midday terminal congestion is heavily compounded by passengers redeeming pre-purchased tickets at the gates, peaking at **12:00 noon**.

### 4.2 Day-of-Week and Weekend vs. Weekday Asymmetry
| Day of Week | Day Classification | Total Tickets Sold | Total Tickets Redeemed | Net Passenger Movement | Share of Redemptions (%) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Monday** | Weekday | 1,670,609 | 1,654,352 | +16,257 | 12.94% |
| **Tuesday** | Weekday | 1,331,860 | 1,271,089 | +60,771 | 9.94% |
| **Wednesday** | Weekday | 1,444,624 | 1,383,026 | +61,598 | 10.82% |
| **Thursday** | Weekday | 1,461,639 | 1,379,066 | +82,573 | 10.79% |
| **Friday** | Weekday | 1,784,931 | 1,621,026 | +163,905 | 12.68% |
| **Saturday** | Weekend | 2,727,394 | 2,795,008 | -67,614 | **21.86%** |
| **Sunday** | Weekend | 2,550,994 | 2,681,726 | -130,732 | **20.98%** |
| **Weekday Subtotal** | **5 Days** | **7,693,663** | **7,308,559** | **+385,104** | **57.16%** |
| **Weekend Subtotal** | **2 Days** | **5,278,388** | **5,476,734** | **-198,346** | **42.84%** |

**Key Insight:**
- **Saturday (21.86% / 2,795,008)** and **Sunday (20.98% / 2,681,726)** alone generate **42.84%** of total weekly boardings—more than double the daily volume of **Tuesday (9.94% / 1,271,089)**.
- Every single weekday exhibits positive Net Passenger Movement (`+385,104` total, peaking on **Friday at +163,905** as riders purchase weekend tickets in advance), which subsequently discharges at the turnstiles on **Saturday (-67,614)** and **Sunday (-130,732)**.

### 4.3 Seasonal Comparison and Off-Season Utilization Index
| Calendar Season | Months Covered | Total Tickets Sold | Total Tickets Redeemed | Net Passenger Movement | Share of Redemptions (%) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Spring** | Mar, Apr, May | 1,693,899 | 1,664,773 | +29,126 | 13.02% |
| **Summer** | Jun, Jul, Aug | 8,341,015 | 8,000,961 | +340,054 | **62.58%** |
| **Fall** | Sep, Oct, Nov | 2,498,657 | 2,606,380 | -107,723 | **20.39%** |
| **Winter** | Dec, Jan, Feb | 438,480 | 513,179 | -74,699 | 4.01% |
| **Off-Season Subtotal** | **Spring + Fall + Winter** | **4,631,036** | **4,784,332** | **-153,296** | **37.42% (Index)** |

**Key Insight:**
- While **Summer** dominates with **62.58% (8,000,961)** of redemptions and builds a **+340,054** ticket surplus, **Fall retains 20.39% (2,606,380)** of annual demand and absorbs **-107,723** in delayed ticket redemptions.
- The **37.42% Off-Season Utilization Index** proves that more than one-third of ferry demand occurs outside the traditional June–August summer window.

---

## 5. Role-Based Actionable Recommendations and Target Thresholds

| Stakeholder Role | Operational Challenge | Concrete Action Plan | Quantified Target Threshold |
| :--- | :--- | :--- | :--- |
| **Operations Team** | Midday turnstile bottlenecks (`79.43%` volume in `10:00–17:59`; `12:00` peak) and `3,236` extreme surge intervals (`P99 > 508`). | Link live gate telemetry to the **1-Hour Rolling Redemption Average ($MA_{1\text{H}}$)**. Trigger maximum vessel deployment and open all turnstile lanes whenever $MA_{1\text{H}} > 350\text{ tickets/15-min}$ (`70%` of P99 threshold). | Reduce peak midday terminal queue wait times by **25%–30%** between `11:00` and `15:00`. |
| **Policy Planners** | Severe weekend crowding (`42.84%` of boardings on Sat/Sun) compounded by `-198,346` pre-purchased ticket drawdowns. | Implement mandatory timed-boarding reservation slots for **Saturday and Sunday (10:00–15:00)** paired with a **15% early-bird fare discount** for off-peak departures before `10:00 AM` (currently `20.57%` share). | Shift **10%–12% of peak weekend boardings** (`~600,000` cumulative riders) into the pre-10:00 AM off-peak window. |
| **Management Stakeholders** |Premature fleet step-down after Labor Day despite Fall capturing `20.39% (2.61M)` of redemptions and `-107,723` ticket drawdown. | Maintain peak summer multi-vessel staffing through **September and October**, restricting major vessel dry-dock maintenance exclusively to **Winter (`4.01%` share)** and early **Spring (`13.02%` share)**. | Eliminate Fall capacity shortfalls and improve off-season vessel utilization efficiency by **15%–20%**. |

---

## 6. Conclusion
By integrating 261,538 15-minute operational intervals into a validated analytical pipeline with 1-hour and 4-hour rolling smoothing, percentile outlier auditing, and role-specific decision matrices, this system provides Toronto Government Parks, Forestry & Recreation with an actionable foundation to optimize ferry scheduling, reduce terminal crowding, and improve year-round passenger safety.