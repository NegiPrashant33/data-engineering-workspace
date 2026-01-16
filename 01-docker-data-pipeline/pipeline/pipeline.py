import sys
import pandas as pd

# First argument is always going to be file name
print("arguments", sys.argv)
month = int(sys.argv[1])

print(f"Running pipeline for day {month}")

df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df["month"] = month
print(df.head())

df.to_parquet(f"output_day_{sys.argv[1]}.parquet")