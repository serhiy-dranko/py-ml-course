import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()

    # Raw source data
    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_ORDERS")
    df_orders = cursor.fetch_pandas_all()

    # dbt's fact table (already has TOTAL_AMOUNT computed)
    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.FCT_ORDERS")
    df_fct = cursor.fetch_pandas_all()

    # Reproduce a mart-style metric: total revenue and order count per customer
    my_summary = df_fct.groupby("CUSTOMER_ID").agg(
        total_revenue=("TOTAL_AMOUNT", "sum"),
        order_count=("ORDER_ID", "nunique"),
        avg_order_value=("TOTAL_AMOUNT", "mean"),
    ).reset_index()

    print("=== My reproduced summary ===")
    print(my_summary.head(10))
    print("\nShape:", my_summary.shape)

    # Check for a real dbt mart model with a similar customer-level summary
    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.FCT_ORDERS")
    df_dim = cursor.fetch_pandas_all()

    print("=== DIM_CUSTOMERS structure ===")
    print("Shape:", df_dim.shape)
    print("Columns:", df_dim.columns.tolist())
    print(df_dim.head(10))

finally:
    conn.close()