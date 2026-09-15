import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_PAYMENTS")
    df = cursor.fetch_pandas_all()

    # Missingness check
    print("=== NaN count ===")
    print(df.isna().sum())

    print("\n=== NaN percentage ===")
    print(df.isna().mean() * 100)

    # Fully duplicate rows
    print("\n=== Fully duplicate rows ===")
    print(df.duplicated().sum())

    # Duplicate ID (primary key) check
    print("\n=== Duplicate ID (primary key) check ===")
    print(df.duplicated(subset=["ID"]).sum())

    # Duplicate Order-ID check
    print("\n=== Duplicate Order-ID check ===")
    print(df.duplicated(subset=["ORDER_ID"]).sum())

    # Cardinality check for each column
    print("\n=== Cardinality per column ===")
    for col in df.columns:
        print(f"{col}: {df[col].nunique()} unique values out of {len(df)} rows")

    # Zero-amount payments its worth a closer look
    print("\n=== Zero-amount payments ===")
    zero_payments = df[df["AMOUNT"] == 0]
    print(zero_payments)

finally:
    conn.close()