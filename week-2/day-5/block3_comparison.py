import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_CUSTOMERS")
    df_raw_customers = cursor.fetch_pandas_all()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_ORDERS")
    df_raw_orders = cursor.fetch_pandas_all()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.STG_CUSTOMERS")
    df_staging_customers = cursor.fetch_pandas_all()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.STG_ORDERS")
    df_staging_orders = cursor.fetch_pandas_all()

    print("--- Shape ---")
    print(f"RAW_CUSTOMERS:   {df_raw_customers.shape}")
    print(f"STG_CUSTOMERS:   {df_staging_customers.shape}")
    print(f"RAW_ORDERS:      {df_raw_orders.shape}")
    print(f"STG_ORDERS:      {df_staging_orders.shape}")

    print("\n--- Dtypes: customers ---")
    print("RAW:\n", df_raw_customers.dtypes)
    print("\nSTAGING:\n", df_staging_customers.dtypes)

    print("\n--- Dtypes: orders ---")
    print("RAW:\n", df_raw_orders.dtypes)
    print("\nSTAGING:\n", df_staging_orders.dtypes)

    print("\n--- Null counts ---")
    print("RAW_CUSTOMERS nulls:\n", df_raw_customers.isna().sum())
    print("\nSTG_CUSTOMERS nulls:\n", df_staging_customers.isna().sum())
    print("\nRAW_ORDERS nulls:\n", df_raw_orders.isna().sum())
    print("\nSTG_ORDERS nulls:\n", df_staging_orders.isna().sum())

    print("\n--- Duplicate keys ---")
    print("RAW_ORDERS duplicated ID:", df_raw_orders.duplicated(subset=["ID"]).sum())
    print("STG_ORDERS duplicated (first col):",
          df_staging_orders.duplicated(subset=[df_staging_orders.columns[0]]).sum())

    print("\n--- Cardinality: STATUS ---")
    print("RAW_ORDERS STATUS unique:", df_raw_orders["STATUS"].nunique())
    if "STATUS" in df_staging_orders.columns:
        print("STG_ORDERS STATUS unique:", df_staging_orders["STATUS"].nunique())
    else:
        print("STG_ORDERS has no STATUS column — columns are:", df_staging_orders.columns.tolist())

    print("\n--- Column names ---")
    print("RAW_ORDERS columns:", df_raw_orders.columns.tolist())
    print("STG_ORDERS columns:", df_staging_orders.columns.tolist())
    print("RAW_CUSTOMERS columns:", df_raw_customers.columns.tolist())
    print("STG_CUSTOMERS columns:", df_staging_customers.columns.tolist())

finally:
    conn.close()