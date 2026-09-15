import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER LIMIT 5000")
    df = cursor.fetch_pandas_all()

    # 1: single-condition filter
    high_balance = df[df["C_ACCTBAL"] > 1000]
    print("High balance head:", high_balance.head)

    # 2: multi-condition filter
    mask = (df["C_ACCTBAL"] > 1000) & (df["C_MKTSEGMENT"] == "BUILDING")
    high_balance_building = df[mask]
    print("High balance + BUILDING shape:", high_balance_building.head)

    # 3: .query()
    high_balance_building_query = df.query("C_ACCTBAL > 1000 and C_MKTSEGMENT == 'BUILDING'")
    print("Results identical?", high_balance_building.equals(high_balance_building_query))

    # 4: .isin()
    target_segments = ["HOUSEHOLD", "AUTOMOBILE"]
    segment_filter = df[df["C_MKTSEGMENT"].isin(target_segments)]
    print(segment_filter.head)

    # 4: .str.contains()
    address_filter = df[df["C_ADDRESS"].str.contains("ave")]
    print(address_filter.head)

    # 5: combine filtering and column selection
    result = df.loc[mask, ["C_CUSTKEY", "C_NAME", "C_ACCTBAL", "C_MKTSEGMENT"]]
    print("\nFiltered + selected columns:")
    print(result.head())

finally:
    conn.close()