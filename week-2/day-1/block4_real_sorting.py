import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER LIMIT 5000")
    df = cursor.fetch_pandas_all()

    # 1: Sort the DataFrame by one column
    sorted_by_balance = df.sort_values("C_ACCTBAL", ascending=False)
    print("Top 5 by balance:")
    print(sorted_by_balance[["C_CUSTKEY", "C_ACCTBAL"]].head())

    # 2: Sort by multiple columns
    sorted_by_segment_and_balance = df.sort_values(["C_MKTSEGMENT", "C_ACCTBAL"], ascending=[True, False])
    print("\nSorted by segment (asc), then balance (desc):")
    print(sorted_by_segment_and_balance[["C_CUSTKEY", "C_MKTSEGMENT", "C_ACCTBAL"]].head(10))

    # 3: Reset index after sorting
    print("\nOriginal index (first 5):", df.index[:5].tolist())
    print("Sorted index (first 5):", sorted_by_balance.index[:5].tolist())

    reset_sorted = sorted_by_balance.reset_index(drop=True)
    print("\nAfter reset_index(drop=True), index (first 5):", reset_sorted.index[:5].tolist())

    # 4: Sort back to original order using the sort index
    back_to_original = sorted_by_balance.sort_index()
    print("\nBack to original order (first 5):")
    print(back_to_original[["C_CUSTKEY", "C_ACCTBAL"]].head())
    
finally:
    conn.close()