# Real-Time Ferry Ticket Sales & Redemption Analytics for Toronto Island Park

**Author:** Etuka Leela Prasad  
**Organization:** Unified Mentor Data Analytics Internship  
**Stakeholder Partner:** Toronto Government Parks, Forestry & Recreation  

## 1. Project Overview
This project delivers an end-to-end operational intelligence dashboard and empirical research study for the **Jack Layton Ferry Terminal** serving Centre Island, Hanlan's Point, and Ward's Island. By analyzing **261,538 15-minute intervals** recorded between **May 1, 2015 and December 21, 2025**, the system tracks **12,972,051 tickets sold** and **12,785,293 tickets redeemed** to optimize vessel scheduling, terminal gate staffing, and seasonal fleet maintenance.

## 2. Validated Key Performance Indicators (KPIs) & Mathematical Definitions
| KPI / Metric Name | Mathematical Formula | Verified Baseline (2015–2025) | Operational Meaning |
| :--- | :--- | :--- | :--- |
| **Tickets Sold per Hour** | `Sum(Sales Count) / (Intervals / 4)` | **198.40 / hr** (`12,972,051` sold) | Average hourly ticket purchase velocity across online and terminal kiosks |
| **Tickets Redeemed per Hour** | `Sum(Redemption Count) / (Intervals / 4)` | **195.54 / hr** (`12,785,293` redeemed) | Physical passenger boarding throughput at terminal turnstiles (`98.56%` redemption rate) |
| **Net Passenger Movement** | `Sum(Sales Count) - Sum(Redemption Count)` | **+186,758** (`+2.86 net / hr`) | Advance purchase buffer (`+385,104` on Weekdays vs. `-198,346` drawdown on Weekends) |
| **Peak Demand Windows** | `(Redemptions in 10:00–17:59 / Total) * 100` | **79.43% Share** (`12:00` Peak Hour) | `10,155,154` boardings occur between `10:00` and `17:59` (`3,236` top 1% surge intervals) |
| **Off-Season Utilization Index** | `((Spring + Fall + Winter Redemptions) / Total) * 100` | **37.42% Non-Summer** (`4,784,332`) | Summer captures `62.58%` (`8,000,961`), Fall `20.39%`, Spring `13.02%`, and Winter `4.01%` |

## 3. Streamlit Web Application Architecture (5 Core Modules)
- **Role-Based Views & Interactive Date/Time Filters:** Supports **Operations Team**, **Policy Planners**, and **Management Stakeholders** with dynamic filters for Calendar Date Range (`2015-05-01` to `2025-12-21`), Season, Day Type (Weekday vs. Weekend), and Operating Hour (`00:00–23:00`).
- **Top KPI Scorecards & Formula Reference Expander:** Complete, non-truncated KPI metrics paired with an expandable mathematical formula and baseline validation table.
- **Tab 1 — Hourly & Daily Demand Trends:** Average 15-minute sales vs. redemptions by hour, cumulative day-of-week comparisons, and a validated Day-of-Week summary table.
- **Tab 2 — Peak vs. Off-Peak & Net Flow:** Peak (`10:00–17:59`) vs. Off-Peak volume comparison, hourly net passenger movement (`Sales - Redemptions`), and a Weekday/Weekend cross-validation table.
- **Tab 3 — Seasonal & Multi-Year Utilization:** Seasonal volume comparisons, annual trajectory (`2015–2025`), and a Season x Hour turnstile boarding density heatmap.
- **Tab 4 — Rolling Averages, Distributions & Outliers:** Interactive `1-Hour (4-interval)` and `4-Hour (16-interval)` rolling average inspector, statistical distribution summary (`Mean`, `Std`, `Median`, `P75`, `P90`, `P95`, `P99`, `Max`), box-plot spread, and top 25 extreme surge outlier audit (`P99 Sales > 458`, `P99 Redemptions > 508`).
- **Tab 5 — Executive Summary & Role Recommendations:** Built-in empirical findings, role-specific quantified recommendations, and a Seasonal Operational Decision Matrix.

## 4. Repository Structure
- `Toronto Island Ferry Tickets.csv`: Raw 15-minute interval dataset (`261,538` records).
- `analysis.py`: Data ingestion, cleaning, feature engineering, rolling averages, outlier detection, and CLI validation script.
- `app.py`: Production 5-tab Streamlit web application.
- `RESEARCH_PAPER.md`: Full technical research paper with methodology, formulas, EDA tables, and recommendations.
- `EXECUTIVE_SUMMARY.md`: Executive policy and operational briefing for Toronto Government Parks, Forestry & Recreation.
- `requirements.txt`: Python package dependencies for cloud deployment.

## 5. Local Execution
```bash
pip install -r requirements.txt
python analysis.py
python -m streamlit run app.py