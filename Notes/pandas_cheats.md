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