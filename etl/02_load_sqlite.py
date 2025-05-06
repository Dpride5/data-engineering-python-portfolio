import sqlite3
import pandas as pd
import argparse
import os

def load_to_sqlite(parquet_path, db_path="data/timesheet.db", table="employee_hours"):
    """Read a Parquet file and write/replace a table in SQLite"""
    print("Reading :", os.path.abspath(parquet_path))
    df = pd.read_parquet(parquet_path)

    conn = sqlite3.connect(db_path)
    df.to_sql(table, conn, if_exists="replace", index=False)

    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    conn.close()

    print(f"Loaded {count:,} rows into '{table}' inside {db_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load Parquet into SQLite")
    parser.add_argument("--parquet", default="data/employee_hours.parquet")
    parser.add_argument("--db",      default="data/timesheet.db")
    parser.add_argument("--table",  default="employee_hours")
    args = parser.parse_args()

    load_to_sqlite(args.parquet, args.db, args.table)