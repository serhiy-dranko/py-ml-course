import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER LIMIT 5000")
    df = cursor.fetch_pandas_all()

    # 1: groupby on two columns
    grouped = df.groupby(["C_MKTSEGMENT", "C_NATIONKEY"])["C_ACCTBAL"].sum()
    print("=== Multi-column groupby (MultiIndex) ===")
    print(grouped.head(10))
    print("\nIndex type:", type(grouped.index))

    # 2: reset_index() — flat, mergeable format
    flat = grouped.reset_index()
    print("\n=== After reset_index() — flat columns ===")
    print(flat.head(10))
    print("\nColumns:", flat.columns.tolist())

    # 3: un   stack() — wide, pivot-similar format
    wide = grouped.unstack()
    print("\n=== After unstack() — wide/pivoted format ===")
    print(wide.head())
    print("\nShape:", wide.shape)

finally:
    conn.close()