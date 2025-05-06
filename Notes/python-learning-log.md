# Python Learning Log

## 2025-04-29
- Practiced list, simple function for list comprehension in `core/01_basics.py`; understood every line.
- Wrote list + function + list-comprehension; clarified correct loop variable usage. 'core/01_basics_drill.py'


## 2025-04-30
- Loaded a timesheet.csv into pandas, inspected dtypes, head(), and summary stats.

## 2025-05-02 (My Birthday!!)
- Loaded timesheet.csv into pandas, getting the info and viewing the top 5 rows with head(), parse 'Total hrs' and convert from string object to float so we can remove data with 0 hours in that column, renamed Name-> Employee_name, and saved to Parquet after pip installing pyarrow

- Added a Pandas cheat sheet with patterns that will be helpful to retaining syntax and steps needed

## 2025-05-03
- Worked with .groupby() for grouping by a certain column just like in sql, .agg() for aggregations (think sum, count, etc.), and then .sortvalues() where we can sort ascending descending
- Added an additional column to the data set to get the percent of the total

## 2025-05-04
- Sorted values by employee_name and Date, added cumulative_hours column by using .groupby() and next used .cumsum() to get the cumulative sum of the values after grouping, queryed a single employee using .query() and saved new parquet
- Set up the Gold Medallion layer

## 2025-05-05
-  Wrapped clean data + agg data into argparse CLI; prints row counts, writes Parquet outputs
-  Debugged ETL script path; now loads via src arg and runs from repo root
- CLI is important because it allows for parameterization, same script works for dev staging and prod with no code edit, its automation friendly, gives a free help screen for self documentation (argparse), a single function that allows for easy unit test with temp files, and we can add logging, retry loops, timing metics in one place.

## 2025-05-06
- Loaded employee_hours Parquet into SQLite(to_sql replace); verified row count with SELECT.