import pandas as pd
import numpy as np
from pathlib import Path

DATA_FILE = "Toronto Island Ferry Tickets.csv"
DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SEASON_ORDER = ["Spring", "Summer", "Fall", "Winter"]

def get_season(month: int) -> str:
    if month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    elif month in [9, 10, 11]:
        return "Fall"
    else:
        return "Winter"

def resolve_csv_path(file_path: str = DATA_FILE) -> Path:
    path = Path(file_path)
    if path.exists():
        return path
    # Fallback: automatically find any CSV in the current project folder
    csv_files = list(Path(".").glob("*.csv"))
    if csv_files:
        return csv_files[0]
    raise FileNotFoundError(f"Could not find '{file_path}' or any .csv file in {Path('.').resolve()}")

def load_and_analyze_ferry_data(file_path: str = DATA_FILE) -> pd.DataFrame:
    path = resolve_csv_path(file_path)

    # 1. Data Ingestion
    df = pd.read_csv(path, low_memory=False)
    df.columns = df.columns.astype(str).str.strip()

    # Dynamically identify Timestamp, Sales Count, and Redemption Count columns
    time_col = None
    sales_col = None
    redemp_col = None
    id_col = None

    for col in df.columns:
        c_low = col.lower()
        if c_low in ["_id", "id"] and id_col is None:
            id_col = col
        elif ("time" in c_low or "date" in c_low) and time_col is None:
            time_col = col
        elif "sale" in c_low and sales_col is None:
            sales_col = col
        elif "redemp" in c_low and redemp_col is None:
            redemp_col = col

    # Fallback by column position if headers have custom names
    if time_col is None or sales_col is None or redemp_col is None:
        cols = list(df.columns)
        if len(cols) >= 4:
            id_col = id_col or cols[0]
            time_col = time_col or cols[1]
            # Check which of cols[2], cols[3] is sales vs redemption
            if redemp_col == cols[2]:
                sales_col = sales_col or cols[3]
            else:
                sales_col = sales_col or cols[2]
                redemp_col = redemp_col or cols[3]
        elif len(cols) == 3:
            time_col = time_col or cols[0]
            sales_col = sales_col or cols[1]
            redemp_col = redemp_col or cols[2]

    rename_dict = {}
    if id_col:
        rename_dict[id_col] = "_id"
    if time_col:
        rename_dict[time_col] = "Timestamp"
    if sales_col:
        rename_dict[sales_col] = "Sales Count"
    if redemp_col:
        rename_dict[redemp_col] = "Redemption Count"

    df = df.rename(columns=rename_dict)

    # Convert Timestamp to datetime and sort chronologically
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df = df.dropna(subset=["Timestamp"]).sort_values("Timestamp").reset_index(drop=True)

    # 2. Data Cleaning & Consistency Checks
    df["Sales Count"] = pd.to_numeric(df["Sales Count"], errors="coerce").fillna(0)
    df["Redemption Count"] = pd.to_numeric(df["Redemption Count"], errors="coerce").fillna(0)

    df["Sales Count"] = df["Sales Count"].clip(lower=0).astype(int)
    df["Redemption Count"] = df["Redemption Count"].clip(lower=0).astype(int)

    # 3. Feature Engineering
    df["Date"] = df["Timestamp"].dt.date
    df["Year"] = df["Timestamp"].dt.year
    df["Month"] = df["Timestamp"].dt.month
    df["MonthName"] = df["Timestamp"].dt.strftime("%b")
    df["YearMonth"] = df["Timestamp"].dt.to_period("M").astype(str)
    df["Hour"] = df["Timestamp"].dt.hour
    df["DayOfWeek"] = df["Timestamp"].dt.day_name()
    df["DayType"] = np.where(df["Timestamp"].dt.dayofweek >= 5, "Weekend", "Weekday")
    df["Season"] = df["Month"].apply(get_season)

    # Core KPI: Net Passenger Movement (Sales - Redemptions)
    df["Net Passenger Movement"] = df["Sales Count"] - df["Redemption Count"]

    # Peak vs Off-Peak Classification (10:00 to 17:59 as Peak Operational Hours)
    df["DemandWindow"] = np.where(
        df["Hour"].between(10, 17),
        "Peak Window (10:00-17:59)",
        "Off-Peak Window"
    )

    # Rolling Averages (15-min intervals: 4 intervals = 1-Hour, 16 intervals = 4-Hour)
    df["Sales_Rolling_1H"] = df["Sales Count"].rolling(window=4, min_periods=1).mean().round(2)
    df["Redemption_Rolling_1H"] = df["Redemption Count"].rolling(window=4, min_periods=1).mean().round(2)
    df["Sales_Rolling_4H"] = df["Sales Count"].rolling(window=16, min_periods=1).mean().round(2)
    df["Redemption_Rolling_4H"] = df["Redemption Count"].rolling(window=16, min_periods=1).mean().round(2)

    # Statistical Outlier Detection (99th Percentile Threshold)
    sales_p99 = df["Sales Count"].quantile(0.99)
    redemp_p99 = df["Redemption Count"].quantile(0.99)
    df["Is_Outlier"] = (df["Sales Count"] > sales_p99) | (df["Redemption Count"] > redemp_p99)

    return df

if __name__ == "__main__":
    df = load_and_analyze_ferry_data()
    total_intervals = len(df)
    total_hours_recorded = total_intervals / 4.0 if total_intervals > 0 else 1.0

    total_sales = int(df["Sales Count"].sum())
    total_redemptions = int(df["Redemption Count"].sum())
    net_movement = int(df["Net Passenger Movement"].sum())

    tickets_sold_per_hour = total_sales / total_hours_recorded
    tickets_redeemed_per_hour = total_redemptions / total_hours_recorded

    hourly_totals = df.groupby("Hour")[["Sales Count", "Redemption Count"]].sum()
    peak_sales_hour = int(hourly_totals["Sales Count"].idxmax())
    peak_redemp_hour = int(hourly_totals["Redemption Count"].idxmax())

    season_redemp = df.groupby("Season")["Redemption Count"].sum().reindex(SEASON_ORDER, fill_value=0)
    off_season_redemp = int(season_redemp.loc[["Spring", "Fall", "Winter"]].sum())
    off_season_utilization_pct = (off_season_redemp / total_redemptions) * 100 if total_redemptions > 0 else 0.0

    sales_p99_val = df["Sales Count"].quantile(0.99)
    redemp_p99_val = df["Redemption Count"].quantile(0.99)
    outlier_count = int(df["Is_Outlier"].sum())

    print("=== TORONTO ISLAND FERRY VALIDATED ANALYTICAL SUMMARY ===")
    print(f"Total 15-Min Intervals: {total_intervals:,}")
    print(f"Date Range: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
    print(f"Total Tickets Sold: {total_sales:,}")
    print(f"Total Tickets Redeemed: {total_redemptions:,}")
    print(f"Cumulative Net Passenger Movement (Sales - Redemptions): {net_movement:,}")
    print(f"Avg Tickets Sold per Hour: {tickets_sold_per_hour:.2f}")
    print(f"Avg Tickets Redeemed per Hour: {tickets_redeemed_per_hour:.2f}")
    print(f"Peak Sales Hour: {peak_sales_hour:02d}:00 | Peak Redemption Hour: {peak_redemp_hour:02d}:00")
    print(f"Off-Season Utilization Index (Non-Summer Share): {off_season_utilization_pct:.2f}%")
    print(f"99th Percentile Outlier Thresholds -> Sales: {sales_p99_val:.0f}, Redemptions: {redemp_p99_val:.0f}")
    print(f"Total High-Volume Outlier Intervals (Top 1%): {outlier_count:,}")

    print("\n--- Seasonal Breakdown (Sales & Redemptions) ---")
    season_summary = df.groupby("Season")[["Sales Count", "Redemption Count", "Net Passenger Movement"]].sum().reindex(SEASON_ORDER, fill_value=0)
    season_summary["Redemption Share (%)"] = ((season_summary["Redemption Count"] / total_redemptions) * 100).round(2)
    print(season_summary.to_string())

    print("\n--- Day Type Breakdown (Weekday vs Weekend) ---")
    daytype_summary = df.groupby("DayType")[["Sales Count", "Redemption Count", "Net Passenger Movement"]].sum()
    daytype_summary["Redemption Share (%)"] = ((daytype_summary["Redemption Count"] / total_redemptions) * 100).round(2)
    print(daytype_summary.to_string())

    print("\n--- Peak vs Off-Peak Window Breakdown ---")
    window_summary = df.groupby("DemandWindow")[["Sales Count", "Redemption Count", "Net Passenger Movement"]].sum()
    window_summary["Redemption Share (%)"] = ((window_summary["Redemption Count"] / total_redemptions) * 100).round(2)
    print(window_summary.to_string())

    print("\n--- Day of Week Breakdown ---")
    dow_summary = df.groupby("DayOfWeek")[["Sales Count", "Redemption Count", "Net Passenger Movement"]].sum().reindex(DAY_ORDER, fill_value=0)
    dow_summary["Redemption Share (%)"] = ((dow_summary["Redemption Count"] / total_redemptions) * 100).round(2)
    print(dow_summary.to_string())