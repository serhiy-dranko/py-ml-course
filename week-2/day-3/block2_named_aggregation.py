import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER LIMIT 5000")
    df = cursor.fetch_pandas_all()

    # 1: named aggregation — 3+ metrics, 2+ different columns
    summary = df.groupby("C_MKTSEGMENT").agg(
        total_balance=("C_ACCTBAL", "sum"),
        avg_balance=("C_ACCTBAL", "mean"),
        distinct_nations=("C_NATIONKEY", "nunique"),
        customer_count=("C_CUSTKEY", "count"),
    )
    print("=== Named aggregation summary ===")
    print(summary)

    # 2: nunique() vs count() on "ID-like" column
    print("\n=== nunique() vs count() on C_CUSTKEY ===")
    print("Total rows:", len(df))
    print("count():", df["C_CUSTKEY"].count())
    print("nunique():", df["C_CUSTKEY"].nunique())

finally:
    conn.close()