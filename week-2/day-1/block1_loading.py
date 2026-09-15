import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection
import pandas as pd

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER LIMIT 5000")

    df = cursor.fetch_pandas_all()

    print(df.info())
    print(df.dtypes)
    print(df.shape)
    print(df.head())

    # task 4 — manual method
    cursor2 = conn.cursor()
    cursor2.execute("SELECT * FROM CUSTOMER LIMIT 5000")
    manual_rows = cursor2.fetchall()
    manual_columns = [col[0] for col in cursor2.description]

    df_manual = pd.DataFrame(manual_rows, columns=manual_columns)

    print("\n--- Manual method dtypes ---")
    print(df_manual.dtypes)

finally:
    conn.close()

    ## When data comes in "manually" without any help with type recognition, literally everything becomes a object — even numeric column (C_ACCTBAL) and data.