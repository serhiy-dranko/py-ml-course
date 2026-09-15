import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection
import pandas as pd


def clean_and_merge(df_primary: pd.DataFrame, df_secondary: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans RAW_CUSTOMERS (df_primary) and RAW_ORDERS (df_secondary),
    then merges them into one DataFrame: one row per customer-order pair,
    plus customers with zero orders (left join).
    Reused directly from Day 2.
    """
    df_primary = df_primary.rename(columns={"ID": "CUSTOMER_ID"})

    before_drop = len(df_secondary)
    df_secondary = df_secondary.dropna(subset=["ORDER_DATE"])
    dropped_count = before_drop - len(df_secondary)
    if dropped_count > 0:
        print(f"Dropped {dropped_count} orders with missing ORDER_DATE.")

    df_secondary["STATUS"] = df_secondary["STATUS"].fillna("unknown")

    try:
        merged = df_primary.merge(
            df_secondary,
            how="left",
            left_on="CUSTOMER_ID",
            right_on="USER_ID",
            validate="one_to_many",
            indicator=True,
        )
    except Exception as e:
        raise ValueError(f"Merge cardinality assumption violated (expected one_to_many): {e}")

    orphaned_orders = (merged["_merge"] == "right_only").sum()
    if orphaned_orders > 0:
        print(f"Warning: {orphaned_orders} orders have no matching customer.")

    customers_without_orders = (merged["_merge"] == "left_only").sum()
    print(f"{customers_without_orders} customers have no orders.")

    return merged.drop(columns=["_merge"])


def summarize_customers(df_merged: pd.DataFrame) -> pd.DataFrame:
    """
    Named-aggregation summary per customer, reusing Day 3's pattern:
    total orders, order count, distinct statuses seen.
    """
    summary = df_merged.groupby("CUSTOMER_ID").agg(
        order_count=("ID", "count"),
        distinct_statuses=("STATUS", "nunique"),
    ).reset_index()
    return summary


conn = get_connection()

try:
    cursor = conn.cursor()

    # Step 1: pull raw tables fresh
    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_CUSTOMERS")
    df_customers = cursor.fetch_pandas_all()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_ORDERS")
    df_orders = cursor.fetch_pandas_all()

    # Step 2: clean_and_merge (Day 2)
    df_merged = clean_and_merge(df_customers, df_orders)
    print("\nMerged shape:", df_merged.shape)

    # Step 3: named aggregation summary (Day 3 style)
    df_summary = summarize_customers(df_merged)
    print("\n=== Customer summary ===")
    print(df_summary.head(10))
    print("\nSummary shape:", df_summary.shape)

finally:
    conn.close()


