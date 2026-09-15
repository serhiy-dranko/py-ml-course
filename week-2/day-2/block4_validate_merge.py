import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_CUSTOMERS")
    df_customers = cursor.fetch_pandas_all()

    cursor.execute("SELECT * FROM JAFFLE_SHOP_DB.RAW.RAW_ORDERS")
    df_orders = cursor.fetch_pandas_all()

    # check for duplicates
    print("Duplicate customer IDs:", df_customers.duplicated(subset=["ID"]).sum())
    print("Duplicate order USER_ID values:",
          df_orders.duplicated(subset=["USER_ID"]).sum())

    validated_merge = df_customers.merge(
        df_orders,
        left_on="ID",
        right_on="USER_ID",
        how="left",
        validate="one_to_many",
    )
    print("\nValidated merge succeeded! Shape:", validated_merge.shape)
    print("\nValidated merge succeeded! Head:")
    print(validated_merge.head())

        ## validate="one_to_one" switch to incorrect validation to see the error
        ## Traceback (most recent call last):
        ##  File "C:\Users\User\Documents\Dataskools\py-ml-course\week-2\day-2\block4_validate_merge.py", line 22, in <module>
        ##    validated_merge = df_customers.merge(
        ##        df_orders,
        ##    ...<3 lines>...
        ##        validate="one_to_one",
        ##    )
        ##  File "C:\Users\User\Documents\Dataskools\py-ml-course\venv\Lib\site-packages\pandas\core\frame.py", line 10859, in merge
        ##    return merge(
        ##        self,
        ##    ...<11 lines>...
        ##        validate=validate,
        ##    )
        ##  File "C:\Users\User\Documents\Dataskools\py-ml-course\venv\Lib\site-packages\pandas\core\reshape\merge.py", line 170, in merge
        ##    op = _MergeOperation(
        ##        left_df,
        ##    ...<10 lines>...
        ##        validate=validate,
        ##    )
        ##  File "C:\Users\User\Documents\Dataskools\py-ml-course\venv\Lib\site-packages\pandas\core\reshape\merge.py", line 813, in __init__
        ##    self._validate_validate_kwd(validate)
        ##    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
        ##  File "C:\Users\User\Documents\Dataskools\py-ml-course\venv\Lib\site-packages\pandas\core\reshape\merge.py", line 1658, in _validate_validate_kwd
        ##    raise MergeError(
        ##        "Merge keys are not unique in right dataset; not a one-to-one merge"
        ##    )
        ## pandas.errors.MergeError: Merge keys are not unique in right dataset; not a one-to-one merge

        # indicator=True

    indicator_merge = df_customers.merge(
        df_orders,
        left_on="ID",
        right_on="USER_ID",
        how="outer",
        indicator=True,
    )
    print("\n=== _merge value counts ===")
    print(indicator_merge["_merge"].value_counts())

    print("\n=== Customers with no orders (left_only) ===")
    print(indicator_merge[indicator_merge["_merge"] == "left_only"][["ID_x", "FIRST_NAME", "LAST_NAME"]])

    print("\n=== Orders with no matching customer (right_only) ===")
    print(indicator_merge[indicator_merge["_merge"] == "right_only"])


finally:
    conn.close()