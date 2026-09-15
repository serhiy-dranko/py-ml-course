import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_CUSTOMERS")
    df_customers = cursor.fetch_pandas_all()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_ORDERS")
    df_orders = cursor.fetch_pandas_all()

    print("Customers columns:", df_customers.columns.tolist())
    print("Orders columns:", df_orders.columns.tolist())
    print("\nlen(customers):", len(df_customers))
    print("len(orders):", len(df_orders))

    # INNER merge
    inner_merged = df_customers.merge(
        df_orders,
        left_on="ID",
        right_on="USER_ID",
        how="inner",
    )
    print("\n=== INNER merge ===")
    print("len(merged):", len(inner_merged))
    print(inner_merged.head())

    # LEFT merge
    left_merged = df_customers.merge(
        df_orders,
        left_on="ID",
        right_on="USER_ID",
        how="left",
    )
    print("\n=== LEFT merge ===")
    print("len(merged):", len(left_merged))

    # OUTER merge
    outer_merged = df_customers.merge(
        df_orders,
        left_on="ID",
        right_on="USER_ID",
        how="outer",
    )
    print("\n=== OUTER merge ===")
    print("len(merged):", len(outer_merged))

    print("\n=== SUMMARY ===")
    print(f"Inner: {len(inner_merged)}, Left: {len(left_merged)}, Outer: {len(outer_merged)}")

finally:
    conn.close()