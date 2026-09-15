import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection
import numpy as np

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_ORDERS")
    df = cursor.fetch_pandas_all()

    print("=== Original ===")
    print(df.head())
    print("\nLength before any changes:", len(df))

    df.loc[df.sample(5, random_state=1).index, "ORDER_DATE"] = None
    df.loc[df.sample(3, random_state=2).index, "STATUS"] = None

    print("\n=== After introducing artificial missing values ===")
    print(df.isna().sum())

    # 1. DROP
    df_dropped = df.dropna(subset=["ORDER_DATE"])
    print("\nLength after dropna(subset=['ORDER_DATE']):", len(df_dropped))

    # 2. FILL
    df["STATUS"] = df["STATUS"].fillna("unknown")
    print("\nAfter fillna('unknown') for STATUS:")
    print(df["STATUS"].value_counts(dropna=False))

    # 3. FLAG-AND-KEEP — ORDER_DATE
    df["order_date_is_missing"] = df["ORDER_DATE"].isna()
    print("\nWith order_date_is_missing flag (ORDER_DATE itself untouched):")
    print(df[["ID", "ORDER_DATE", "order_date_is_missing"]].head(10))

finally:
    conn.close()