import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_CUSTOMERS")
    df_raw = cursor.fetch_pandas_all()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.STG_CUSTOMERS")
    df_staging = cursor.fetch_pandas_all()

    print("=== SHAPE COMPARISON ===")
    print("Raw shape:", df_raw.shape)
    print("Staging shape:", df_staging.shape)

    print("\n=== DTYPES: RAW ===")
    print(df_raw.dtypes)

    print("\n=== DTYPES: STAGING ===")
    print(df_staging.dtypes)

    print("\n=== COLUMN NAMES: RAW ===")
    print(df_raw.columns.tolist())

    print("\n=== COLUMN NAMES: STAGING ===")
    print(df_staging.columns.tolist())

    print("\n=== SAMPLE: RAW ===")
    print(df_raw.head())

    print("\n=== SAMPLE: STAGING ===")
    print(df_staging.head())

finally:
    conn.close()

## The staging model preserves the exact same row count (100) and column count (3) as the raw source table, indicating no filtering or row-level transformation occurs at this layer. 
## The most significant structural change is a column rename: the raw ID column becomes CUSTOMER_ID in staging, following the dbt convention of giving generic identifier columns explicit, join-friendly names. 
## Data types remained unchanged between the two layers for all three columns. FIRST_NAME and LAST_NAME values appear identical, suggesting no cleaning or reformatting was applied to this particular table at the staging level
## The transformation here is purely structural (renaming), not about data quality.