import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_ORDERS")
    df_orders = cursor.fetch_pandas_all()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.FCT_ORDERS")
    df_fct_orders = cursor.fetch_pandas_all()

    print("=== FCT_ORDERS structure ===")
    print("Shape:", df_fct_orders.shape)
    print("Columns:", df_fct_orders.columns.tolist())
    print(df_fct_orders.head())

    print("\n=== Our RAW_ORDERS for comparison ===")
    print("Shape:", df_orders.shape)
    print("Columns:", df_orders.columns.tolist())

finally:
    conn.close()