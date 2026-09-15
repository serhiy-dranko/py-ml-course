import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_PAYMENTS")
    df = cursor.fetch_pandas_all()

    print("=== Shape ===")
    print(df.shape)

    print("\n=== Dtypes ===")
    print(df.dtypes)

    print("\n=== Head ===")
    print(df.head())

    print("\n=== Random sample ===")
    print(df.sample(10))

finally:
    conn.close()