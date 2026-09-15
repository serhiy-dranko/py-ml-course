import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.STG_CUSTOMERS")
    df_staging_customers = cursor.fetch_pandas_all()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.STG_ORDERS")
    df_staging_orders = cursor.fetch_pandas_all()

    print("=== STG_CUSTOMERS ===")
    print(df_staging_customers.shape)
    print(df_staging_customers.head())

    print("\n=== STG_ORDERS ===")
    print(df_staging_orders.shape)
    print(df_staging_orders.head())

finally:
    conn.close()