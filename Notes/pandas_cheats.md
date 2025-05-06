# Pandas Patterns

## Load & Inspect
df = pd.read_csv("path.csv", parse_dates=["date_col"])
df.head()
df.info()
df.describe()

## Rename Columns
df = df.rename(columns={"Old Name": "New Name"})

## String to Numeric Function
def parse_func_name_here(x):
    """Input whatever you need to do to parse the data here
    See pandas 02 for examples
    """
df["new_column" = df["raw_string_column"].apply(parse_func_name_here)]

## Filter & Drop
df = df[df["value"] > 0].dropna(subset=["value"])

## Save New Clean Output
df.to_parquet("clean.parquet", index=False)

## Parsing Hours and avoiding NA strings
def parse_hours(hstr):
    """'8 h 44 m' -> 8.73333'"""
    if pd.isna(hstr):
        return pd.NA
    parts = hstr.strip().split() # ['8', 'h', '44', 'm']
    hours = int(parts[0])
    minutes = int(parts[2])

    return hours + minutes / 60
df["hours_worked"] = raw["Total hrs"].apply(parse_hours)

## Running Total per Group
'''python
df = df.sort_values(["key","date"])
df["cumulative_metric"] = = df.groupby("key")["metric".cumsum()

## Basic Pandas CLI with argparse
```python
import argparse, pandas as pd
def main(src, dest):
    df = pd.read_csv(src)
    # ... transforms ...
    df.to_parquet(dest, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", default="data/input.csv")
    parser.add_argument("--dest", default="data/output.parquet")
    args = parser.parse_args()
    main(args.src, args.dest)


| Aspect                  | What we did                                                                    | Why it matters                                              | How to say it in an interview                                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Parameterization**    | Replaced hard‑coded file paths with `--src`, `--out_clean`, `--out_emp` flags. | Same script works for dev, staging, prod—no code edits.     | “I exposed the paths as CLI flags so Ops can point the pipeline at any bucket or date partition without touching the code.”   |
| **Automation‑friendly** | Put the logic in `run_etl()` and called it from `if __name__ == "__main__":`.  | Lets cron, Airflow, or GitHub Actions call it directly.     | “I packaged the ETL as a command‑line tool so we can drop it into an Airflow DAG or CI job with a single bash command.”       |
| **Self‑documentation**  | `argparse` gives a free `--help` screen.                                       | New teammates see valid options instantly; easier hand‑off. | “Running `python etl.py --help` shows all supported flags—no need to dig through code.”                                       |
| **Testability**         | A single function that takes paths → easy to unit‑test with temp files.        | Proves you think about maintainability.                     | “Because the function is pure (src → dest), we can unit‑test it by passing a small sample file and asserting on output rows.” |
| **Resilience hooks**    | Now we can add logging, retry loops, timing metrics in one place.              | Builds toward prod‑ready pipeline.                          | “The CLI wrapper gives us a single entry point to add logging and retries later.”                                             |
