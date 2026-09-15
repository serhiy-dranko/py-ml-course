import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_ORDERS")
    df = cursor.fetch_pandas_all()

    print("=== Shape ===")
    print(df.shape)

    print("\n=== NaN count per column ===")
    print(df.isna().sum())

    print("\n=== NaN percentage per column ===")
    print(df.isna().mean() * 100)

    for col in df.select_dtypes(include="object").columns:
        print(f"\n=== value_counts for {col} ===")
        print(df[col].value_counts(dropna=False).head(10))
        
finally:
    conn.close()