import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER LIMIT 5000")
    df = cursor.fetch_pandas_all()

    # 2: single-column, single-stat groupby
    segment_totals = df.groupby("C_MKTSEGMENT")["C_ACCTBAL"].sum()
    print("=== Total balance by segment ===")
    print(segment_totals)

    # 3: the same, sorted descending
    segment_totals_sorted = segment_totals.sort_values(ascending=False)
    print("\n=== Sorted descending ===")
    print(segment_totals_sorted)

    # 4: .size() vs .count()
    print("\n=== .size() (all rows, including NaN) ===")
    print(df.groupby("C_MKTSEGMENT")["C_ACCTBAL"].size())

    print("\n=== .count() (only non-NaN values) ===")
    print(df.groupby("C_MKTSEGMENT")["C_ACCTBAL"].count())

finally:
    conn.close()