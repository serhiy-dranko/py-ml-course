import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection
import matplotlib.pyplot as plt
import seaborn as sns

conn = get_connection()

try:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_CUSTOMERS")
    df_raw_customers = cursor.fetch_pandas_all()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_ORDERS")
    df_raw_orders = cursor.fetch_pandas_all()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.STG_CUSTOMERS")
    df_staging_customers = cursor.fetch_pandas_all()

    # Chart 1: row count before/after (customers)
    fig, ax = plt.subplots(figsize=(7, 5))
    counts = [len(df_raw_customers), len(df_staging_customers)]
    labels = ["RAW_CUSTOMERS", "STG_CUSTOMERS"]
    bars = ax.bar(labels, counts, color=["#888888", "#4C72B0"])
    ax.set_title(f"Customer row count is identical between raw and staging ({counts[0]} = {counts[1]})")
    ax.set_ylabel("Number of rows")
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(count), ha="center")
    plt.tight_layout()
    plt.savefig("chart1_row_counts.png", dpi=150)
    plt.close()
    print("Saved chart1_row_counts.png")

    # Chart 2: distribution of orders per customer
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

    # Chart 3: STATUS category distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    status_counts = df_raw_orders["STATUS"].value_counts()
    status_counts.plot(kind="bar", ax=ax, color="#4C72B0")
    top_pct = (status_counts.iloc[0] / status_counts.sum() * 100)
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