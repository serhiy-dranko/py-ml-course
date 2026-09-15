import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def clean_and_merge(df_primary: pd.DataFrame, df_secondary: pd.DataFrame) -> pd.DataFrame:
    """Cleans and merges RAW_CUSTOMERS + RAW_ORDERS. Reused directly from Day 2."""
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
    """Named-aggregation summary per customer. Reused directly from Day 3 style."""
    return df_merged.groupby("CUSTOMER_ID").agg(
        order_count=("ID", "count"),
        distinct_statuses=("STATUS", "nunique"),
    ).reset_index()


conn = get_connection()

try:
    cursor = conn.cursor()

    print("=" * 60)
    print("STEP 1: PULL RAW + RUN PIPELINE (Day 2 + Day 3 reused)")
    print("=" * 60)

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_CUSTOMERS")
    df_raw_customers = cursor.fetch_pandas_all()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_ORDERS")
    df_raw_orders = cursor.fetch_pandas_all()

    df_merged = clean_and_merge(df_raw_customers, df_raw_orders)
    print("\nMerged shape:", df_merged.shape)

    df_summary = summarize_customers(df_merged)
    print("\n=== Customer summary (first 10) ===")
    print(df_summary.head(10))

    print("\n" + "=" * 60)
    print("STEP 2: PULL STAGING COMPARISON DATA")
    print("=" * 60)

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.STG_CUSTOMERS")
    df_staging_customers = cursor.fetch_pandas_all()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.STG_ORDERS")
    df_staging_orders = cursor.fetch_pandas_all()

    print("\n" + "=" * 60)
    print("STEP 3: SYSTEMATIC RAW vs STAGING COMPARISON")
    print("=" * 60)

    print("\n--- Shape ---")
    print(f"RAW_CUSTOMERS: {df_raw_customers.shape}  |  STG_CUSTOMERS: {df_staging_customers.shape}")
    print(f"RAW_ORDERS:    {df_raw_orders.shape}  |  STG_ORDERS:    {df_staging_orders.shape}")

    print("\n--- Column names ---")
    print("RAW_ORDERS:  ", df_raw_orders.columns.tolist())
    print("STG_ORDERS:  ", df_staging_orders.columns.tolist())
    print("RAW_CUSTOMERS:", df_raw_customers.columns.tolist())
    print("STG_CUSTOMERS:", df_staging_customers.columns.tolist())

    print("\n--- Null counts ---")
    print("RAW_ORDERS:\n", df_raw_orders.isna().sum())
    print("STG_ORDERS:\n", df_staging_orders.isna().sum())

    print("\n--- Duplicate keys ---")
    print("RAW_ORDERS duplicated ID:", df_raw_orders.duplicated(subset=["ID"]).sum())
    print("STG_ORDERS duplicated ORDER_ID:", df_staging_orders.duplicated(subset=["ORDER_ID"]).sum())

    print("\n--- Cardinality: order status ---")
    print("RAW_ORDERS.STATUS unique:", df_raw_orders["STATUS"].nunique())
    print("STG_ORDERS.ORDER_STATUS unique:", df_staging_orders["ORDER_STATUS"].nunique())

    print("\n" + "=" * 60)
    print("STEP 4: PRESENTATION VISUALIZATIONS")
    print("=" * 60)

    fig, ax = plt.subplots(figsize=(7, 5))
    counts = [len(df_raw_customers), len(df_staging_customers)]
    bars = ax.bar(["RAW_CUSTOMERS", "STG_CUSTOMERS"], counts, color=["#888888", "#4C72B0"])
    ax.set_title(f"Customer row count is identical between raw and staging ({counts[0]} = {counts[1]})")
    ax.set_ylabel("Number of rows")
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(count), ha="center")
    plt.tight_layout()
    plt.savefig("chart1_row_counts.png", dpi=150)
    plt.close()
    print("Saved chart1_row_counts.png")

    orders_per_customer = df_raw_orders.groupby("USER_ID")["ID"].count()
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.histplot(orders_per_customer, bins=range(0, orders_per_customer.max() + 2), ax=ax, color="#4C72B0")
    ax.set_title("Most active customers place 1-2 orders; a few place 3+")
    ax.set_xlabel("Number of orders per customer (customers with 0 orders excluded)")
    ax.set_ylabel("Number of customers")
    plt.tight_layout()
    plt.savefig("chart2_orders_per_customer.png", dpi=150)
    plt.close()
    print("Saved chart2_orders_per_customer.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    status_counts = df_raw_orders["STATUS"].value_counts()
    status_counts.plot(kind="bar", ax=ax, color="#4C72B0")
    top_pct = status_counts.iloc[0] / status_counts.sum() * 100
    ax.set_title(f"'{status_counts.index[0]}' dominates order status at {top_pct:.0f}% of all orders")
    ax.set_xlabel("Status")
    ax.set_ylabel("Number of orders")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("chart3_status_distribution.png", dpi=150)
    plt.close()
    print("Saved chart3_status_distribution.png")

finally:
    conn.close()

print("\n" + "=" * 60)
print("CLOSING SUMMARY — WEEK 2 TAKEAWAY")
print("=" * 60)
print("""
dbt's staging layer here adds modest but real value: it renames every
ambiguous ID column into explicit, join-safe names (CUSTOMER_ID, ORDER_ID,
ORDER_STATUS) this is  the exact fix for the _x/_y merge confusion we hit on Day 2.
It does NOT filter or re-type anything, since the raw tables were
already clean. This week's real findings (38 customers with zero orders, one
payment row != one order, a right-skewed orders-per-customer distribution)
came from applying Day 1-3 techniques directly to the raw data, not from
dbt's staging transformations.
""")