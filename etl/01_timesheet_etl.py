# Updated on 5/22/2025
import logging # NEW
import time # NEW
from pathlib import Path # NEW


import argparse
import pandas as pd

# -----parser-----
# Changed 5/22/2025

# def parse_hours(hstr):
#     if pd.isna(hstr):
#         return pd.NA
#     parts = hstr.strip().split()
#     hours = float(parts[0])
#     minutes = float(parts[2])
#     return hours + (minutes / 60)

def run_etl(src, out_clean, out_emp):

    import os
    print("Loading", os.path.abspath(src))

    # 1. Load
    raw = pd.read_csv(src, parse_dates=["Date"])

    # 2. Transform
    raw["hours_worked"] = raw["Total hrs"].apply(parse_hours)
    df = (
        raw.rename(columns={"Name": "employee_name"})
            .loc[lambda d: d["hours_worked"] > 0]
            .dropna(subset=["hours_worked"])
            .sort_values(["employee_name", "Date"])
    )
    
    # 3. Save Clean
    df.to_parquet(out_clean, index=False)

    # 4. Aggregate
    emp_hours = (
        df.groupby("employee_name", as_index=False)
        .agg(total_hours=("hours_worked", "sum"))
        .sort_values("total_hours", ascending=False)
    )

    # 5. Save Aggregation
    emp_hours.to_parquet(out_emp, index=False)

    print(f"Clean rows {len(df):,} | Employees: {len(emp_hours):,}")
    print(f"Saved -> {out_clean} and {out_emp}")

# Changed 5/22/2025
# if __name__=="__main__":
#     parser = argparse.ArgumentParser(description="Timesheet ETL pipeline")
#     parser.add_argument("--src", default="data/timesheet.csv")
#     parser.add_argument("--out_clean", default="data/timesheet_clean.parquet")
#     parser.add_argument("--out_emp", default="data/employee_hours.parquet")
#     args = parser.parse_args()

#     run_etl(args.src, args.out_clean, args.out_emp)

# 5. Set up basic logging - 5/22/2025

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "timesheet_etl.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# 6. Parse CLI arguments (drop into main()) - 5/22/2025

def parse_args():
    parser = argparse.ArgumentParser(description="Timesheet ETL pipeline")
    parser.add_argument("--src", default="data/timesheet.csv")
    parser.add_argument("--out_clean", default="data/timesheet_clean.parquet")
    parser.add_argument("--out_emp", default="data/employee_hours.parquet")
    return parser.parse_args()

# 7. Main wrapper with retries - 5/22/2025

def main():
    args = parse_args()
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"ETL attempt {attempt} started")
            run_etl(args.src, args.out_clean, args.out_emp)
            logging.info("ETL completed Successfully")
            break # Success exit loop
        except Exception as e:
            logging.error(f"ETL attempt {attempt} failed {e}", exc_info=True)
            if attempt == max_retries:
                logging.critical(f"ETL failed after max retries, exiting with error")
                raise
            logging.info("Sleeping 60s before retry...")
            time.sleep(60)

if __name__ == "__main__":
    main()