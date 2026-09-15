import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_PAYMENTS")
    df = cursor.fetch_pandas_all()

    # Point 1: correlation matrix
    print("=== Correlation matrix (numeric columns) ===")
    print(df.corr(numeric_only=True))

    # Point 2: does AMOUNT distribution differ by PAYMENT_METHOD?
    print("\n=== AMOUNT distribution by PAYMENT_METHOD ===")
    print(df.groupby("PAYMENT_METHOD")["AMOUNT"].describe())

    # Point 3: low-correlation pair for scatter plot
    print("\n=== Low-correlation pair ===")
    print("ORDER_ID vs AMOUNT")
    print(
        df["ORDER_ID"].corr(df["AMOUNT"])
    )
    
finally:
    conn.close()