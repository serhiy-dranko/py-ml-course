import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

import matplotlib.pyplot as plt
import seaborn as sns

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_PAYMENTS")
    df = cursor.fetch_pandas_all()

# Point 1: Histograms

    print("=== Histogram: AMOUNT ===")

    df["AMOUNT"].hist(bins=20)

    plt.title("Distribution of AMOUNT")
    plt.xlabel("AMOUNT")
    plt.ylabel("Count")
    plt.show()


    print("\n=== Histogram: ORDER_ID ===")

    df["ORDER_ID"].hist(bins=20)

    plt.title("Distribution of ORDER_ID")
    plt.xlabel("ORDER_ID")
    plt.ylabel("Count")
    plt.show()


    # Point 2: Boxplot

    print("\n=== Boxplot: AMOUNT by PAYMENT_METHOD ===")

    sns.boxplot(
        data=df,
        x="PAYMENT_METHOD",
        y="AMOUNT"
    )

    plt.title("AMOUNT by PAYMENT_METHOD")
    plt.xlabel("PAYMENT_METHOD")
    plt.ylabel("AMOUNT")
    plt.show()

# Point 3: Scatter plot

    print("\n=== Scatter plot: ORDER_ID vs AMOUNT ===")

    sns.scatterplot(
        data=df,
        x="ORDER_ID",
        y="AMOUNT"
    )

    plt.title("ORDER_ID vs AMOUNT")
    plt.xlabel("ORDER_ID")
    plt.ylabel("AMOUNT")
    plt.show()

finally:
    conn.close()