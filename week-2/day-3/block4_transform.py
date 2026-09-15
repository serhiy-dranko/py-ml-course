import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection
import time

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER LIMIT 5000")
    df = cursor.fetch_pandas_all()

    print("Rows before:", len(df))

    # 1: transform() percentage of segment total
    df["pct_of_segment_total"] = df["C_ACCTBAL"] / df.groupby("C_MKTSEGMENT")["C_ACCTBAL"].transform("sum")

    print("\n=== With pct_of_segment_total ===")
    print(df[["C_CUSTKEY", "C_MKTSEGMENT", "C_ACCTBAL", "pct_of_segment_total"]].head(10))

    # 2: confirmation — number of rows unchanged
    print("\nRows after transform():", len(df))

    # 3: same result via groupby + merge
    start_transform = time.perf_counter()
    df["pct_via_transform"] = df["C_ACCTBAL"] / df.groupby("C_MKTSEGMENT")["C_ACCTBAL"].transform("sum")
    end_transform = time.perf_counter()

    start_merge = time.perf_counter()
    segment_totals = df.groupby("C_MKTSEGMENT")["C_ACCTBAL"].sum().reset_index()
    segment_totals = segment_totals.rename(columns={"C_ACCTBAL": "segment_total"})
    df_merged = df.merge(segment_totals, on="C_MKTSEGMENT", how="left")
    df_merged["pct_via_merge"] = df_merged["C_ACCTBAL"] / df_merged["segment_total"]
    end_merge = time.perf_counter()

    print(f"\ntransform() time: {end_transform - start_transform:.6f} seconds")
    print(f"groupby+merge time: {end_merge - start_merge:.6f} seconds")

    # Check — are the results identical?
    print("\nResults match?", (df["pct_via_transform"].round(10) == df_merged["pct_via_merge"].round(10)).all())

finally:
    conn.close()

## My rule: reach for transform() whenever the same group-level statistic needs to be attached back onto every original row for further row-level calculation (percentages, ratios, deviations from group mean). 
## Reach for groupby-then-merge only when the group-level result needs additional processing of its own before joining back, or when joining onto a different table than the one the groupby came from.