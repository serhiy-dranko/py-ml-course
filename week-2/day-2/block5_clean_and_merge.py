import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection
import pandas as pd


def clean_and_merge(df_primary: pd.DataFrame, df_secondary: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans RAW_CUSTOMERS (df_primary) and RAW_ORDERS (df_secondary),
    then merges them into one DataFrame: one row per customer-order pair,
    plus customers with zero orders (left join).

    Assumes df_primary has a unique 'ID' column (customer key),
    and df_secondary has a 'USER_ID' column referencing it (many-to-one).
    """

    # Rename the primary key up front to avoid ambiguous _x/_y suffixes downstream
    df_primary = df_primary.rename(columns={"ID": "CUSTOMER_ID"})

    # --- Missing data handling ---
    # Note: in practice RAW_CUSTOMERS/RAW_ORDERS came back fully populated.
    # These steps are defensive — they activate only if nulls are present,
    # so the function stays correct even if source data quality changes later.

    # Drop rows with no order date — a missing date makes an order un-analyzable
    # for any time-based reporting, and we treat it as rare/random.
    
    before_drop = len(df_secondary)
    df_secondary = df_secondary.dropna(subset=["ORDER_DATE"])
    dropped_count = before_drop - len(df_secondary)
    print(f"Dropped {dropped_count} orders with missing ORDER_DATE.")

    # Fill missing STATUS with an explicit 'unknown' category rather than
    # guessing a real status — keeps the row without inventing false information.
    df_secondary["STATUS"] = df_secondary["STATUS"].fillna("unknown")

    # --- Validated merge ---
    # One customer can have many orders, but each order belongs to exactly one
    # customer — so we expect a one-to-many relationship. If that assumption
    # is ever violated (e.g. duplicate customer IDs appear), we want a loud
    # failure here, not a silently inflated row count downstream.
    try:
        merged = df_primary.merge(
            df_secondary,
            left_on="CUSTOMER_ID",
            right_on="USER_ID",
            how="left",
            validate="one_to_many",
            indicator=True,
        )
    except Exception as e:
        raise ValueError(
            f"Merge cardinality assumption violated (expected one_to_many): {e}"
        )

    # Audit: flag if anything unexpected shows up on the right side
    orphaned_orders = (merged["_merge"] == "right_only").sum()
    if orphaned_orders > 0:
        print(f"Warning: {orphaned_orders} orders have no matching customer.")
        
    # Audit: flag if anything unexpected shows up on the left side
    customers_without_orders = (merged["_merge"] == "left_only").sum()
    print(f"{customers_without_orders} customers have no orders.")

    return merged.drop(columns=["_merge"])


conn = get_connection()

try:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_CUSTOMERS")
    df_customers = cursor.fetch_pandas_all()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_ORDERS")
    df_orders = cursor.fetch_pandas_all()

    result = clean_and_merge(df_customers, df_orders)

    print("\n=== Final result ===")
    print("Shape:", result.shape)
    print(result.head(140))

finally:
    conn.close()