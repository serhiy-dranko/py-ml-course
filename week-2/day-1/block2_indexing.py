import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER LIMIT 5000")
    df = cursor.fetch_pandas_all()

    print(df.index)

    # 1 .iloc
    first_10_iloc = df.iloc[0:10]
    print("\n--- .iloc[0:10] ---")
    print(first_10_iloc[["C_CUSTKEY", "C_NAME"]])

    # 2 .loc
    first_10_loc = df.loc[0:9]
    print("\n--- .loc[0:9] ---")
    print(first_10_loc[["C_CUSTKEY", "C_NAME"]])

    # .iloc uses POSITION it always works the same way regardless of what the index labels actually are.
    # .loc uses LABELS — it looks for index values that literally match what you give it. df.loc[0:9] means "give me all rows whose index label is between 0 and 9, inclusive"

    # 3 Set C_CUSTKEY as index
    df_indexed = df.set_index("C_CUSTKEY")
    print("\n--- New index ---")
    print(df_indexed.index)

    specific_customer = df_indexed.loc[60005]
    print("\n--- Customer 60005 ---")
    print(specific_customer)

    # 4 Setting With Copy Warning
    west_segment = df[df["C_MKTSEGMENT"] == "BUILDING"]
    west_segment["C_ACCTBAL"] = 0   

    print("\nDid original df change?")
    print(df[df["C_MKTSEGMENT"] == "BUILDING"][["C_CUSTKEY", "C_ACCTBAL"]].head())

    # correct
    df.loc[df["C_MKTSEGMENT"] == "BUILDING", "C_ACCTBAL"] = 0
    print("\nAfter correct .loc assignment:")
    print(df[df["C_MKTSEGMENT"] == "BUILDING"][["C_CUSTKEY", "C_ACCTBAL"]].head())

finally:
    conn.close()