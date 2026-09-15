import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_PAYMENTS")
    df = cursor.fetch_pandas_all()

    # 1: describe() for numeric columns and categorical columns
    print("=== Numeric describe() ===")
    print(df.describe())

    print("\n=== Categorical describe() ===")
    print(df.describe(include="object"))

    # 3: check unique count for categorical column
    print("\n=== PAYMENT_METHOD unique values ===")
    print(df["PAYMENT_METHOD"].nunique())
    print(df["PAYMENT_METHOD"].value_counts())

    ## aditional check
    print("\n=== ORDER_ID duplicate check ===")
    print("Total rows:", len(df))
    print("Unique ORDER_ID values:", df["ORDER_ID"].nunique())

finally:
    conn.close()

## The most surprising finding: row count (113) doesn't match unique ORDER_ID count (99), meaning ~14 orders have multiple payment records. 
## One row here represents a single payment transaction, not a single order. This contradicts an assumption I might have made from the table("raw payments" like it maps 1:1 to orders). 
## This also confirms the earlier min: 0.0 for AMOUNT is plausible in a payments.